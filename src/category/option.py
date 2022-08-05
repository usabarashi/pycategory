"""Option"""
from __future__ import annotations

from abc import abstractmethod, abstractproperty
from collections.abc import Generator
from functools import wraps
from typing import Any, Callable, Generic, Literal, ParamSpec, TypeAlias, TypeVar, cast

from . import monad

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
EE = TypeVar("EE")
U = TypeVar("U")
P = ParamSpec("P")


class Option(monad.Monad, Generic[T]):
    """Option"""

    @abstractmethod
    def __iter__(self) -> Generator[Option[T], None, T]:
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

    @staticmethod
    def do(context: Callable[P, OptionDo[T]], /) -> Callable[P, Option[T]]:
        """map, flatmap combination syntax sugar.

        Only type checking can determine type violations, and runtime errors may not occur.
        """

        @wraps(context)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Option[T]:
            context_ = context(*args, **kwargs)
            try:
                while True:
                    yield_state = next(context_)
                    if not isinstance(yield_state, Option):
                        raise TypeError(yield_state)
                    match yield_state.composability():
                        case monad.Composability.Immutable:
                            return yield_state
                        case monad.Composability.Variable:
                            # Priority is given to the value of the sub-generator's monad.
                            ...
            except StopIteration as return_:
                return Some[T].lift(return_.value)

        return wrapper

    def method(self, functor: Callable[[Option[T]], TT], /) -> TT:
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
        yield self.flatmap(lambda value: Some[T](value))
        raise GeneratorExit(self)

    def map(self, functor: Callable[[T], TT], /) -> Void[TT]:
        return cast(Void[TT], self)

    def flatmap(self, functor: Callable[[T], Option[TT]], /) -> Void[TT]:
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

    def method(self, functor: Callable[[Void[T]], TT], /) -> TT:
        return functor(self)


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
        yield self.flatmap(lambda value: Some[T](value))
        return self.value

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


SubType: TypeAlias = Void[T] | Some[T]
OptionDo: TypeAlias = Generator[Option[Any], None, T]

SINGLETON_VOID = Void[Any]()
