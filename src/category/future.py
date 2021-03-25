"""Future"""

from __future__ import annotations

import asyncio
import concurrent.futures
import dataclasses
from abc import ABC
from typing import Callable, Type, TypeVar

from category.try_ import Failure, Success, TryST

T = TypeVar("T")
S = TypeVar("S")
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

    def map(self, functor: Callable[[T], S], ec: Type[ExecutionContext]) -> Future[S]:
        def fold(try_: TryST[T]) -> TryST[S]:
            if isinstance(try_, Failure):
                return Failure[S](value=try_.value)
            else:
                return Success[S](value=functor(try_.value))

        return self.transform(functor=fold, ec=ec)

    def flatmap(
        self, functor: Callable[[T], Future[S]], ec: Type[ExecutionContext]
    ) -> Future[S]:
        def fold(try_: TryST[T]) -> Future[S]:
            if isinstance(try_, Failure):
                return self
            else:
                return functor(try_.value)

        return self.transform_with(functor=fold, ec=ec)

    def transform(
        self, functor: Callable[[TryST[T]], TryST[S]], ec: Type[ExecutionContext]
    ) -> Future[S]:
        future = Future[S]()
        self.on_complete(
            functor=lambda result: future.try_complete(result=functor(result)), ec=ec
        )
        return future

    def transform_with(
        self, functor: Callable[[TryST[T]], Future[S]], ec: Type[ExecutionContext]
    ) -> Future[S]:
        next_future = Future[S]()

        def complete(current_result: TryST[T]) -> None:
            current_future = functor(current_result)
            return current_future.on_complete(
                lambda next_result: next_future.try_complete(next_result),
                ec=ec,
            )

        self.on_complete(complete, ec=ec)
        return next_future

    def try_complete(self, result: TryST[T]) -> bool:
        if self.done():
            return False
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
        functor: Callable[[TryST[T]], U],
        ec: Type[ExecutionContext],
    ) -> None:
        if self.done():
            try:
                result = self.result()
                awaitable = ec.loop.run_in_executor(
                    ec.executor(), functor, Success(result)
                )
                self._result = ec.loop.run_until_complete(awaitable)
            except Exception as error:
                awaitable = ec.loop.run_in_executor(
                    ec.executor(), functor, Failure(value=error)
                )
                self._result = ec.loop.run_until_complete(awaitable)
        else:

            def callback(self: Future[T]) -> None:
                try:
                    result = self.result()
                    self._result = functor(Success(value=result))
                except Exception as error:
                    self._result = functor(Failure(value=error))

            self.add_done_callback(fn=callback)

    @staticmethod
    def successful(value: T) -> Future[T]:
        future = Future[T]()
        future.set_result(result=value)
        return future

    @property
    def value(self) -> TryST[T]:
        try:
            return Success(value=self.result())
        except Exception as failure:
            return Failure(value=failure)
