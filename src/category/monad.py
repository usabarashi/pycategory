"""Monad
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import dataclasses
import inspect
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Generator, Generic, Literal, TypeVar, Union

T = TypeVar("T")


class Monad(ABC):
    """Monad"""

    value: Any

    @abstractmethod
    def __bool__(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __call__(self) -> Generator[Monad, None, Any]:
        raise NotImplementedError


class Frame:
    def __init__(self, depth: int = 2):
        self.filename: str = inspect.stack()[depth].filename
        self.line: int = inspect.stack()[depth].frame.f_lineno
        self.function: str = inspect.stack()[depth].function
        self.args: dict[str, Any] = inspect.getargvalues(
            inspect.stack()[depth].frame
        ).locals
        self.stack: list[inspect.FrameInfo] = inspect.stack()


# Either/Left/Right
L = TypeVar("L")
R = TypeVar("R")
LL = TypeVar("LL")
RR = TypeVar("RR")


class Either(Monad, ABC, Generic[L, R]):
    """Either

    Left: Irregular case
    Right: Regular case
    """

    value: Union[L, R]

    def __call__(self) -> Generator[Either[L, R], None, Union[L, R]]:
        yield self
        return self.value

    @abstractmethod
    def is_left(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_right(self) -> bool:
        raise NotADirectoryError

    @abstractmethod
    def fold(self, left: Callable[[L], LL], right: Callable[[R], RR]) -> Either[LL, RR]:
        raise NotImplementedError

    @staticmethod
    def do(
        generator_fuction: Callable[..., Generator[Either[L, R], Any, R]]
    ) -> Callable[..., Either[L, R]]:
        def wrapper(*args: Any, **kwargs: Any) -> Either[L, R]:
            def recur(
                generator: Generator[Union[Left[L, R], Any], Union[Left[L, R], Any], R],
                prev: Any,
            ) -> Either[L, R]:
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    # Regura case
                    return Right(last.value)
                if Left is type(result):
                    # Irregular case
                    return result
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return wrapper


@dataclasses.dataclass(frozen=True)
class Left(Either[L, R]):
    """Left"""

    value: L
    frame: Frame = dataclasses.field(default_factory=Frame)

    def __bool__(self) -> Literal[False]:
        return False

    def is_left(self) -> Literal[True]:
        return True

    def is_right(self) -> Literal[False]:
        return False

    def fold(self, left: Callable[[L], LL], right: Callable[[R], RR]) -> Either[LL, RR]:
        return Left[LL, RR](value=left(self.value))


@dataclasses.dataclass(frozen=True)
class Right(Either[L, R]):
    """Right"""

    value: R

    def __bool__(self) -> Literal[True]:
        return True

    def is_left(self) -> Literal[False]:
        return False

    def is_right(self) -> Literal[True]:
        return True

    def fold(self, left: Callable[[L], LL], right: Callable[[R], RR]) -> Either[LL, RR]:
        return Right[LL, RR](right(self.value))


# Try/Failure/Success
S = TypeVar("S")


class Try(Monad, Generic[T]):
    """Try

    試行型
    """

    value: Union[Exception, T]

    @abstractmethod
    def __call__(self) -> Generator[Try[T], None, Union[Exception, T]]:
        raise NotImplementedError

    @abstractmethod
    def is_failure(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_success(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def fold(
        self,
        failure: Callable[[Exception], Exception],
        success: Callable[[T], S],
    ) -> Try[S]:
        raise NotImplementedError

    @staticmethod
    def hold(fuction: Callable[..., T]) -> Callable[..., Try[T]]:
        def wrapper(*args: Any, **kwargs: Any) -> Try[T]:
            try:
                return Success(value=fuction(*args, **kwargs))
            except Exception as error:
                return Failure[T](value=error)

        return wrapper

    @staticmethod
    def do(
        generator_fuction: Callable[..., Generator[Any, Any, T]]
    ) -> Callable[..., Try[T]]:
        def impl(*args: Any, **kwargs: Any) -> Try[T]:
            def recur(
                generator: Generator[Union[Failure[T], Any], Union[Failure[T], Any], T],
                prev: Any,
            ) -> Try[T]:
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    # Success case
                    return Success(value=last.value)
                # Failure case
                if Failure is type(result):
                    return result
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


@dataclasses.dataclass(frozen=True)
class Failure(Try[T]):
    """Failure"""

    value: Exception

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(self) -> Generator[Failure[T], None, Exception]:
        yield self
        return self.value

    def is_success(self) -> Literal[False]:
        return False

    def is_failure(self) -> Literal[True]:
        return True

    def fold(
        self,
        failure: Callable[[Exception], Exception],
        success: Callable[[T], S],
    ) -> Try[S]:
        return Failure[S](failure(self.value))


@dataclasses.dataclass(frozen=True)
class Success(Try[T]):
    """Success"""

    value: T

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(self) -> Generator[Success[T], None, T]:
        yield self
        return self.value

    def is_failure(self) -> Literal[False]:
        return False

    def is_success(self) -> Literal[True]:
        return True

    def fold(
        self,
        failure: Callable[[Exception], Exception],
        success: Callable[[T], S],
    ) -> Try[S]:
        return Success(success(self.value))


# Future
@dataclasses.dataclass(frozen=True)
class Future(Monad, Generic[T]):

    value: Awaitable[T]
    loop: asyncio.AbstractEventLoop

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(self) -> Generator[Try[T], None, Union[Exception, T]]:
        try:
            success = self.loop.run_until_complete(future=self.value)
            yield Success(value=success)
            return success
        except Exception as error:
            yield Failure(value=error)
            return error

    def on_complete(self) -> Try[T]:
        try:
            return Success(value=self.loop.run_until_complete(future=self.value))
        except Exception as error:
            return Failure[T](value=error)

    @staticmethod
    def hold(function: Callable[..., T]):
        def wrapper(*args: Any, **kwargs: Any):
            def context(
                *,
                loop: asyncio.AbstractEventLoop,
                executor: Union[
                    concurrent.futures.ProcessPoolExecutor,
                    concurrent.futures.ThreadPoolExecutor,
                ],
            ) -> Future[T]:
                return Future(
                    value=loop.run_in_executor(executor, function, *args),
                    loop=loop,
                )

            return context

        return wrapper

    @staticmethod
    def do(fuction: Callable[..., Generator[Any, Any, T]]):
        def wrapper(*args: Any, **kwargs: Any):
            def context(
                *,
                loop: asyncio.AbstractEventLoop,
                executor: Union[
                    concurrent.futures.ProcessPoolExecutor,
                    concurrent.futures.ThreadPoolExecutor,
                ],
            ):
                kwargs.update({"loop": loop, "executor": executor})

                def recur(
                    generator: Generator[
                        Union[Failure[T], Any], Union[Failure[T], Any], T
                    ],
                    prev: Any,
                ) -> Future[T]:
                    try:
                        result = generator.send(prev)
                    except StopIteration as last:
                        # Success case
                        def success(stop_iteration: StopIteration) -> T:
                            return stop_iteration.value

                        return Future(
                            value=loop.run_in_executor(executor, success, last),
                            loop=loop,
                        )
                    # Failure case
                    if Failure is type(result):

                        def failure(exception: Exception) -> T:
                            raise exception

                        return Future(
                            value=loop.run_in_executor(executor, failure, result.value),
                            loop=loop,
                        )
                    return recur(generator, result)

                return recur(fuction(*args, **kwargs), None)

            return context

        return wrapper
