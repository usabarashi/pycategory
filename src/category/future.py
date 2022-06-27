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

from category import monad, try_

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


class Future(monad.Monad, concurrent.futures.Future[T]):
    """Future"""

    def __init__(self) -> None:
        super().__init__()

    def unapply(self) -> tuple[()] | tuple[Any]:
        return (self.result(),)

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
    def lift(*args: ..., **kwargs: ...) -> Future[T]:
        return Future.successful(*args, **kwargs)

    def map(
        self, functor: Callable[[T], TT], /
    ) -> Callable[[Type[ExecutionContext]], Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            def fold(try__: try_.Try[T], /) -> try_.Try[TT]:
                match try__.pattern:
                    case try_.Failure() as failure:
                        return try_.Failure[TT](failure.exception)
                    case try_.Success(value):
                        return try_.Success[TT](functor(value))

            return self.transform(fold)(ec)

        return with_context

    def flatmap(
        self, functor: Callable[[T], Future[TT]], /
    ) -> Callable[[Type[ExecutionContext]], Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            def fold(try__: try_.Try[T]) -> Future[TT]:
                match try__.pattern:
                    case try_.Failure() as failure:
                        future = Future[TT]()
                        future.set_exception(exception=failure.exception)
                        return future
                    case try_.Success(value):
                        try:
                            return functor(value)
                        except Exception as error:
                            future = Future[TT]()
                            future.set_exception(exception=error)
                            return future

            return self.transform_with(fold)(ec)

        return with_context

    def transform(
        self, functor: Callable[[try_.Try[T]], try_.Try[TT]], /
    ) -> Callable[[Type[ExecutionContext]], Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            future = Future[TT]()
            self.on_complete(lambda result: future.try_complete(functor(result)))(ec)
            return future

        return with_context

    def transform_with(
        self, functor: Callable[[try_.Try[T]], Future[TT]], /
    ) -> Callable[[Type[ExecutionContext]], Future[TT]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[TT]:
            next_future = Future[TT]()

            def complete(current_result: try_.Try[T]) -> None:
                current_future = functor(current_result)
                return current_future.on_complete(
                    lambda next_result: next_future.try_complete(next_result),
                )(ec)

            self.on_complete(complete)(ec)
            return next_future

        return with_context

    def try_complete(self, result: try_.Try[T], /) -> bool:
        if self.done():
            return False
        elif self._state is PENDING:
            match result.pattern:
                case try_.Failure() as failure:
                    self.set_exception(exception=failure.exception)
                case try_.Success(value):
                    self.set_result(result=value)
            return True
        else:

            def callback(self: Future[T]):
                match result.pattern:
                    case try_.Failure() as failure:
                        self._result = None
                        self._exception = failure.exception
                    case try_.Success(value):
                        self._result = value
                        self._exceptoin = None

            self.add_done_callback(fn=callback)
            return True

    def on_complete(
        self, functor: Callable[[try_.Try[T]], U], /
    ) -> Callable[[Type[ExecutionContext]], None]:
        def with_context(ec: Type[ExecutionContext], /) -> None:
            if self.done():

                def callback(self: Future[T]) -> None:
                    try:
                        # FIXME: Threaded processing
                        result = self.result()
                        self._result = functor(try_.Success(result))
                        self._exception = None
                    except Exception as error:
                        self._result = functor(try_.Failure(error))
                        self._exception = None

                self.add_done_callback(fn=callback)

        return with_context

    @staticmethod
    def successful(value: T, /) -> Future[T]:
        future = Future[T]()
        future.set_result(result=value)
        return future

    @property
    def value(self) -> try_.Try[T]:
        try:
            return try_.Success[T](self.result())
        except Exception as failure:
            return try_.Failure[T](failure)

    @staticmethod
    def do(context: Callable[P, FutureDo[T]], /) -> Callable[P, Future[T]]:
        """map, flatmap combination syntax sugar.

        Only type checking can determine type violations, and runtime errors may not occur.
        """

        @wraps(context)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Future[T]:
            context_ = context(*args, **kwargs)
            try:
                while True:
                    yield_state = next(context_)
                    if not isinstance(yield_state, Future):
                        raise TypeError(yield_state)
                    match yield_state.composability():
                        case monad.Composability.IMPOSSIBLE:
                            return yield_state
                        case monad.Composability.POSSIBLE:
                            # Priority is given to the value of the sub-generator's monad.
                            ...
                        case _:
                            raise TypeError(yield_state)
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


FutureDo: TypeAlias = Generator[Future[Any], None, T]
