"""Option"""
from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Generator
from typing import Any, Callable, Literal, ParamSpec, TypeAlias, TypeVar, cast

from . import extension, extractor, monad

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
EE = TypeVar("EE")
U = TypeVar("U")
P = ParamSpec("P")


class Option(ABC, monad.Monad[T], extension.Extension):
    """Option"""

    @abstractmethod
    def __iter__(self) -> Generator[Option[T], None, T]:
        raise NotImplementedError

    @abstractmethod
    def map(self, function_: Callable[[T], TT], /) -> Option[TT]:
        raise NotImplementedError

    @staticmethod
    def pure(value: T) -> Option[T]:
        return Some[T](value)

    @abstractmethod
    def flat_map(self, function_: Callable[[T], Option[TT]], /) -> Option[TT]:
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


class Void(Option[T]):
    """Void"""

    def __new__(cls) -> Void[T]:
        if not hasattr(cls, "_singleton"):
            cls._singleton = super(Void, cls).__new__(cls)
        return cls._singleton

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __iter__(self) -> Generator[Option[T], None, T]:
        raise GeneratorExit(self)

    def map(self, _: Callable[[T], TT], /) -> Option[TT]:
        return cast(Void[TT], self)

    def flat_map(self, _: Callable[[T], Option[TT]], /) -> Option[TT]:
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


class Some(Option[T], extractor.Extractor):
    """Some"""

    __match_args__ = ("value",)

    def __init__(self, value: T, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.value)})"

    def __iter__(self) -> Generator[Option[T], None, T]:
        yield self
        return self.value

    def map(self, function_: Callable[[T], TT], /) -> Option[TT]:
        return Some[TT](function_(self.value))

    def flat_map(self, function_: Callable[[T], Option[TT]], /) -> Option[TT]:
        return function_(self.value)

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


SubType: TypeAlias = Void[T] | Some[T]
OptionDo: TypeAlias = Generator[Option[T], None, T]
VOID = Void[Any]()
