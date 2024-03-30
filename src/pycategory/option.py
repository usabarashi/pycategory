"""Option"""

from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Generator
from typing import Any, Callable, Literal, ParamSpec, TypeAlias, TypeVar, cast

from . import extension, extractor, monad

T = TypeVar("T")
Tp = TypeVar("Tp", covariant=True)
TTp = TypeVar("TTp", covariant=True)
Ep = TypeVar("Ep", covariant=True)
U = TypeVar("U")
P = ParamSpec("P")


class Option(ABC, monad.Monad[Tp], extension.Extension):
    """Option"""

    @abstractmethod
    def __iter__(self) -> Generator[Option[Tp], None, Tp]:
        raise NotImplementedError()

    @abstractmethod
    def map(self, func: Callable[[Tp], TTp], /) -> Option[TTp]:
        raise NotImplementedError()

    @staticmethod
    def pure(value: T) -> Option[T]:
        return Some[T](value)

    @abstractmethod
    def flat_map(self, func: Callable[[Tp], Option[TTp]], /) -> Option[TTp]:  # type: ignore
        raise NotImplementedError()

    @abstractmethod
    def fold(self, *, void: Callable[..., U], some: Callable[[Tp], U]) -> U:
        raise NotImplementedError()

    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def not_empty(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> Tp:
        raise NotImplementedError()

    @abstractmethod
    def get_or_else(self, default: Callable[..., Ep], /) -> Ep | Tp:
        raise NotImplementedError()

    @abstractproperty
    def pattern(self) -> SubType[Tp]:
        raise NotImplementedError()

    @staticmethod
    def do(  # type: ignore
        context: Callable[P, Generator[Option[Any], None, Tp]], /
    ) -> Callable[P, Option[Tp]]:
        """map, flat_map combination syntax sugar."""
        return cast(Callable[P, Option[Tp]], monad.Monad.do(context))


class Void(Option[Tp]):
    """Void"""

    def __new__(cls) -> Void[Tp]:
        if not hasattr(cls, "_singleton"):
            cls._singleton = super(Void, cls).__new__(cls)
        return cls._singleton

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __iter__(self) -> Generator[Option[Tp], None, Tp]:
        raise monad.ShortCircuit(self)

    def map(self, _: Callable[[Tp], TTp], /) -> Option[TTp]:
        return cast(Void[TTp], self)

    def flat_map(self, _: Callable[[Tp], Option[TTp]], /) -> Option[TTp]:
        return cast(Void[TTp], self)

    def fold(self, *, void: Callable[..., U], some: Callable[[Tp], U]) -> U:
        return void()

    def is_empty(self) -> Literal[True]:
        return True

    def not_empty(self) -> Literal[False]:
        return False

    def get(self) -> Tp:
        raise ValueError(self)

    def get_or_else(self, default: Callable[..., Ep], /) -> Ep:
        return default()

    @property
    def pattern(self) -> SubType[Tp]:
        return self


class Some(Option[Tp], extractor.Extractor):
    """Some"""

    __match_args__ = ("value",)

    def __init__(self, value: Tp, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.value)})"

    def __eq__(self, other: Option[Tp]) -> bool:  # type: ignore
        match other.pattern:
            case Void():
                return False
            case Some(value):
                return self.value == value

    def __iter__(self) -> Generator[Option[Tp], None, Tp]:
        yield self
        return self.value

    def map(self, func: Callable[[Tp], TTp], /) -> Option[TTp]:
        return Some[TTp](func(self.value))

    def flat_map(self, func: Callable[[Tp], Option[TTp]], /) -> Option[TTp]:
        return func(self.value)

    def fold(self, *, void: Callable[..., U], some: Callable[[Tp], U]) -> U:
        return some(self.value)

    def is_empty(self) -> Literal[False]:
        return False

    def not_empty(self) -> Literal[True]:
        return True

    def get(self) -> Tp:
        return self.value

    def get_or_else(self, default: Callable[..., Any], /) -> Tp:
        return self.value

    @property
    def pattern(self) -> SubType[Tp]:
        return self


SubType: TypeAlias = Void[Tp] | Some[Tp]
OptionDo: TypeAlias = Generator[Option[Any], None, Tp]
VOID = Void[Any]()
