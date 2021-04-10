"""Future"""
from __future__ import annotations

import asyncio
import concurrent.futures
import dataclasses
from abc import ABC
from concurrent.futures._base import PENDING
from typing import Any, Callable, Generator, Type, TypeVar, Union

from category.try_ import Failure, Success, Try

T = TypeVar("T")
TT = TypeVar("TT")
U = TypeVar("U")


class ExecutionContext(ABC):
    """ExecutionContext"""

    loop: asyncio.AbstractEventLoop
    executor: Type[concurrent.futures.ThreadPoolExecutor]


@dataclasses.dataclass(frozen=True)
class ThreadPoolExecutionContext(ExecutionContext):
    """ThreadPoolExecutionContext"""

    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
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
            yield Success(value=success)
            return success
        except Exception as error:
            yield Failure(value=error)
            raise GeneratorExit(self) from error

    def map(self, functor: Callable[[T], TT]) -> Callable[..., Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            def fold(try_: Try[T]) -> Try[TT]:
                if isinstance(try_.pattern, Failure):
                    return Failure[TT](value=try_.pattern.value)
                else:
                    return Success[TT](value=functor(try_.pattern.value))

            return self.transform(functor=fold)(ec)

        return with_context

    def flatmap(self, functor: Callable[[T], Future[TT]]) -> Callable[..., Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            def fold(try_: Try[T]) -> Future[TT]:
                if isinstance(try_.pattern, Failure):
                    future = Future[TT]()
                    future.set_exception(exception=try_.pattern.value)
                    return future
                else:
                    return functor(try_.pattern.value)

            return self.transform_with(functor=fold)(ec)

        return with_context

    def transform(
        self, functor: Callable[[Try[T]], Try[TT]]
    ) -> Callable[..., Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            future = Future[TT]()
            self.on_complete(
                functor=lambda result: future.try_complete(result=functor(result))
            )(ec)
            return future

        return with_context

    def transform_with(
        self, functor: Callable[[Try[T]], Future[TT]]
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

    def try_complete(self, result: Try[T]) -> bool:
        if self.done():
            return False
        elif self._state is PENDING:
            try_ = result
            if isinstance(try_.pattern, Failure):
                self.set_exception(exception=try_.pattern.value)
            else:
                self.set_result(result=result.value)
            return True
        else:

            def callback(self: Future[T]):
                if isinstance(result, Failure):
                    self._result = None
                    self._exception = result.value
                else:
                    self._result = result.value
                    self._exception = None

            self.add_done_callback(fn=callback)
            return True

    def on_complete(
        self,
        functor: Callable[[Try[T]], U],
    ) -> Callable[..., None]:
        def with_context(ec: Type[ExecutionContext], /) -> None:
            if self.done():

                def callback(self: Future[T]) -> None:
                    try:
                        # FIXME: Threaded processing
                        result = self.result()
                        self._result = functor(Success(value=result))
                        self._exception = None
                    except Exception as error:
                        self._result = functor(Failure(value=error))
                        self._exception = None

                self.add_done_callback(fn=callback)

        return with_context

    @staticmethod
    def successful(value: T) -> Future[T]:
        future = Future[T]()
        future.set_result(result=value)
        return future

    @property
    def value(self) -> Try[T]:
        try:
            return Success[T](value=self.result())
        except Exception as failure:
            return Failure[T](value=failure)

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
                    return Future[T].successful(value=functor(*args, **kwargs))
                except Exception as error:
                    future = Future[T]()
                    future.set_exception(exception=error)
                    return future

            return with_context

        return wrapper

    @staticmethod
    def do(generator_function: Callable[..., FutureDo[T]]) -> Callable[..., Future[T]]:
        def impl(*args: Any, **kwargs: Any) -> Future[T]:
            def recur(
                generator: FutureDo[T],
                prev: Union[Any, Try[Any]],
            ) -> Future[T]:
                try:
                    result: Union[Any, Try[T]] = generator.send(prev)
                # Success case
                except StopIteration as last:
                    return Future[T].successful(value=last.value)
                # Failure case
                if isinstance(result, Failure):
                    future = Future[T]()
                    future.set_exception(exception=result.value)
                    return future
                return recur(generator, result)

            return recur(generator_function(*args, **kwargs), None)

        return impl

    def convert(self, functor: Callable[[Future[T]], TT]) -> TT:
        return functor(self)


FutureDo = Generator[Union[Any, Try[Any]], Union[Any, Try[Any]], T]
