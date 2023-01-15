"""Either"""
from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Generator
from typing import Callable, Generic, Literal, ParamSpec, TypeAlias, TypeVar, cast

from . import constraints, extension, extractor, monad, option, try_

L = TypeVar("L", covariant=True)
R = TypeVar("R", covariant=True)
LL = TypeVar("LL")
RR = TypeVar("RR")
TT = TypeVar("TT")
U = TypeVar("U")
P = ParamSpec("P")


class Either(ABC, Generic[L, R], monad.Monad[R], extension.Extension):
    """Either"""

    @abstractmethod
    def __iter__(self) -> Generator[Either[L, R], None, R]:
        raise NotImplementedError

    @abstractmethod
    def map(self, func: Callable[[R], RR], /) -> Either[L, RR]:
        raise NotImplementedError

    @staticmethod
    def pure(value: R) -> Either[L, R]:
        return Right[L, R](value)

    @abstractmethod
    def flat_map(self, func: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        raise NotImplementedError

    @abstractproperty
    def to_option(self) -> option.Option[R]:
        raise NotImplementedError

    @abstractmethod
    def to_try(
        self, evidence: constraints.SubtypeConstraints[L, Exception], /
    ) -> try_.Try[R]:
        raise NotImplementedError

    @abstractmethod
    def fold(self, *, left: Callable[[L], U], right: Callable[[R], U]) -> U:
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

    @abstractmethod
    def get(self) -> R:
        raise NotImplementedError

    @abstractmethod
    def get_or_else(self, default: Callable[..., LL], /) -> LL | R:
        raise NotImplementedError

    @abstractproperty
    def pattern(self) -> SubType[L, R]:
        raise NotImplementedError


class Left(Either[L, R], extractor.Extractor):
    """Left"""

    __match_args__ = ("value",)

    def __init__(self, value: L, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other: Either[L, R]) -> bool:
        match other.pattern:
            case Left(value):
                return self.value == value
            case Right():
                return False

    def __iter__(self) -> Generator[Either[L, R], None, R]:
        raise GeneratorExit(self)

    def map(self, _: Callable[[R], RR], /) -> Either[L, RR]:
        return cast(Left[L, RR], self)

    def flat_map(self, _: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        return cast(Left[L, RR], self)

    @property
    def to_option(self) -> option.Option[R]:
        return option.VOID

    def to_try(
        self, evidence: constraints.SubtypeConstraints[L, Exception], /
    ) -> try_.Try[R]:
        return try_.Failure[R](cast(Exception, self.value))

    def fold(self, *, left: Callable[[L], U], right: Callable[[R], U]) -> U:
        return left(self.value)

    def left(self) -> LeftProjection[L, R]:
        return LeftProjection[L, R](either=self)

    def right(self) -> RightProjection[L, R]:
        return RightProjection[L, R](either=self)

    def is_left(self) -> Literal[True]:
        return True

    def is_right(self) -> Literal[False]:
        return False

    def get(self) -> R:
        raise ValueError(self.value)

    def get_or_else(self, default: Callable[..., LL], /) -> LL:
        return default()

    @property
    def pattern(self) -> SubType[L, R]:
        return self


class Right(Either[L, R], extractor.Extractor):
    """Right"""

    __match_args__ = ("value",)

    def __init__(self, value: R, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other: Either[L, R]) -> bool:
        match other.pattern:
            case Left():
                return False
            case Right(value):
                return self.value == value

    def __iter__(self) -> Generator[Either[L, R], None, R]:
        yield self
        return self.value

    def map(self, func: Callable[[R], RR], /) -> Either[L, RR]:
        return Right[L, RR](func(self.value))

    def flat_map(self, func: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        return func(self.value)

    @property
    def to_option(self) -> option.Option[R]:
        return option.Some[R](self.value)

    def to_try(
        self, evidence: constraints.SubtypeConstraints[L, Exception], /
    ) -> try_.Try[R]:
        return try_.Success[R](self.value)

    def fold(self, *, left: Callable[[L], U], right: Callable[[R], U]) -> U:
        return right(self.value)

    def left(self) -> LeftProjection[L, R]:
        return LeftProjection[L, R](either=self)

    def right(self) -> RightProjection[L, R]:
        return RightProjection[L, R](either=self)

    def is_left(self) -> Literal[False]:
        return False

    def is_right(self) -> Literal[True]:
        return True

    def get(self) -> R:
        return self.value

    def get_or_else(self, default: Callable[..., LL], /) -> R:
        return self.value

    @property
    def pattern(self) -> SubType[L, R]:
        return self


class LeftProjection(Generic[L, R], extension.Extension):
    """LeftProjection"""

    __match_args__ = ("either",)

    def __init__(self, either: SubType[L, R]):
        self._either = either

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._either})"

    def get(self) -> L:
        match self._either:
            case Left() as left:
                return left.value
            case _:
                raise ValueError(self)

    def get_or_else(self, default: Callable[..., RR], /) -> L | RR:
        match self._either:
            case Left() as left:
                return left.value
            case _:
                return default()

    def map(self, func: Callable[[L], LL], /) -> Either[LL, R]:
        match self._either:
            case Left() as left:
                return Left[LL, R](func(left.value))
            case Right() as right:
                return cast(Right[LL, R], right)

    def flat_map(self, func: Callable[[L], Either[LL, R]], /) -> Either[LL, R]:
        match self._either:
            case Left() as left:
                return func(left.value)
            case Right() as right:
                return cast(Right[LL, R], right)


class RightProjection(Generic[L, R], extension.Extension):
    """RightProjection"""

    __match_args__ = ("either",)

    def __init__(self, either: SubType[L, R]):
        self._either = either

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._either})"

    def get(self) -> R:
        match self._either:
            case Left():
                raise ValueError(self)
            case Right() as right:
                return right.get()

    def get_or_else(self, default: Callable[..., LL], /) -> LL | R:
        match self._either:
            case Left():
                return default()
            case Right() as right:
                return right.get()

    def map(self, func: Callable[[R], RR], /) -> Either[L, RR]:
        match self._either:
            case Left() as left:
                return cast(Left[L, RR], left)
            case Right() as right:
                return Right[L, RR](func(right.get()))

    def flat_map(self, func: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        match self._either:
            case Left() as left:
                return cast(Left[L, RR], left)
            case Right() as right:
                return func(right.get())


SubType: TypeAlias = Left[L, R] | Right[L, R]
EitherDo: TypeAlias = Generator[Either[L, R], None, R]
