"""Future"""
from __future__ import annotations

import asyncio
import concurrent.futures
import dataclasses
from abc import ABC
from collections.abc import Generator
from concurrent.futures._base import PENDING
from typing import Any, Callable, ParamSpec, Type, TypeVar

from category.try_ import Failure, Success, Try

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


class Future(concurrent.futures.Future[T]):
    """Future"""

    def __init__(self) -> None:
        super().__init__()

    def __bool__(self) -> bool:
        return self.done() and bool(self.value)

    def __iter__(
        self,
    ) -> Generator[
        tuple[Future[T], Callable[[Future[T]], T], Callable[[T], Future[T]]],
        tuple[Future[T], Callable[[Future[T]], T], Callable[[T], Future[T]]],
        T,
    ]:
        lift: Callable[[T], Future[T]] = lambda value: Future[T].successful(value)
        flattened_monad = self.flatmap(ThreadPoolExecutionContext)(lift)
        try:
            yield flattened_monad, Future.result, lift
            return flattened_monad.result()
        except Exception as error:
            yield flattened_monad, Future.result, lift
            raise GeneratorExit from error

    def map(
        self, ec: Type[ExecutionContext], /
    ) -> Callable[[Callable[[T], TT]], Future[TT]]:
        def wrapper(functor: Callable[[T], TT], /) -> Future[TT]:
            def fold(try_: Try[T]) -> Try[TT]:
                match try_.pattern:
                    case Failure() as failure:
                        return Failure[TT](failure.exception)
                    case Success(value):
                        return Success[TT](functor(value))

            return self.transform(ec)(fold)

        return wrapper

    def flatmap(
        self, ec: Type[ExecutionContext], /
    ) -> Callable[[Callable[[T], Future[TT]]], Future[TT]]:
        def wrapper(functor: Callable[[T], Future[TT]], /) -> Future[TT]:
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

        return wrapper

    def transform(
        self, ec: Type[ExecutionContext], /
    ) -> Callable[[Callable[[Try[T]], Try[TT]]], Future[TT]]:
        def wrapper(functor: Callable[[Try[T]], Try[TT]], /) -> Future[TT]:
            future = Future[TT]()
            self.on_complete(ec)(lambda result: future.try_complete(functor(result)))
            return future

        return wrapper

    def transform_with(
        self, functor: Callable[[Try[T]], Future[TT]], /
    ) -> Callable[[Type[ExecutionContext]], Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            next_future = Future[TT]()

            def complete(current_result: Try[T]) -> None:
                current_future = functor(current_result)
                return current_future.on_complete(ec)(
                    lambda next_result: next_future.try_complete(next_result),
                )

            self.on_complete(ec)(complete)
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
        self, ec: Type[ExecutionContext], /
    ) -> Callable[[Callable[[Try[T]], U]], None]:
        def wrapper(functor: Callable[[Try[T]], U], /) -> None:
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

        return wrapper

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

    def method(self, functor: Callable[[Future[T]], TT], /) -> TT:
        return functor(self)

    @staticmethod
    def hold(
        functor: Callable[P, T]
    ) -> Callable[[Type[ExecutionContext]], Callable[P, Future[T]]]:
        def with_context(ec: Type[ExecutionContext], /) -> Callable[P, Future[T]]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> Future[T]:
                # FIXME: Threaded processing
                try:
                    result = functor(*args, **kwargs)
                    return Future[T].successful(result)
                except Exception as error:
                    future = Future[T]()
                    future.set_exception(exception=error)
                    return future

            return wrapper

        return with_context


FutureDo = Generator[
    tuple[Future[T], Callable[[Future[T]], T], Callable[[T], Future[T]]],
    tuple[Future[T], Callable[[Future[T]], T], Callable[[T], Future[T]]],
    T,
]
