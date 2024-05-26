"""Either"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any, Callable, Final, Literal, cast

from pycategory.data import option, try_
from pycategory.trait import extension, monad
from pycategory.type import constraints, extractor


class Either[L, R](extension.Extension, monad.Monad[R], ABC):
    """Either"""

    @abstractmethod
    def __iter__(self) -> Generator[Either[L, R], None, R]:
        raise NotImplementedError()

    @abstractmethod
    def map[RR](self, func: Callable[[R], RR], /) -> Either[L, RR]:
        raise NotImplementedError()

    @staticmethod
    def pure(value: R) -> Either[L, R]:
        return Right[L, R](value)

    @abstractmethod
    def flat_map[RR](self, func: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:  # type: ignore
        """

        type: ignore
            Cannot interpret partial application of type constructor
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def to_option(self) -> option.Option[R]:
        raise NotImplementedError()

    @abstractmethod
    def to_try(self, evidence: constraints.SubtypeConstraints[L, Exception], /) -> try_.Try[R]:
        raise NotImplementedError()

    @abstractmethod
    def fold[U](self, *, left: Callable[[L], U], right: Callable[[R], U]) -> U:
        raise NotImplementedError()

    @abstractmethod
    def left(self) -> LeftProjection[L, R]:
        raise NotImplementedError()

    @abstractmethod
    def right(self) -> RightProjection[L, R]:
        raise NotImplementedError()

    @abstractmethod
    def is_left(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_right(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> R:
        raise NotImplementedError()

    @abstractmethod
    def get_or_else[LL](self, default: Callable[..., LL], /) -> LL | R:
        raise NotImplementedError()

    @property
    @abstractmethod
    def pattern(self) -> SubType[L, R]:
        raise NotImplementedError()

    @staticmethod
    def do[  # type: ignore
        **P
    ](context: Callable[P, Generator[Either[L, Any], None, R]], /) -> Callable[P, Either[L, R]]:
        """map, flat_map combination syntax sugar."""
        return cast(Callable[P, Either[L, R]], monad.Monad.do(context))


class Left[L, R](Either[L, R], extractor.Extractor):
    """Left"""

    __match_args__ = ("value",)

    def __init__(self, value: L, /):
        self.value: Final = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other: Either[L, R]) -> bool:  # type: ignore
        match other.pattern:
            case Left(value):
                return self.value == value
            case Right():
                return False

    def __iter__(self) -> Generator[Either[L, R], None, R]:
        raise monad.ShortCircuit(self)

    def map[RR](self, _: Callable[[R], RR], /) -> Either[L, RR]:
        return cast(Left[L, RR], self)

    def flat_map[RR](self, _: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        return cast(Left[L, RR], self)

    @property
    def to_option(self) -> option.Option[R]:
        return option.VOID

    def to_try(self, evidence: constraints.SubtypeConstraints[L, Exception], /) -> try_.Try[R]:
        return try_.Failure[R](cast(Exception, self.value))

    def fold[U](self, *, left: Callable[[L], U], right: Callable[[R], U]) -> U:
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

    def get_or_else[LL](self, default: Callable[..., LL], /) -> LL:
        return default()

    @property
    def pattern(self) -> SubType[L, R]:
        return self


class Right[L, R](Either[L, R], extractor.Extractor):
    """Right"""

    __match_args__ = ("value",)

    def __init__(self, value: R, /):
        self.value: Final = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other: Either[L, R]) -> bool:  # type: ignore
        match other.pattern:
            case Left():
                return False
            case Right(value):
                return self.value == value

    def __iter__(self) -> Generator[Either[L, R], None, R]:
        yield self
        return self.value

    def map[RR](self, func: Callable[[R], RR], /) -> Either[L, RR]:
        return Right[L, RR](func(self.value))

    def flat_map[RR](self, func: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        return func(self.value)

    @property
    def to_option(self) -> option.Option[R]:
        return option.Some[R](self.value)

    def to_try(self, evidence: constraints.SubtypeConstraints[L, Exception], /) -> try_.Try[R]:
        return try_.Success[R](self.value)

    def fold[U](self, *, left: Callable[[L], U], right: Callable[[R], U]) -> U:
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

    def get_or_else(self, default: Callable[..., Any], /) -> R:
        return self.value

    @property
    def pattern(self) -> SubType[L, R]:
        return self


class LeftProjection[L, R](extension.Extension):
    """LeftProjection"""

    __match_args__ = ("either",)

    def __init__(self, either: SubType[L, R]):
        self._either: Final = either

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._either})"

    def get(self) -> L:
        match self._either:
            case Left() as left:
                return left.value
            case _:
                raise ValueError(self)

    def get_or_else[RR](self, default: Callable[..., RR], /) -> L | RR:
        match self._either:
            case Left() as left:
                return left.value
            case _:
                return default()

    def map[LL](self, func: Callable[[L], LL], /) -> Either[LL, R]:
        match self._either:
            case Left() as left:
                return Left[LL, R](func(left.value))
            case Right() as right:
                return cast(Right[LL, R], right)

    def flat_map[LL](self, func: Callable[[L], Either[LL, R]], /) -> Either[LL, R]:
        match self._either:
            case Left() as left:
                return func(left.value)
            case Right() as right:
                return cast(Right[LL, R], right)


class RightProjection[L, R](extension.Extension):
    """RightProjection"""

    __match_args__ = ("either",)

    def __init__(self, either: SubType[L, R]):
        self._either: Final = either

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._either})"

    def get(self) -> R:
        match self._either:
            case Left():
                raise ValueError(self)
            case Right() as right:
                return right.get()

    def get_or_else[LL](self, default: Callable[..., LL], /) -> LL | R:
        match self._either:
            case Left():
                return default()
            case Right() as right:
                return right.get()

    def map[RR](self, func: Callable[[R], RR], /) -> Either[L, RR]:
        match self._either:
            case Left() as left:
                return cast(Left[L, RR], left)
            case Right() as right:
                return Right[L, RR](func(right.get()))

    def flat_map[RR](self, func: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        match self._either:
            case Left() as left:
                return cast(Left[L, RR], left)
            case Right() as right:
                return func(right.get())


type SubType[L, R] = Left[L, R] | Right[L, R]
type EitherDo[L, R] = Generator[Either[L, Any], None, R]
