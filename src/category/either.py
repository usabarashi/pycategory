"""Either"""
from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Generator
from typing import Any, Callable, Generic, Literal, TypeVar

L = TypeVar("L", covariant=True)
R = TypeVar("R", covariant=True)
LL = TypeVar("LL")
RR = TypeVar("RR")
TT = TypeVar("TT")
U = TypeVar("U")


class Either(ABC, Generic[L, R]):
    """Either"""

    @abstractmethod
    def __call__(self) -> Generator[Either[L, R], Either[L, R], R]:
        raise NotImplementedError

    @abstractmethod
    def map(self, functor: Callable[[R], RR], /) -> Either[L, RR]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, functor: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
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

    @abstractmethod
    def method(self, functor: Callable[[Either[L, R]], TT]) -> TT:
        raise NotImplementedError

    @staticmethod
    def do(
        generator_fuction: Callable[..., EitherDo[L, R]]
    ) -> Callable[..., Either[L, R]]:
        def wrapper(*args: Any, **kwargs: Any) -> Either[L, R]:
            def recur(
                generator: EitherDo[L, R],
                prev: Any | Either[L, Any],
            ) -> Either[L, R]:
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    return Right[L, R](last.value)
                if isinstance(result, Left):
                    return result
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return wrapper


class Left(Either[L, R]):
    """Left"""

    __match_args__ = ("value",)

    def __init__(self, value: L, /):
        self.value = value

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(self) -> Generator[Left[L, R], Left[L, R], R]:
        yield self
        raise GeneratorExit(self)

    def map(self, functor: Callable[[R], RR], /) -> Left[L, RR]:
        return Left[L, RR](self.value)

    def flatmap(self, functor: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        return Left[L, RR](self.value)

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

    def method(self, functor: Callable[[Left[L, R]], TT], /) -> TT:
        return functor(self)


class Right(Either[L, R]):
    """Right"""

    __match_args__ = ("value",)

    def __init__(self, value: R, /):
        self.value = value

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(self) -> Generator[Either[L, R], Either[L, R], R]:
        yield self
        return self.value

    def map(self, functor: Callable[[R], RR], /) -> Right[L, RR]:
        return Right[L, RR](functor(self.value))

    def flatmap(self, functor: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        return functor(self.value)

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

    def method(self, functor: Callable[[Right[L, R]], TT], /) -> TT:
        return functor(self)


class LeftProjection(Generic[L, R]):
    """LeftProjection"""

    __match_args__ = ("either",)

    def __init__(self, either: SubType[L, R]):
        self._either = either

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

    def map(self, functor: Callable[[L], LL], /) -> Either[LL, R]:
        match self._either:
            case Left() as left:
                return Left[LL, R](functor(left.value))
            case Right() as right:
                return Right[LL, R](right.get())

    def flatmap(self, functor: Callable[[L], Either[LL, R]], /) -> Either[LL, R]:
        match self._either:
            case Left() as left:
                return functor(left.value)
            case Right() as right:
                return Right[LL, R](right.get())


class RightProjection(Generic[L, R]):
    """RightProjection"""

    __match_args__ = ("either",)

    def __init__(self, either: SubType[L, R]):
        self._either = either

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

    def map(self, functor: Callable[[R], RR], /) -> Either[L, RR]:
        match self._either:
            case Left() as left:
                return Left[L, RR](left.value)
            case Right() as right:
                return Right[L, RR](functor(right.get()))

    def flatmap(self, functor: Callable[[R], Either[L, RR]], /) -> Either[L, RR]:
        match self._either:
            case Left() as left:
                return Left[L, RR](left.value)
            case Right() as right:
                return functor(right.get())


SubType = Left[L, R] | Right[L, R]
EitherDo = Generator[Any | Either[L, Any], Any | Either[L, Any], R]
ReturnEither = EitherDo
