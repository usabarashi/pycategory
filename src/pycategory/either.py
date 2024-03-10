"""Either"""
from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Generator
from typing import (
    Any,
    Callable,
    Generic,
    Literal,
    ParamSpec,
    TypeAlias,
    TypeVar,
    cast,
)

from . import constraints, extension, extractor, monad, option, try_

R = TypeVar("R")
Lp = TypeVar("Lp", covariant=True)
Rp = TypeVar("Rp", covariant=True)
LLp = TypeVar("LLp", covariant=True)
RRp = TypeVar("RRp", covariant=True)
U = TypeVar("U")
P = ParamSpec("P")


class Either(ABC, Generic[Lp, Rp], monad.Monad[Rp], extension.Extension):
    """Either"""

    @abstractmethod
    def __iter__(self) -> Generator[Either[Lp, Rp], None, Rp]:
        raise NotImplementedError()

    @abstractmethod
    def map(self, func: Callable[[Rp], RRp], /) -> Either[Lp, RRp]:
        raise NotImplementedError()

    @staticmethod
    def pure(value: R) -> Either[Lp, R]:
        return Right[Lp, R](value)

    @abstractmethod
    def flat_map(self, func: Callable[[Rp], Either[Lp, RRp]], /) -> Either[Lp, RRp]:  # type: ignore
        """

        type: ignore
            Cannot interpret partial application of type constructor
        """
        raise NotImplementedError

    @abstractproperty
    def to_option(self) -> option.Option[Rp]:
        raise NotImplementedError()

    @abstractmethod
    def to_try(self, evidence: constraints.SubtypeConstraints[Lp, Exception], /) -> try_.Try[Rp]:
        raise NotImplementedError()

    @abstractmethod
    def fold(self, *, left: Callable[[Lp], U], right: Callable[[Rp], U]) -> U:
        raise NotImplementedError()

    @abstractmethod
    def left(self) -> LeftProjection[Lp, Rp]:
        raise NotImplementedError()

    @abstractmethod
    def right(self) -> RightProjection[Lp, Rp]:
        raise NotImplementedError()

    @abstractmethod
    def is_left(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_right(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> Rp:
        raise NotImplementedError()

    @abstractmethod
    def get_or_else(self, default: Callable[..., LLp], /) -> LLp | Rp:
        raise NotImplementedError()

    @abstractproperty
    def pattern(self) -> SubType[Lp, Rp]:
        raise NotImplementedError()

    @staticmethod
    def do(  # type: ignore
        context: Callable[P, Generator[Either[Lp, Any], None, Rp]], /
    ) -> Callable[P, Either[Lp, Rp]]:
        """map, flat_map combination syntax sugar."""
        return cast(Callable[P, Either[Lp, Rp]], monad.Monad.do(context))


class Left(Either[Lp, Rp], extractor.Extractor):
    """Left"""

    __match_args__ = ("value",)

    def __init__(self, value: Lp, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other: Either[Lp, Rp]) -> bool:  # type: ignore
        match other.pattern:
            case Left(value):
                return self.value == value
            case Right():
                return False

    def __iter__(self) -> Generator[Either[Lp, Rp], None, Rp]:
        raise monad.ShortCircuit(self)

    def map(self, _: Callable[[Rp], RRp], /) -> Either[Lp, RRp]:
        return cast(Left[Lp, RRp], self)

    def flat_map(self, _: Callable[[Rp], Either[Lp, RRp]], /) -> Either[Lp, RRp]:
        return cast(Left[Lp, RRp], self)

    @property
    def to_option(self) -> option.Option[Rp]:
        return option.VOID

    def to_try(self, evidence: constraints.SubtypeConstraints[Lp, Exception], /) -> try_.Try[Rp]:
        return try_.Failure[Rp](cast(Exception, self.value))

    def fold(self, *, left: Callable[[Lp], U], right: Callable[[Rp], U]) -> U:
        return left(self.value)

    def left(self) -> LeftProjection[Lp, Rp]:
        return LeftProjection[Lp, Rp](either=self)

    def right(self) -> RightProjection[Lp, Rp]:
        return RightProjection[Lp, Rp](either=self)

    def is_left(self) -> Literal[True]:
        return True

    def is_right(self) -> Literal[False]:
        return False

    def get(self) -> Rp:
        raise ValueError(self.value)

    def get_or_else(self, default: Callable[..., LLp], /) -> LLp:
        return default()

    @property
    def pattern(self) -> SubType[Lp, Rp]:
        return self


class Right(Either[Lp, Rp], extractor.Extractor):
    """Right"""

    __match_args__ = ("value",)

    def __init__(self, value: Rp, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other: Either[Lp, Rp]) -> bool:  # type: ignore
        match other.pattern:
            case Left():
                return False
            case Right(value):
                return self.value == value

    def __iter__(self) -> Generator[Either[Lp, Rp], None, Rp]:
        yield self
        return self.value

    def map(self, func: Callable[[Rp], RRp], /) -> Either[Lp, RRp]:
        return Right[Lp, RRp](func(self.value))

    def flat_map(self, func: Callable[[Rp], Either[Lp, RRp]], /) -> Either[Lp, RRp]:
        return func(self.value)

    @property
    def to_option(self) -> option.Option[Rp]:
        return option.Some[Rp](self.value)

    def to_try(self, evidence: constraints.SubtypeConstraints[Lp, Exception], /) -> try_.Try[Rp]:
        return try_.Success[Rp](self.value)

    def fold(self, *, left: Callable[[Lp], U], right: Callable[[Rp], U]) -> U:
        return right(self.value)

    def left(self) -> LeftProjection[Lp, Rp]:
        return LeftProjection[Lp, Rp](either=self)

    def right(self) -> RightProjection[Lp, Rp]:
        return RightProjection[Lp, Rp](either=self)

    def is_left(self) -> Literal[False]:
        return False

    def is_right(self) -> Literal[True]:
        return True

    def get(self) -> Rp:
        return self.value

    def get_or_else(self, default: Callable[..., Any], /) -> Rp:
        return self.value

    @property
    def pattern(self) -> SubType[Lp, Rp]:
        return self


class LeftProjection(Generic[Lp, Rp], extension.Extension):
    """LeftProjection"""

    __match_args__ = ("either",)

    def __init__(self, either: SubType[Lp, Rp]):
        self._either = either

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._either})"

    def get(self) -> Lp:
        match self._either:
            case Left() as left:
                return left.value
            case _:
                raise ValueError(self)

    def get_or_else(self, default: Callable[..., RRp], /) -> Lp | RRp:
        match self._either:
            case Left() as left:
                return left.value
            case _:
                return default()

    def map(self, func: Callable[[Lp], LLp], /) -> Either[LLp, Rp]:
        match self._either:
            case Left() as left:
                return Left[LLp, Rp](func(left.value))
            case Right() as right:
                return cast(Right[LLp, Rp], right)

    def flat_map(self, func: Callable[[Lp], Either[LLp, Rp]], /) -> Either[LLp, Rp]:
        match self._either:
            case Left() as left:
                return func(left.value)
            case Right() as right:
                return cast(Right[LLp, Rp], right)


class RightProjection(Generic[Lp, Rp], extension.Extension):
    """RightProjection"""

    __match_args__ = ("either",)

    def __init__(self, either: SubType[Lp, Rp]):
        self._either = either

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._either})"

    def get(self) -> Rp:
        match self._either:
            case Left():
                raise ValueError(self)
            case Right() as right:
                return right.get()

    def get_or_else(self, default: Callable[..., LLp], /) -> LLp | Rp:
        match self._either:
            case Left():
                return default()
            case Right() as right:
                return right.get()

    def map(self, func: Callable[[Rp], RRp], /) -> Either[Lp, RRp]:
        match self._either:
            case Left() as left:
                return cast(Left[Lp, RRp], left)
            case Right() as right:
                return Right[Lp, RRp](func(right.get()))

    def flat_map(self, func: Callable[[Rp], Either[Lp, RRp]], /) -> Either[Lp, RRp]:
        match self._either:
            case Left() as left:
                return cast(Left[Lp, RRp], left)
            case Right() as right:
                return func(right.get())


SubType: TypeAlias = Left[Lp, Rp] | Right[Lp, Rp]
EitherDo: TypeAlias = Generator[Either[Lp, Any], None, Rp]
