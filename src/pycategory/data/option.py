"""Option"""

from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Generator
from typing import Any, Callable, Final, Literal, cast

from pycategory.trait import extension, monad
from pycategory.type import extractor


class Option[A](extension.Extension, monad.Monad[A], ABC):
    """Option"""

    @abstractmethod
    def __iter__(self) -> Generator[Option[A], None, A]:
        raise NotImplementedError()

    @abstractmethod
    def map[B](self, func: Callable[[A], B], /) -> Option[B]:
        raise NotImplementedError()

    @staticmethod
    def pure(value: A) -> Option[A]:
        return Some[A](value)

    @abstractmethod
    def flat_map[B](self, func: Callable[[A], Option[B]], /) -> Option[B]:  # type: ignore
        raise NotImplementedError()

    @abstractmethod
    def fold[U](self, *, void: Callable[..., U], some: Callable[[A], U]) -> U:
        raise NotImplementedError()

    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def not_empty(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> A:
        raise NotImplementedError()

    @abstractmethod
    def get_or_else[E](self, default: Callable[..., E], /) -> E | A:
        raise NotImplementedError()

    @abstractproperty
    def pattern(self) -> SubType[A]:
        raise NotImplementedError()

    @staticmethod
    def do[  # type: ignore
        **P
    ](context: Callable[P, Generator[Option[Any], None, A]], /) -> Callable[  # type: ignore
        P, Option[A]
    ]:
        """map, flat_map combination syntax sugar."""
        return cast(Callable[P, Option[A]], monad.Monad.do(context))


class Void[A](Option[A]):
    """Void"""

    def __new__(cls) -> Void[A]:
        if not hasattr(cls, "_singleton"):
            cls._singleton = super(Void, cls).__new__(cls)
        return cls._singleton

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __iter__(self) -> Generator[Option[A], None, A]:
        raise monad.ShortCircuit(self)

    def map[B](self, _: Callable[[A], B], /) -> Option[B]:
        return cast(Void[B], self)

    def flat_map[B](self, _: Callable[[A], Option[B]], /) -> Option[B]:
        return cast(Void[B], self)

    def fold[U](self, *, void: Callable[..., U], some: Callable[[A], U]) -> U:
        return void()

    def is_empty(self) -> Literal[True]:
        return True

    def not_empty(self) -> Literal[False]:
        return False

    def get(self) -> A:
        raise ValueError(self)

    def get_or_else[E](self, default: Callable[..., E], /) -> E:
        return default()

    @property
    def pattern(self) -> SubType[A]:
        return self


class Some[A](Option[A], extractor.Extractor):
    """Some"""

    __match_args__ = ("value",)

    def __init__(self, value: A, /):
        self.value: Final = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.value)})"

    def __eq__(self, other: Option[A]) -> bool:  # type: ignore
        match other.pattern:
            case Void():
                return False
            case Some(value):
                return self.value == value

    def __iter__(self) -> Generator[Option[A], None, A]:
        yield self
        return self.value

    def map[B](self, func: Callable[[A], B], /) -> Option[B]:
        return Some[B](func(self.value))

    def flat_map[B](self, func: Callable[[A], Option[B]], /) -> Option[B]:
        return func(self.value)

    def fold[U](self, *, void: Callable[..., U], some: Callable[[A], U]) -> U:
        return some(self.value)

    def is_empty(self) -> Literal[False]:
        return False

    def not_empty(self) -> Literal[True]:
        return True

    def get(self) -> A:
        return self.value

    def get_or_else(self, default: Callable[..., Any], /) -> A:
        return self.value

    @property
    def pattern(self) -> SubType[A]:
        return self


type SubType[A] = Void[A] | Some[A]
type OptionDo[A] = Generator[Option[Any], None, A]
VOID = Void[Any]()
