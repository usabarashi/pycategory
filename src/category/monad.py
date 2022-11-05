"""Monad"""
from __future__ import annotations

from abc import abstractmethod
from enum import Enum, auto
from functools import wraps
from typing import (
    Any,
    Callable,
    Generator,
    Optional,
    ParamSpec,
    Type,
    TypeAlias,
    TypeVar,
    cast,
    overload,
)

from . import applicative, curry_

T = TypeVar("T", covariant=True)
A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)
C = TypeVar("C", covariant=True)
M = TypeVar("M", covariant=True)
P = ParamSpec("P")


class Composability(Enum):
    Immutable = auto()
    Variable = auto()


@curry_.curry
def monad(self: Monad[T], other: Callable[[T], Monad[A]], /) -> Monad[A]:
    raise NotImplementedError


@curry_.curry
def monad2(self: Monad2[A, B], other: Callable[[B], Monad2[A, C]], /) -> Monad2[A, C]:
    raise NotImplementedError


@overload
def do(context: Callable[P, Generator[Monad[T], None, T]], /) -> Callable[P, Monad[T]]:
    ...


@overload
def do(
    context: Callable[P, Generator[Monad2[A, B], None, B]], /
) -> Callable[P, Monad2[A, B]]:
    ...


def do(
    context: Callable[P, Generator[Monad[T], None, T]]
    | Callable[P, Generator[Monad2[A, B], None, B]],
    /,
) -> Callable[P, Monad[T]] | Callable[P, Monad2[A, B]]:
    """map, flat_map combination syntax sugar.

    Deprecated.

    Type Hint does not support Higher Kind Type, so get a warning.
    Only type checking can determine type violations, and runtime errors may not occur.
    """

    @wraps(context)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Monad[T] | Monad2[A, B]:
        context_ = context(*args, **kwargs)
        context_type: Optional[Type[Monad[T] | Monad2[A, B]]] = None
        try:
            while True:
                yield_state = next(context_)
                if not any(
                    (
                        isinstance(yield_state, Monad),
                        isinstance(yield_state, Monad2),
                    )
                ):
                    raise TypeError(yield_state)
                match yield_state.composability(), context_type:
                    case Composability.Immutable, _:
                        return yield_state
                    case Composability.Variable, None:
                        context_type = type(yield_state)
                    case Composability.Variable, _ if type(
                        yield_state
                    ) is not context_type:
                        raise TypeError(
                            yield_state,
                            f"A different type ${type(yield_state)} from the context ${context_} is specified.",
                        )
                    case Composability.Variable, _ if type(yield_state) is context_type:
                        # Priority is given to the value of the subgenerator's return monad.
                        ...
                    case _:
                        raise ValueError(context)
        except StopIteration as return_:
            if context_type is None:
                raise TypeError(context, "No context type specification")
            return cast(Monad[T] | Monad2[A, B], context_type).lift(return_.value)

    return wrapper


class Monad(applicative.Applicative[T]):
    """Monad"""

    __match_args__: tuple[()] | tuple[str] = ()

    def __bool__(self) -> bool:
        raise NotImplementedError

    def __iter__(self) -> Generator[Monad[T], None, T]:
        raise NotImplementedError

    @classmethod
    def lift(cls, *args: ..., **kwargs: ...) -> Monad[T]:
        return cls(*args, **kwargs)

    def unapply(self) -> tuple[()] | tuple[Any, ...]:
        """

        Return match attributes as tuples
        """
        if len(self.__match_args__) <= 0:
            return ()
        else:
            return tuple(
                value for key, value in vars(self).items() if key in self.__match_args__
            )

    def composability(self) -> Composability:
        match self.__bool__():
            case False:
                return Composability.Immutable
            case True:
                return Composability.Variable

    def get(self) -> Any:
        raise NotImplementedError

    flat_map = abstractmethod(monad)


class Monad2(applicative.Applicative2[A, B]):
    """Monad"""

    __match_args__: tuple[()] | tuple[str] = ()

    def __bool__(self) -> bool:
        raise NotImplementedError

    def __iter__(self) -> Generator[Monad2[A, B], None, B]:
        raise NotImplementedError

    @classmethod
    def lift(cls, *args: ..., **kwargs: ...) -> Monad2[A, B]:
        return cls(*args, **kwargs)

    def unapply(self) -> tuple[()] | tuple[Any, ...]:
        """

        Return match attributes as tuples
        """
        if len(self.__match_args__) <= 0:
            return ()
        else:
            return tuple(
                value for key, value in vars(self).items() if key in self.__match_args__
            )

    def composability(self) -> Composability:
        match self.__bool__():
            case False:
                return Composability.Immutable
            case True:
                return Composability.Variable

    def get(self) -> B:
        raise NotImplementedError

    flat_map = abstractmethod(monad2)


MonadDo: TypeAlias = Generator[Monad[T], None, T] | Generator[Monad2[A, B], None, B]
