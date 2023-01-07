"""Future"""
from __future__ import annotations

import concurrent.futures
from collections.abc import Generator
from concurrent.futures._base import PENDING
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeAlias, TypeVar, cast

from . import monad, try_

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
U = TypeVar("U")
P = ParamSpec("P")


class ProcessPoolExecutionContext(concurrent.futures.ProcessPoolExecutor):
    def submit(self, fn: Callable[..., T], /, *args: ..., **kwargs: ...) -> Future[T]:
        with self._shutdown_lock:
            if self._broken:
                raise concurrent.futures.process.BrokenProcessPool(self._broken)
            if self._shutdown_thread:
                raise RuntimeError("cannot schedule new futures after shutdown")
            if concurrent.futures.process._global_shutdown:
                raise RuntimeError(
                    "cannot schedule new futures after " "interpreter shutdown"
                )

            future = Future[T]()
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
    def submit(self, fn: Callable[..., T], /, *args: ..., **kwargs: ...) -> Future[T]:
        with self._shutdown_lock, concurrent.futures.thread._global_shutdown_lock:
            if self._broken:
                raise concurrent.futures.thread.BrokenThreadPool(self._broken)

            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")
            if concurrent.futures.thread._shutdown:
                raise RuntimeError(
                    "cannot schedule new futures after " "interpreter shutdown"
                )

            future = Future[T]()
            work_item = concurrent.futures.thread._WorkItem(future, fn, args, kwargs)

            self._work_queue.put(work_item)
            self._adjust_thread_count()
            return future


class Future(concurrent.futures.Future[T], monad.Monad[T]):
    """Future"""

    def __init__(self) -> None:
        super().__init__()

    def unapply(self) -> tuple[()] | tuple[Any]:
        return (self.result(),)

    def __bool__(self) -> bool:
        return self.done() and bool(self.value)

    def __iter__(self) -> Generator[Future[T], None, T]:
        try:
            match self.pattern:
                case try_.Failure():
                    yield self
                    raise GeneratorExit(self)
                case try_.Success(value):
                    yield self
                    return value
        except Exception:
            raise

    @staticmethod
    def pure(*args: ..., **kwargs: ...) -> Future[T]:
        return Future[T].successful(*args, **kwargs)

    def map(
        self, functor: Callable[[T], TT], /
    ) -> Callable[[ExecutionContext], Future[TT]]:
        def with_context(executor: ExecutionContext, /) -> Future[TT]:
            def fold(previous_result: try_.Try[T], /) -> try_.Try[TT]:
                match previous_result.pattern:
                    case try_.Failure() as failure:
                        return cast(try_.Failure[TT], failure)
                    case try_.Success(previous_value):
                        return try_.Success[TT](functor(previous_value))

            return self.transform(fold)(executor)

        return with_context

    def flat_map(
        self, other: Callable[[T], Future[TT]], /
    ) -> Callable[[ExecutionContext], Future[TT]]:
        def with_context(executor: ExecutionContext, /) -> Future[TT]:
            def fold(try__: try_.Try[T]) -> Future[TT]:
                match try__.pattern:
                    case try_.Failure():
                        return cast(Future[TT], self)
                    case try_.Success(value):
                        try:
                            return other(value)
                        except Exception as exception:
                            return Future[TT].failed(exception)

            return self.transform_with(fold)(executor)

        return with_context

    def recover(
        self, other: Callable[[Exception], TT], /
    ) -> Callable[[ExecutionContext], Future[TT]]:
        def with_context(executor: ExecutionContext, /) -> Future[TT]:
            return self.transform(lambda try__: try__.recover(other))(executor)

        return with_context

    def recover_with(
        self, other: Callable[[Exception], Future[TT]], /
    ) -> Callable[[ExecutionContext], Future[TT]]:
        def with_context(executor: ExecutionContext, /) -> Future[TT]:
            def complete(try__: try_.Try[T]) -> Future[TT]:
                match try__.pattern:
                    case try_.Failure() as failure:
                        if (result := other(failure.exception)) is None:
                            return Future[TT].failed(failure.exception)
                        else:
                            return result
                    case try_.Success():
                        return cast(Future[TT], self)

            return self.transform_with(complete)(executor)

        return with_context

    def transform(
        self, try_other: Callable[[try_.Try[T]], try_.Try[TT]], /
    ) -> Callable[[ExecutionContext], Future[TT]]:
        def with_context(executor: ExecutionContext, /) -> Future[TT]:
            current_future = Future[TT]()  # PENDING
            self.on_complete(
                lambda result: current_future.try_complete(try_other(result))
            )(executor)
            return current_future

        return with_context

    def transform_with(
        self, other: Callable[[try_.Try[T]], Future[TT]], /
    ) -> Callable[[ExecutionContext], Future[TT]]:
        def with_context(executor: ExecutionContext, /) -> Future[TT]:
            current_future = Future[TT]()

            def complete(previous_result: try_.Try[T]) -> None:
                previous_future = other(previous_result)
                previous_future.on_complete(
                    lambda current_result: current_future.try_complete(current_result),
                )(executor)

            self.on_complete(complete)(executor)
            return current_future

        return with_context

    def try_complete(self, preview_result: try_.Try[T], /) -> bool:
        def callback(self: Future[T]):
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

    def on_complete(
        self, try_complete_other: Callable[[try_.Try[T]], U], /
    ) -> Callable[[ExecutionContext], None]:
        def with_context(executor: ExecutionContext, /) -> None:
            if not self.done():
                self.add_done_callback(fn=lambda _: try_complete_other(self.value))
            else:
                try:
                    try_complete_other(self.value)
                except Exception as exception:
                    self._exception = exception
                    self._result = None

        return with_context

    @staticmethod
    def successful(value: T, /) -> Future[T]:
        future = Future[T]()
        future.set_result(result=value)
        return future

    @staticmethod
    def failed(exception: Exception, /) -> Future[T]:
        future = Future[T]()
        future.set_exception(exception=exception)
        return future

    @staticmethod
    def from_try(try_value: try_.Try[T], /) -> Future[T]:
        match try_value.pattern:
            case try_.Failure() as failure:
                return Future[T].failed(failure.exception)
            case try_.Success(value):
                return Future[T].successful(value)

    @property
    def value(self) -> SubType[T]:
        try:
            return try_.Success[T](self.result())
        except Exception as failure:
            return try_.Failure[T](failure)

    @property
    def pattern(self) -> SubType[T]:
        return self.value

    @staticmethod
    def do(
        context: Callable[P, FutureDo[T]], /
    ) -> Callable[P, Callable[[ExecutionContext], Future[T]]]:
        """map, flat_map combination syntax sugar.

        Only type checking can determine type violations, and runtime errors may not occur.
        """

        @wraps(context)
        def wrapper(
            *args: P.args, **kwargs: P.kwargs
        ) -> Callable[[ExecutionContext], Future[T]]:
            def with_context(executor: ExecutionContext, /) -> Future[T]:
                context_ = context(*args, **kwargs)
                try:
                    while True:
                        yield_state = next(context_)
                        if not isinstance(yield_state, Future):
                            raise TypeError(yield_state)
                        match yield_state.composability():
                            case monad.Composability.Immutable:
                                return yield_state
                            case monad.Composability.Variable:
                                # Priority is given to the value of the sub-generator's monad.
                                ...
                except StopIteration as return_:
                    return Future[T].pure(return_.value)

            return with_context

        return wrapper

    def method(self, other: Callable[[Future[T]], TT], /) -> TT:
        return other(self)

    @staticmethod
    def hold(
        function: Callable[P, T]
    ) -> Callable[P, Callable[[ExecutionContext], Future[T]]]:
        """

        Example usage of ProcessPoolExecutionContext:

            ec = ProcessPoolExecutionContext(max_worker=5)

            def toplevel_function(*args, **kwargs) -> T:
                ...

            _ = Future.hold(toplevel_function)(*args, **kwargs)(ec)

        Example usage of ThreadPoolExecutionContext:

            ec = ThreadPoolExecutionContext(max_worker=5)

            @Future.hold
            def function(*args, **kwargs) -> T:
                ...

            _ = function(*args, **kwargs)(ec)

        """

        @wraps(function)
        def wrapper(
            *args: P.args, **kwargs: P.kwargs
        ) -> Callable[[ExecutionContext], Future[T]]:
            def with_context(executor: ExecutionContext, /) -> Future[T]:
                return executor.submit(function, *args, **kwargs)

            return with_context

        return wrapper


FutureDo: TypeAlias = Generator[Future[T], None, T]
ExecutionContext: TypeAlias = ProcessPoolExecutionContext | ThreadPoolExecutionContext
SubType: TypeAlias = try_.Failure[T] | try_.Success[T]
