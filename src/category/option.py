"""Option"""
from __future__ import annotations

from abc import abstractmethod, abstractproperty
from collections.abc import Generator
from typing import Any, Callable, Generic, Literal, TypeVar

from category.monad import Monad

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
EE = TypeVar("EE")
U = TypeVar("U")


class Option(Monad, Generic[T]):
    """Option"""

    @abstractmethod
    def __iter__(self) -> Generator[Option[T], None, T]:
        raise NotImplementedError

    @staticmethod
    def send(monad: Option[T], /) -> T:
        raise NotImplementedError

    @staticmethod
    def lift(value: T, /) -> Option[T]:
        raise NotImplementedError

    @abstractmethod
    def map(self, functor: Callable[[T], TT], /) -> Option[TT]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, functor: Callable[[T], Option[TT]], /) -> Option[TT]:
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

    def method(self, functor: Callable[[Option[T]], TT], /) -> TT:
        raise NotImplementedError


class Void(Option[T]):
    """Void"""

    def __new__(cls) -> Void[T]:
        if not hasattr(cls, "_singleton"):
            cls._singleton = super(Void, cls).__new__(cls)
        return cls._singleton

    def __bool__(self) -> Literal[False]:
        return False

    def __iter__(self) -> Generator[Option[T], None, T]:
        yield self.flatmap(lambda value: Some[T](value))
        raise GeneratorExit(self)

    @staticmethod
    def send(monad: Option[T], /) -> T:
        return monad.get()

    @staticmethod
    def lift(value: T, /) -> Void[T]:
        return Void[T]()

    def map(self, functor: Callable[[T], TT], /) -> Void[TT]:
        return Void[TT]()

    def flatmap(self, functor: Callable[[T], Option[TT]], /) -> Void[TT]:
        return Void[TT]()

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

    def method(self, functor: Callable[[Void[T]], TT], /) -> TT:
        return functor(self)


class Some(Option[T]):
    """Some"""

    __match_args__ = ("value",)

    def __init__(self, value: T, /):
        self.value = value

    def __bool__(self) -> Literal[True]:
        return True

    def __iter__(self) -> Generator[Option[T], None, T]:
        yield self.flatmap(lambda value: Some[T](value))
        return self.value

    @staticmethod
    def send(monad: Option[T]) -> T:
        return monad.get()

    @staticmethod
    def lift(value: T) -> Some[T]:
        return Some[T](value)

    def map(self, functor: Callable[[T], TT], /) -> Some[TT]:
        return Some[TT](functor(self.value))

    def flatmap(self, functor: Callable[[T], Option[TT]], /) -> Option[TT]:
        return functor(self.value)

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

    def method(self, functor: Callable[[Some[T]], TT], /) -> TT:
        return functor(self)


SubType = Void[T] | Some[T]
OptionDo = Generator[Option[T], Any, T]

SINGLETON_VOID = Void[Any]()
