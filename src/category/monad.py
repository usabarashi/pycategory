from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod
from typing import Any, Callable, Generator, Generic, Literal, TypeVar, Union

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class Monad(ABC, Generic[T]):
    """Monad"""

    value: T

    @abstractmethod
    def __bool__(self) -> bool:
        raise NotImplementedError

    def __call__(self):
        if not bool(self):
            return self
        return self.value


# Try/Failure/Success
S = TypeVar("S")


@dataclasses.dataclass(frozen=True)
class Try(Monad, ABC, Generic[T]):
    """Try"""

    value: Union[Exception, T]

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
        def wrapper(*args: Any, **kwargs: Any) -> Union[Failure[Exception], Success[T]]:
            try:
                return Success(value=fuction(*args, **kwargs))
            except Exception as error:
                return Failure(value=error)

        return wrapper

    @staticmethod
    def do(
        generator_fuction: Callable[..., Generator[Any, Any, T]]
    ) -> Callable[..., Try[T]]:
        def impl(*args: Any, **kwargs: Any) -> Union[Failure, Success[T]]:
            def recur(generator: Generator, prev: Any):
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    return Success(value=last.value)
                # Failure case
                if isinstance(result, Failure):
                    return result
                # Success case
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


@dataclasses.dataclass(frozen=True)
class Failure(Try, Generic[T]):
    """Failure"""

    value: Exception

    def __bool__(self) -> Literal[False]:
        return False

    def is_success(self) -> Literal[False]:
        return False

    def is_failure(self) -> Literal[True]:
        return True

    def fold(
        self,
        failure: Callable[[Exception], Exception],
        success: Callable[[T], S],
    ) -> Try[S]:
        return Failure(failure(self.value))


@dataclasses.dataclass(frozen=True)
class Success(Try, Generic[T]):
    """Success"""

    value: T

    def __bool__(self) -> Literal[True]:
        return True

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


# Either/Left/Right
L = TypeVar("L")
R = TypeVar("R")
LD = TypeVar("LD")
RD = TypeVar("RD")


@dataclasses.dataclass(frozen=True)
class Either(Monad, ABC, Generic[L, R]):
    """
    Left: Irregular case
    Right: Regular case
    """

    value: Union[L, R]

    @abstractmethod
    def is_left(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_right(self) -> bool:
        raise NotADirectoryError

    @abstractmethod
    def fold(self, left=Callable[[L], LD], right=Callable[[R], RD]):
        raise NotImplementedError

    @staticmethod
    def do(
        generator_fuction: Callable[..., Generator[Either[L, R], Any, R]]
    ) -> Callable[..., Either[L, R]]:
        def wrapper(*args, **kwargs):
            def recur(generator: Generator, prev: Any):
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    return Right(last.value)
                # Irregular case
                if isinstance(result, Left):
                    return result
                # Regura case
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return wrapper


@dataclasses.dataclass(frozen=True)
class Left(Either[L, R]):
    """Left"""

    value: L

    def __bool__(self) -> Literal[False]:
        return False

    def is_left(self) -> Literal[True]:
        return True

    def is_right(self) -> Literal[False]:
        return False

    def fold(self, left=Callable[[L], LD], right=Callable[[R], RD]) -> Either[Any, Any]:
        return Left[LD, RD](value=left(self.value))


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

    def fold(self, left=Callable[[L], LD], right=Callable[[R], RD]) -> Either[Any, Any]:
        return Right[LD, RD](right(self.value))