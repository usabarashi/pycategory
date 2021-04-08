from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Callable, Generator, Generic, Literal, Optional, TypeVar, Union

L = TypeVar("L")
R = TypeVar("R")
LL = TypeVar("LL")
RR = TypeVar("RR")
TT = TypeVar("TT")
EE = TypeVar("EE")


class Either(ABC, Generic[L, R]):
    """Either"""

    value: Union[L, R]

    @abstractmethod
    def __call__(
        self, /, convert: Optional[Callable[[Either[L, R]], EE]] = None
    ) -> Generator[Union[EE, Either[L, R]], None, R]:
        raise NotImplementedError

    @abstractmethod
    def map(self, functor: Callable[[R], RR]) -> Either[L, RR]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, functor: Callable[[R], Either[L, RR]]) -> Either[L, RR]:
        raise NotImplementedError

    @abstractmethod
    def fold(self, /, left: Callable[[L], TT], right: Callable[[R], TT]) -> TT:
        raise NotImplementedError

    @abstractmethod
    def left(self) -> LeftProjection[L, R]:
        raise NotImplementedError

    @abstractmethod
    def right(self) -> RightProjection[L, R]:
        raise NotImplementedError

    @abstractmethod
    def is_left(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_right(self) -> bool:
        raise NotImplementedError

    @abstractproperty
    def pattern(self) -> SubType[L, R]:
        raise NotImplementedError

    @staticmethod
    def do(
        generator_fuction: Callable[..., EitherGenerator[L, R]]
    ) -> Callable[..., Either[L, R]]:
        def wrapper(*args: Any, **kwargs: Any) -> Either[L, R]:
            def recur(
                generator: EitherGenerator[L, R],
                prev: Any,
            ) -> Either[L, R]:
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    return Right(value=last.value)
                if isinstance(result, Left):
                    return result
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return wrapper

    @abstractmethod
    def convert(self, functor: Callable[[Either[L, R]], TT]) -> TT:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class Left(Either[L, R]):
    """Left"""

    value: L

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(
        self, /, convert: Optional[Callable[[Either[L, R]], EE]] = None
    ) -> Generator[Union[EE, Left[L, R]], None, R]:
        if convert is not None:
            yield convert(self)
            raise GeneratorExit(self)
        else:
            yield self
            raise GeneratorExit(self)

    def map(self, functor: Callable[[R], RR]) -> Either[L, RR]:
        return Left[L, RR](self.value)

    def flatmap(self, functor: Callable[[R], Either[L, RR]]) -> Either[L, RR]:
        return Left[L, RR](value=self.value)

    def fold(self, /, left: Callable[[L], TT], right: Callable[[R], TT]) -> TT:
        return left(self.value)

    def left(self) -> LeftProjection[L, R]:
        return LeftProjection[L, R](either=self)

    def right(self) -> RightProjection[L, R]:
        return RightProjection[L, R](either=self)

    def is_left(self) -> Literal[True]:
        return True

    def is_right(self) -> Literal[False]:
        return False

    @property
    def pattern(self) -> SubType[L, R]:
        return self

    def convert(self, functor: Callable[[Left[L, R]], TT]) -> TT:
        return functor(self)


@dataclasses.dataclass(frozen=True)
class Right(Either[L, R]):
    """Right"""

    value: R

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(
        self, convert: Optional[Callable[[Either[L, R]], EE]] = None
    ) -> Generator[Union[EE, Right[L, R]], None, R]:
        if convert is not None:
            yield convert(self)
            raise GeneratorExit(self)
        else:
            yield self
            return self.value

    def map(self, functor: Callable[[R], RR]) -> Either[L, RR]:
        return Right[L, RR](functor(self.value))

    def flatmap(self, functor: Callable[[R], Either[L, RR]]) -> Either[L, RR]:
        return functor(self.value)

    def fold(self, /, left: Callable[[L], TT], right: Callable[[R], TT]) -> TT:
        return right(self.value)

    def left(self) -> LeftProjection[L, R]:
        return LeftProjection[L, R](either=self)

    def right(self) -> RightProjection[L, R]:
        return RightProjection[L, R](either=self)

    def is_left(self) -> Literal[False]:
        return False

    def is_right(self) -> Literal[True]:
        return True

    @property
    def pattern(self) -> SubType[L, R]:
        return self

    def convert(self, functor: Callable[[Right[L, R]], TT]) -> TT:
        return functor(self)


@dataclasses.dataclass(frozen=True)
class LeftProjection(Generic[L, R]):
    """LeftProjection"""

    either: SubType[L, R]

    def __bool__(self) -> bool:
        return bool(self.either)

    def get(self) -> L:
        if isinstance(self.either, Left):
            return self.either.value
        else:
            raise ValueError(self)

    def get_or_else(self, default: Callable[..., RR]) -> Union[L, RR]:
        if isinstance(self.either, Left):
            return self.either.value
        else:
            return default()

    def map(self, functor: Callable[[L], LL]) -> Either[LL, R]:
        if isinstance(self.either, Left):
            return Left[LL, R](value=functor(self.either.value))
        else:
            return Right[LL, R](value=self.either.value)

    def flatmap(self, functor: Callable[[L], Either[LL, R]]) -> Either[LL, R]:
        if isinstance(self.either, Left):
            return functor(self.either.value)
        else:
            return Right[LL, R](value=self.either.value)


@dataclasses.dataclass(frozen=True)
class RightProjection(Generic[L, R]):
    """RightProjection"""

    either: SubType[L, R]

    def __bool__(self) -> bool:
        return bool(self.either)

    def get(self) -> R:
        if isinstance(self.either, Left):
            raise ValueError(self)
        else:
            return self.either.value

    def get_or_else(self, default: Callable[..., LL]) -> Union[LL, R]:
        if isinstance(self.either, Left):
            return default()
        else:
            return self.either.value

    def map(self, functor: Callable[[R], RR]) -> Either[L, RR]:
        if isinstance(self.either, Left):
            return Left[L, RR](value=self.either.value)
        else:
            return Right[L, RR](value=functor(self.either.value))

    def flatmap(self, functor: Callable[[R], Either[L, RR]]) -> Either[L, RR]:
        if isinstance(self.either, Left):
            return Left[L, RR](value=self.either.value)
        else:
            return functor(self.either.value)


SubType = Union[Left[L, R], Right[L, R]]
EitherDo = Generator[Union[Either[L, Any], Any], Any, R]
EitherGenerator = Generator[
    Union[Either[L, Any], Any],
    Union[Either[L, Any], Any],
    R,
]
