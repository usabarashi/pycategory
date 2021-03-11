from __future__ import annotations

import asyncio
import concurrent.futures
import dataclasses
from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Optional, TypeVar, Union

from category.collection import Vector
from category.try_ import Failure, Success, TryST

T = TypeVar("T")
S = TypeVar("S")
U = TypeVar("U")


class ExecutionContext(ABC):
    """ExecutionContext"""

    @abstractmethod
    def execute(self, runnable: Runnable) -> Any:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class ThreadPoolExecutionContext(ExecutionContext):
    """ThreadPoolExecutionContext"""

    loop: asyncio.AbstractEventLoop

    def execute(self, runnable: Runnable) -> None:
        if runnable.try_ is not None:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                awaitable = self.loop.run_in_executor(
                    executor, runnable.functor, runnable.try_
                )
                result = self.loop.run_until_complete(future=awaitable)
                return result
        raise EOFError


class Promise(ABC, Generic[T]):
    """Promise"""

    @property
    def future(self) -> Future[T]:
        raise NotImplementedError

    @abstractmethod
    def try_complete(
        self,
        result: TryST[T],
    ) -> bool:
        """try_comple

        False: Already set the value.
        True: I was able to set the value.
        """
        raise NotImplementedError


class Runnable(ABC):
    ec: ExecutionContext
    functor: Callable[[TryST[Any]], Any]
    try_: Optional[TryST[Any]]

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError


@dataclasses.dataclass
class RunnableWithValue(Runnable, Generic[T, U]):
    """RunnableWithValue"""

    ec: ExecutionContext
    functor: Callable[[TryST[T]], U]
    try_: Optional[TryST[T]] = None

    def run(self) -> None:
        if self.try_ is None:
            raise NotImplementedError("value must be set")
        else:
            self.functor(self.try_)

    def execute(self) -> None:
        self.ec.execute(self)


class PromiseContent(Generic[T]):
    pass


@dataclasses.dataclass
class Result(PromiseContent[T]):
    """Result"""

    value: T


@dataclasses.dataclass
class Listeners(PromiseContent[T]):
    """Listeners"""

    runnables: Vector[RunnableWithValue[T, Any]] = dataclasses.field(
        default_factory=Vector
    )


@dataclasses.dataclass
class Future(Promise[T]):
    name: str
    listeners_or_result: Union[Listeners[T], Result[TryST[T]]] = dataclasses.field(
        default_factory=Listeners
    )

    def map(
        self, functor: Callable[[T], S], ec: ExecutionContext, name: str
    ) -> Future[S]:
        def fold(try_: TryST[T]) -> TryST[S]:
            if isinstance(try_, Failure):
                return Failure(value=try_.value)
            else:
                return Success(value=functor(try_.value))

        return self.transform(functor=fold, ec=ec, name=name)

    def flatmap(
        self, functor: Callable[[T], Future[S]], ec: ExecutionContext, name: str
    ) -> Future[S]:
        def fold(try_: TryST[T]) -> Future[S]:
            if isinstance(try_, Failure):
                future = Future[S](name=name)
                failure = try_.value
                future.listeners_or_result = Result(value=Failure(value=failure))
                return future
            else:
                return functor(try_.value)

        return self.transform_with(functor=fold, ec=ec, name=name)

    @property
    def future(self) -> Future[T]:
        return self

    def transform(
        self, functor: Callable[[TryST[T]], TryST[S]], ec: ExecutionContext, name: str
    ) -> Future[S]:
        promise = Future[S](name=name)
        self.on_complete(
            functor=lambda result: promise.try_complete(result=functor(result)),
            ec=ec,
            name=name,
        )
        return promise.future

    def transform_with(
        self, functor: Callable[[TryST[T]], Future[S]], ec: ExecutionContext, name: str
    ) -> Future[S]:
        promise = Future[S](name=name)

        def complete(result: TryST[T]) -> None:
            future = functor(result)
            return future.on_complete(
                lambda current_result: promise.try_complete(current_result),
                ec=ec,
                name="from-" + future.name,
            )

        self.on_complete(complete, ec=ec, name="from-" + self.name)
        return promise.future

    def try_complete(self, result: TryST[T]) -> bool:
        """try_comple

        False: Already set the value.
        True: I was able to set the value.
        """
        if isinstance(self.listeners_or_result, Result):
            return False
        else:
            listeners = self.listeners_or_result
            # When an asynchronous side effect occurs
            # if self.listeners_or_result is listeners:
            #    self.listeners_or_result = Result(value=result)
            # else:
            #    self.try_complete(result=result)

            def complete(runnable: RunnableWithValue[T, Any]) -> None:
                if runnable.try_ is not None:
                    runnable.try_ = result
                runnable.execute()

            listeners.runnables.foreach(lambda runnable: complete(runnable=runnable))
            return True

    def on_complete(
        self, functor: Callable[[TryST[T]], U], ec: ExecutionContext, name: str
    ) -> None:
        new_runnable = RunnableWithValue[T, Any](functor=functor, ec=ec)
        if isinstance(self.listeners_or_result, Result):
            if new_runnable.try_ is None:
                result = self.listeners_or_result
                new_runnable.try_ = result.value
            new_runnable.execute()
        else:
            listeners = self.listeners_or_result
            # Stack new task
            if listeners is self.listeners_or_result:
                listeners = Listeners(listeners.runnables.append(new_runnable))
            else:
                self.on_complete(functor=functor, ec=ec, name=name)

    @staticmethod
    def successful(value: T, name: str) -> Future[T]:
        future = Future[T](name=name)
        future.listeners_or_result = Result(value=Success(value=value))
        return future
