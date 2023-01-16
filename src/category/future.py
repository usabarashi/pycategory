"""Future"""
from __future__ import annotations

import concurrent.futures
from collections.abc import Generator
from concurrent.futures._base import PENDING
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeAlias, TypeVar, cast

from . import extension, implicit_, monad, try_

Sm = TypeVar("Sm", contravariant=True)
Tm = TypeVar("Tm", covariant=True)
U = TypeVar("U")
P = ParamSpec("P")


class ProcessPoolExecutionContext(concurrent.futures.ProcessPoolExecutor):
    def submit(self, fn: Callable[..., Sm], /, *args: ..., **kwargs: ...) -> Future[Sm]:
        with self._shutdown_lock:
            if self._broken:
                raise concurrent.futures.process.BrokenProcessPool(self._broken)
            if self._shutdown_thread:
                raise RuntimeError("cannot schedule new futures after shutdown")
            if concurrent.futures.process._global_shutdown:
                raise RuntimeError(
                    "cannot schedule new futures after " "interpreter shutdown"
                )

            future = Future[Sm]()
            work_item = concurrent.futures.process._WorkItem(future, fn, args, kwargs)

            self._pending_work_items[self._queue_count] = work_item
            self._work_ids.put(self._queue_count)
            self._queue_count += 1
            # Wake up queue management thread
            self._executor_manager_thread_wakeup.wakeup()

            self._adjust_process_count()
            self._start_executor_manager_thread()
            return future


class ThreadPoolExecutionContext(concurrent.futures.ThreadPoolExecutor):
    def submit(self, fn: Callable[..., Sm], /, *args: ..., **kwargs: ...) -> Future[Sm]:
        with self._shutdown_lock, concurrent.futures.thread._global_shutdown_lock:
            if self._broken:
                raise concurrent.futures.thread.BrokenThreadPool(self._broken)

            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")
            if concurrent.futures.thread._shutdown:
                raise RuntimeError(
                    "cannot schedule new futures after " "interpreter shutdown"
                )

            future = Future[Sm]()
            work_item = concurrent.futures.thread._WorkItem(future, fn, args, kwargs)

            self._work_queue.put(work_item)
            self._adjust_thread_count()
            return future


class Future(monad.Monad[Sm], concurrent.futures.Future[Sm], extension.Extension):
    """Future"""

    def __init__(self) -> None:
        super().__init__()

    def unapply(self) -> tuple[()] | tuple[Any]:
        return (self.result(),)

    def __iter__(self) -> Generator[Future[Sm], None, Sm]:
        try:
            match self.pattern:
                case try_.Failure() as failure:
                    raise GeneratorExit(self) from failure.exception
                case try_.Success(value):
                    yield self
                    return value
        except Exception:
            raise

    @staticmethod
    def pure(value: Sm) -> Future[Sm]:
        return Future.successful(value)

    @implicit_.explicit[concurrent.futures.Executor].hold
    def map(self, func: Callable[[Sm], Tm], /) -> Future[Tm]:
        if (executor := implicit_.parameter(concurrent.futures.Executor)) is None:
            raise implicit_.CannotFindImplicitParameter(ExecutionContext)

        def fold(previous_result: try_.Try[Sm], /) -> try_.Try[Tm]:
            match previous_result.pattern:
                case try_.Failure() as failure:
                    return cast(try_.Failure[Tm], failure)
                case try_.Success(previous_value):
                    return try_.Success[Tm](func(previous_value))

        return self.transform(fold)(executor)

    @implicit_.explicit[concurrent.futures.Executor].hold
    def flat_map(self, func: Callable[[Sm], Future[Tm]], /) -> Future[Tm]:
        if (executor := implicit_.parameter(concurrent.futures.Executor)) is None:
            raise implicit_.CannotFindImplicitParameter(ExecutionContext)

        def fold(try__: try_.Try[Sm]) -> Future[Tm]:
            match try__.pattern:
                case try_.Failure():
                    return cast(Future[Tm], self)
                case try_.Success(value):
                    try:
                        return func(value)
                    except Exception as exception:
                        return Future[Tm].failed(exception)

        return self.transform_with(fold)(executor)

    @implicit_.explicit[concurrent.futures.Executor].hold
    def recover(self, func: Callable[[Exception], Tm], /) -> Future[Tm]:
        if (executor := implicit_.parameter(concurrent.futures.Executor)) is None:
            raise implicit_.CannotFindImplicitParameter(ExecutionContext)
        return self.transform(lambda try__: try__.recover(func))(executor)

    @implicit_.explicit[concurrent.futures.Executor].hold
    def recover_with(self, func: Callable[[Exception], Future[Tm]], /) -> Future[Tm]:
        if (executor := implicit_.parameter(concurrent.futures.Executor)) is None:
            raise implicit_.CannotFindImplicitParameter(ExecutionContext)

        def complete(try__: try_.Try[Sm]) -> Future[Tm]:
            match try__.pattern:
                case try_.Failure() as failure:
                    if (result := func(failure.exception)) is None:
                        return Future[Tm].failed(failure.exception)
                    else:
                        return result
                case try_.Success():
                    return cast(Future[Tm], self)

        return self.transform_with(complete)(executor)

    @implicit_.explicit[concurrent.futures.Executor].hold
    def transform(
        self, try_other: Callable[[try_.Try[Sm]], try_.Try[Tm]], /
    ) -> Future[Tm]:
        if (executor := implicit_.parameter(concurrent.futures.Executor)) is None:
            raise implicit_.CannotFindImplicitParameter(ExecutionContext)
        current_future = Future[Tm]()  # PENDING
        self.on_complete(lambda result: current_future.try_complete(try_other(result)))(
            executor
        )
        return current_future

    @implicit_.explicit[concurrent.futures.Executor].hold
    def transform_with(
        self, func: Callable[[try_.Try[Sm]], Future[Tm]], /
    ) -> Future[Tm]:
        if (executor := implicit_.parameter(concurrent.futures.Executor)) is None:
            raise implicit_.CannotFindImplicitParameter(ExecutionContext)
        current_future = Future[Tm]()

        def complete(previous_result: try_.Try[Sm]) -> None:
            previous_future = func(previous_result)
            previous_future.on_complete(
                lambda current_result: current_future.try_complete(current_result),
            )(executor)

        self.on_complete(complete)(executor)
        return current_future

    def try_complete(self, preview_result: try_.Try[Sm], /) -> bool:
        def callback(self: Future[Sm]):
            match preview_result.pattern:
                case try_.Failure() as failure:
                    self._exception = failure.exception
                    self._result = None
                    for waiter in self._waiters:
                        waiter.add_result(self)
                case try_.Success(value):
                    self._exception = None
                    self._result = value
                    for waiter in self._waiters:
                        waiter.add_result(self)

        if self.done():
            return False
        elif self._state is PENDING:
            self.add_done_callback(fn=callback)
            self.set_result(None)  # PENDING -> FINISHED
            return True
        else:
            self.add_done_callback(fn=callback)
            return True

    @implicit_.explicit[concurrent.futures.Executor].hold
    def on_complete(self, try_complete_other: Callable[[try_.Try[Sm]], U], /) -> None:
        if not self.done():
            self.add_done_callback(fn=lambda _: try_complete_other(self.value))
        else:
            try:
                try_complete_other(self.value)
            except Exception as exception:
                self._exception = exception
                self._result = None

    @staticmethod
    def successful(value: Sm, /) -> Future[Sm]:
        future = Future[Sm]()
        future.set_result(result=value)
        return future

    @staticmethod
    def failed(exception: Exception, /) -> Future[Sm]:
        future = Future[Sm]()
        future.set_exception(exception=exception)
        return future

    @staticmethod
    def from_try(try_value: try_.Try[Sm], /) -> Future[Sm]:
        match try_value.pattern:
            case try_.Failure() as failure:
                return Future[Sm].failed(failure.exception)
            case try_.Success(value):
                return Future[Sm].successful(value)

    @property
    def value(self) -> SubType[Sm]:
        try:
            return try_.Success[Sm](self.result())
        except Exception as failure:
            return try_.Failure[Sm](failure)

    @property
    def pattern(self) -> SubType[Sm]:
        return self.value

    @staticmethod
    def hold(func: Callable[P, Sm]) -> implicit_.Implicit[Callable[P, Future[Sm]]]:
        @wraps(func)
        @implicit_.implicit[concurrent.futures.Executor].hold
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Future[Sm]:
            if (executor := implicit_.parameter(concurrent.futures.Executor)) is None:
                raise implicit_.CannotFindImplicitParameter(ExecutionContext)
            return executor.submit(func, *args, **kwargs)

        return wrapper

    @staticmethod
    def hold_explicit(
        func: Callable[P, Sm]
    ) -> Callable[P, Callable[[concurrent.futures.Executor], Future[Sm]]]:
        @wraps(func)
        @implicit_.explicit[concurrent.futures.Executor].hold
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Future[Sm]:

            if (executor := implicit_.parameter(concurrent.futures.Executor)) is None:
                raise implicit_.CannotFindImplicitParameter(ExecutionContext)
            return executor.submit(func, *args, **kwargs)

        return wrapper


ExecutionContext: TypeAlias = ProcessPoolExecutionContext | ThreadPoolExecutionContext
SubType: TypeAlias = try_.Failure[Sm] | try_.Success[Sm]
FutureDo: TypeAlias = Generator[Future[Sm], None, Sm]
