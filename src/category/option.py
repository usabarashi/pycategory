"""Option"""
from __future__ import annotations

from abc import abstractmethod, abstractproperty
from collections.abc import Generator
from typing import Any, Callable, Literal, ParamSpec, TypeAlias, TypeVar, cast

from . import monad

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
EE = TypeVar("EE")
U = TypeVar("U")
P = ParamSpec("P")


class Option(monad.Monad[T]):
    """Option"""

    @abstractmethod
    def __iter__(self) -> Generator[Option[T], None, T]:
        raise NotImplementedError

    @abstractmethod
    def map(self, functor: Callable[[T], TT], /) -> Option[TT]:
        raise NotImplementedError

    @staticmethod
    def pure(value: T) -> Option[T]:
        return Some[T](value)

    @abstractmethod
    def flat_map(self, other: Callable[[T], Option[TT]], /) -> Option[TT]:
        raise NotImplementedError

    @abstractmethod
    def fold(self, *, void: Callable[..., U], some: Callable[[T], U]) -> U:
        raise NotImplementedError

    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def not_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_or_else(self, default: Callable[..., EE], /) -> EE | T:
        raise NotImplementedError

    @abstractproperty
    def pattern(self) -> SubType[T]:
        raise NotImplementedError

    def method(self, other: Callable[[Option[T]], TT], /) -> TT:
        raise NotImplementedError


class Void(Option[T]):
    """Void"""

    def __new__(cls) -> Void[T]:
        if not hasattr(cls, "_singleton"):
            cls._singleton = super(Void, cls).__new__(cls)
        return cls._singleton

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __bool__(self) -> Literal[False]:
        return False

    def __iter__(self) -> Generator[Option[T], None, T]:
        raise GeneratorExit(self)

    def map(self, functor: Callable[[T], TT], /) -> Void[TT]:
        return cast(Void[TT], self)

    def flat_map(self, other: Callable[[T], Option[TT]], /) -> Void[TT]:
        return cast(Void[TT], self)

    def fold(self, *, void: Callable[..., U], some: Callable[[T], U]) -> U:
        return void()

    def is_empty(self) -> Literal[True]:
        return True

    def not_empty(self) -> Literal[False]:
        return False

    def get(self) -> T:
        raise ValueError(self)

    def get_or_else(self, default: Callable[..., EE], /) -> EE:
        return default()

    @property
    def pattern(self) -> SubType[T]:
        return self

    def method(self, other: Callable[[Void[T]], TT], /) -> TT:
        return other(self)


class Some(Option[T]):
    """Some"""

    __match_args__ = ("value",)

    def __init__(self, value: T, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.value)})"

    def __bool__(self) -> Literal[True]:
        return True

    def __iter__(self) -> Generator[Option[T], None, T]:
        yield self
        return self.value

    def map(self, functor: Callable[[T], TT], /) -> Some[TT]:
        return Some[TT](functor(self.value))

    def flat_map(self, other: Callable[[T], Option[TT]], /) -> Option[TT]:
        return other(self.value)

    def fold(self, *, void: Callable[..., U], some: Callable[[T], U]) -> U:
        return some(self.value)

    def is_empty(self) -> Literal[False]:
        return False

    def not_empty(self) -> Literal[True]:
        return True

    def get(self) -> T:
        return self.value

    def get_or_else(self, default: Callable[..., EE], /) -> T:
        return self.value

    @property
    def pattern(self) -> SubType[T]:
        return self

    def method(self, other: Callable[[Some[T]], TT], /) -> TT:
        return other(self)


SubType: TypeAlias = Void[T] | Some[T]
OptionDo: TypeAlias = Generator[Option[T], None, T]

SINGLETON_VOID = Void[Any]()
