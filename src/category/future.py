"""Future"""
from __future__ import annotations

import asyncio
import concurrent.futures
import dataclasses
from abc import ABC
from collections.abc import Generator
from concurrent.futures._base import PENDING
from functools import wraps
from typing import Any, Callable, ParamSpec, Type, TypeAlias, TypeVar

from category.try_ import Failure, Monad, Success, Try

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
U = TypeVar("U")
P = ParamSpec("P")


class ExecutionContext(ABC):
    """ExecutionContext"""

    loop: Callable[[], asyncio.AbstractEventLoop]
    executor: Type[concurrent.futures.ThreadPoolExecutor]


@dataclasses.dataclass(frozen=True)
class ThreadPoolExecutionContext(ExecutionContext):
    """ThreadPoolExecutionContext"""

    loop: Callable[[], asyncio.AbstractEventLoop] = asyncio.get_running_loop
    executor: Type[
        concurrent.futures.ThreadPoolExecutor
    ] = concurrent.futures.ThreadPoolExecutor


class Future(Monad, concurrent.futures.Future[T]):
    """Future"""

    def __init__(self) -> None:
        super().__init__()

    def __bool__(self) -> bool:
        return self.done() and bool(self.value)

    def __iter__(self) -> Generator[Future[T], None, T]:
        try:
            flattened_monad = self.flatmap(lambda value: Future[T].successful(value))(
                ExecutionContext
            )
            yield flattened_monad
            return flattened_monad.result()
        except Exception as error:
            future = Future[T]()
            future.set_exception(error)
            yield future
            raise GeneratorExit from error

    @staticmethod
    def send(monad: Future[T], /) -> T:
        return monad.result()

    @staticmethod
    def lift(value: T, /) -> Future[T]:
        return Future[T].successful(value)

    def map(
        self, functor: Callable[[T], TT], /
    ) -> Callable[[Type[ExecutionContext]], Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            def fold(try_: Try[T], /) -> Try[TT]:
                match try_.pattern:
                    case Failure() as failure:
                        return Failure[TT](failure.exception)
                    case Success(value):
                        return Success[TT](functor(value))

            return self.transform(fold)(ec)

        return with_context

    def flatmap(
        self, functor: Callable[[T], Future[TT]], /
    ) -> Callable[[Type[ExecutionContext]], Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            def fold(try_: Try[T]) -> Future[TT]:
                match try_.pattern:
                    case Failure() as failure:
                        future = Future[TT]()
                        future.set_exception(exception=failure.exception)
                        return future
                    case Success(value):
                        try:
                            return functor(value)
                        except Exception as error:
                            future = Future[TT]()
                            future.set_exception(exception=error)
                            return future

            return self.transform_with(fold)(ec)

        return with_context

    def transform(
        self, functor: Callable[[Try[T]], Try[TT]], /
    ) -> Callable[[Type[ExecutionContext]], Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            future = Future[TT]()
            self.on_complete(lambda result: future.try_complete(functor(result)))(ec)
            return future

        return with_context

    def transform_with(
        self, functor: Callable[[Try[T]], Future[TT]], /
    ) -> Callable[[Type[ExecutionContext]], Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            next_future = Future[TT]()

            def complete(current_result: Try[T]) -> None:
                current_future = functor(current_result)
                return current_future.on_complete(
                    lambda next_result: next_future.try_complete(next_result),
                )(ec)

            self.on_complete(complete)(ec)
            return next_future

        return with_context

    def try_complete(self, result: Try[T], /) -> bool:
        if self.done():
            return False
        elif self._state is PENDING:
            match result.pattern:
                case Failure() as failure:
                    self.set_exception(exception=failure.exception)
                case Success(value):
                    self.set_result(result=value)
            return True
        else:

            def callback(self: Future[T]):
                match result.pattern:
                    case Failure() as failure:
                        self._result = None
                        self._exception = failure.exception
                    case Success(value):
                        self._result = value
                        self._exceptoin = None

            self.add_done_callback(fn=callback)
            return True

    def on_complete(
        self, functor: Callable[[Try[T]], U], /
    ) -> Callable[[Type[ExecutionContext]], None]:
        def with_context(ec: Type[ExecutionContext], /) -> None:
            if self.done():

                def callback(self: Future[T]) -> None:
                    try:
                        # FIXME: Threaded processing
                        result = self.result()
                        self._result = functor(Success(result))
                        self._exception = None
                    except Exception as error:
                        self._result = functor(Failure(error))
                        self._exception = None

                self.add_done_callback(fn=callback)

        return with_context

    @staticmethod
    def successful(value: T, /) -> Future[T]:
        future = Future[T]()
        future.set_result(result=value)
        return future

    @property
    def value(self) -> Try[T]:
        try:
            return Success[T](self.result())
        except Exception as failure:
            return Failure[T](failure)

    @staticmethod
    def do(context: Callable[P, FutureDo[T]], /) -> Callable[P, Future[T]]:
        """map, flatmap combination syntax sugar.

        Only type checking can determine type violations, and runtime errors may not occur.
        """

        @wraps(context)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Future[T]:
            context_ = context(*args, **kwargs)
            state: Any = None
            try:
                while True:
                    flatmapped = context_.send(state)
                    match flatmapped.value.pattern:
                        case Failure():
                            return flatmapped
                        case Success():
                            state = Future[Any].send(flatmapped)
                        case _:
                            raise TypeError(flatmapped)
            except StopIteration as return_:
                return Future[T].lift(return_.value)

        return wrapper

    def method(self, functor: Callable[[Future[T]], TT], /) -> TT:
        return functor(self)

    @staticmethod
    def hold(
        function: Callable[P, T]
    ) -> Callable[P, Callable[[Type[ExecutionContext]], Future[T]]]:
        @wraps(function)
        def wrapper(
            *args: P.args, **kwargs: P.kwargs
        ) -> Callable[[Type[ExecutionContext]], Future[T]]:
            def with_context(ec: Type[ExecutionContext], /) -> Future[T]:
                # FIXME: Threaded processing
                try:
                    result = function(*args, **kwargs)
                    return Future[T].successful(result)
                except Exception as error:
                    future = Future[T]()
                    future.set_exception(exception=error)
                    return future

            return with_context

        return wrapper


FutureDo: TypeAlias = Generator[Future[Any], Any, T]
