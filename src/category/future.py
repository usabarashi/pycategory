"""Future"""
from __future__ import annotations

import asyncio
import concurrent.futures
import dataclasses
from abc import ABC
from collections.abc import Generator
from concurrent.futures._base import PENDING
from typing import Any, Callable, Optional, Type, TypeVar

from category.try_ import Failure, Success, Try

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
U = TypeVar("U")


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
        return self.done()

    def __call__(self) -> Generator[Try[T], Try[T], T]:
        try:
            success = self.result()
            yield Success(success)
            return success
        except Exception as error:
            yield Failure(error)
            raise GeneratorExit(self) from error

    def map(self, functor: Callable[[T], TT], /) -> Callable[..., Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            def fold(try_: Try[T]) -> Try[TT]:
                match try_.pattern:
                    case Failure() as failure:
                        return Failure[TT](failure.exception)
                    case Success(value):
                        return Success[TT](functor(value))

            return self.transform(fold)(ec)

        return with_context

    def flatmap(
        self, functor: Callable[[T], Future[TT]], /
    ) -> Callable[..., Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            def fold(try_: Try[T]) -> Future[TT]:
                match try_.pattern:
                    case Failure() as failure:
                        future = Future[TT]()
                        future.set_exception(exception=failure.exception)
                        return future
                    case Success(value):
                        return functor(value)

            return self.transform_with(fold)(ec)

        return with_context

    def transform(
        self, functor: Callable[[Try[T]], Try[TT]], /
    ) -> Callable[..., Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            future = Future[TT]()
            self.on_complete(lambda result: future.try_complete(functor(result)))(ec)
            return future

        return with_context

    def transform_with(
        self, functor: Callable[[Try[T]], Future[TT]], /
    ) -> Callable[..., Future[TT]]:
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
        self,
        functor: Callable[[Try[T]], U],
        /,
    ) -> Callable[..., None]:
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

    def method(self, functor: Callable[[Future[T]], TT], /) -> TT:
        return functor(self)

    @staticmethod
    def hold(
        functor: Callable[..., T]
    ) -> Callable[..., Callable[[Type[ExecutionContext]], Future[T]]]:
        def wrapper(
            *args: Any, **kwargs: Any
        ) -> Callable[[Type[ExecutionContext]], Future[T]]:
            def with_context(ec: Type[ExecutionContext], /) -> Future[T]:
                # FIXME: Threaded processing
                try:
                    return Future[T].successful(functor(*args, **kwargs))
                except Exception as error:
                    future = Future[T]()
                    future.set_exception(exception=error)
                    return future

            return with_context

        return wrapper

    @staticmethod
    def do(generator_function: Callable[..., FutureDo[T]]) -> Callable[..., Future[T]]:
        def wrapper(*args: Any, **kwargs: Any) -> Future[T]:
            state: Optional[Any] = None
            context = generator_function(*args, **kwargs)
            while True:
                try:
                    result = context.send(state)
                except StopIteration as return_:
                    return Future[T].successful(return_.value)
                match result:
                    case Failure() as failure:
                        future = Future[T]()
                        future.set_exception(failure.exception)
                        return future
                    case Success(value):
                        state = value
                    case _:
                        raise ValueError(result)

        return wrapper


FutureDo = Generator[Any | Try[Any], Any | Try[Any], T]
