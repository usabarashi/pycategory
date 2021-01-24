from __future__ import annotations

import dataclasses
from abc import abstractmethod
from typing import Any, Callable, Generator, Generic, Literal, TypeVar, Union

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class Monad(Generic[T]):
    """Monad"""

    value: T

    @abstractmethod
    def __bool__(self) -> bool:
        raise NotImplementedError

    def __call__(self):
        if not bool(self):
            return self
        return self.value


L = TypeVar("L")
R = TypeVar("R")
LD = TypeVar("LD")
RD = TypeVar("RD")


@dataclasses.dataclass(frozen=True)
class Either(Monad, Generic[L, R]):
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
    def map(self, function=Callable[[R], Any]) -> Either[L, Any]:
        raise NotImplementedError

    @abstractmethod
    def fold(self, left=Callable[[L], Any], right=Callable[[R], Any]):
        raise NotImplementedError

    @staticmethod
    def do(generator_fuction: Callable[..., Generator[Either[L, R]]]) -> Either[L, R]:
        import functools

        @functools.wraps(generator_fuction)
        def impl():
            generator = generator_fuction()

            def recur(generator: Generator, prev: Any):
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    return Right(last.value)
                # Irregular case
                if issubclass(type(result), Either):
                    return result
                # Regura case
                return recur(generator, result)

            return recur(generator, None)

        return impl


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

    def map(self, function=Callable[[L], T]) -> Either[L, T]:
        return Left[L, T](value=self.value)

    def fold(self, left=Callable[[L], LD], right=Callable[[R], RD]) -> Either[LD, RD]:
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

    def map(self, function=Callable[[R], RD]) -> Either[L, RD]:
        return Right(function(value=self.value))

    def fold(self, left=Callable[[L], LD], right=Callable[[R], LD]) -> Either[LD, RD]:
        return Right[LD, RD](right(self.value))
