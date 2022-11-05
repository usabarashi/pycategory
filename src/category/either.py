"""Either"""
from __future__ import annotations

from abc import abstractmethod, abstractproperty
from collections.abc import Generator
from functools import wraps
from typing import Any, Callable, Generic, Literal, ParamSpec, TypeAlias, TypeVar, cast

from . import constraints, monad, option, try_

L = TypeVar("L", covariant=True)
R = TypeVar("R", covariant=True)
LL = TypeVar("LL")
RR = TypeVar("RR")
TT = TypeVar("TT")
U = TypeVar("U")
P = ParamSpec("P")


class Either(monad.Monad2[L, R]):
    """Either"""

    @abstractmethod
    def __iter__(self) -> Generator[Either[L, R], None, R]:
        raise NotImplementedError

    @abstractmethod
    def map(self, other: Callable[[R], RR], /) -> Either[L, RR]:
        raise NotImplementedError

    @abstractmethod
    def flat_map(self, other: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
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

    @staticmethod
    def do(context: Callable[P, EitherDo[L, R]], /) -> Callable[P, Either[L, R]]:
        """map, flat_map combination syntax sugar.

        Only type checking can determine type violations, and runtime errors may not occur.
        """

        @wraps(context)
        def wrapper(*args: P.args, **kwargs: P.kwargs):
            context_ = context(*args, **kwargs)
            try:
                while True:
                    yield_state = next(context_)
                    if not isinstance(yield_state, Either):
                        raise TypeError(yield_state)
                    match yield_state.composability():
                        case monad.Composability.Immutable:
                            return yield_state
                        case monad.Composability.Variable:
                            # Priority is given to the value of the sub-generator's monad.
                            ...
            except StopIteration as return_:
                return Right[L, R].lift(return_.value)

        return wrapper

    @abstractmethod
    def method(self, other: Callable[[Either[L, R]], TT], /) -> TT:
        raise NotImplementedError


class Left(Either[L, R]):
    """Left"""

    __match_args__ = ("value",)

    def __init__(self, value: L, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __bool__(self) -> Literal[False]:
        return False

    def __iter__(self) -> Generator[Either[L, R], None, R]:
        yield self.flat_map(lambda right: Right[L, R](right))
        raise GeneratorExit(self)

    def map(self, other: Callable[[R], RR], /) -> Left[L, RR]:
        return cast(Left[L, RR], self)

    def flat_map(self, other: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        return cast(Left[L, RR], self)

    @property
    def to_option(self) -> option.Option[R]:
        return option.Void[R]()

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

    def method(self, other: Callable[[Left[L, R]], TT], /) -> TT:
        return other(self)


class Right(Either[L, R]):
    """Right"""

    __match_args__ = ("value",)

    def __init__(self, value: R, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __bool__(self) -> Literal[True]:
        return True

    def __iter__(self) -> Generator[Either[L, R], None, R]:
        yield self.flat_map(lambda right: Right[L, R](right))
        return self.value

    def map(self, other: Callable[[R], RR], /) -> Right[L, RR]:
        return Right[L, RR](other(self.value))

    def flat_map(self, other: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        return other(self.value)

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

    def method(self, other: Callable[[Right[L, R]], TT], /) -> TT:
        return other(self)


class LeftProjection(Generic[L, R]):
    """LeftProjection"""

    __match_args__ = ("either",)

    def __init__(self, either: SubType[L, R]):
        self._either = either

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._either})"

    def __bool__(self) -> bool:
        return bool(self._either)

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

    def map(self, other: Callable[[L], LL], /) -> Either[LL, R]:
        match self._either:
            case Left() as left:
                return Left[LL, R](other(left.value))
            case Right() as right:
                return cast(Right[LL, R], right)

    def flat_map(self, other: Callable[[L], Either[LL, R]], /) -> Either[LL, R]:
        match self._either:
            case Left() as left:
                return other(left.value)
            case Right() as right:
                return cast(Right[LL, R], right)


class RightProjection(Generic[L, R]):
    """RightProjection"""

    __match_args__ = ("either",)

    def __init__(self, either: SubType[L, R]):
        self._either = either

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._either})"

    def __bool__(self) -> bool:
        return bool(self._either)

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

    def map(self, other: Callable[[R], RR], /) -> Either[L, RR]:
        match self._either:
            case Left() as left:
                return cast(Left[L, RR], left)
            case Right() as right:
                return Right[L, RR](other(right.get()))

    def flat_map(self, other: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        match self._either:
            case Left() as left:
                return cast(Left[L, RR], left)
            case Right() as right:
                return other(right.get())


SubType: TypeAlias = Left[L, R] | Right[L, R]
EitherDo: TypeAlias = Generator[Either[L, Any], None, R]
