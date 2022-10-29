"""Monad"""
from __future__ import annotations

from abc import ABC
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
)

T = TypeVar("T", covariant=True)
M = TypeVar("M", covariant=True)
P = ParamSpec("P")


class Composability(Enum):
    Immutable = auto()
    Variable = auto()


class Monad(ABC):
    """Monad"""

    __match_args__: tuple[()] | tuple[str] = ()

    def __bool__(self) -> bool:
        raise NotImplementedError

    def __iter__(self) -> Generator[Monad, None, Any]:
        raise NotImplementedError

    @classmethod
    def lift(cls, *args: ..., **kwargs: ...):
        return cls(*args, **kwargs)

    def unapply(self) -> tuple[()] | tuple[Any]:
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

    def map(self, functor: Any, /) -> Any:
        raise NotImplementedError

    def flatmap(self, functor: Any, /) -> Any:
        raise NotImplementedError


def do(context: Callable[P, MonadDo[M, T]], /) -> Callable[P, M]:
    """map, flatmap combination syntax sugar.

    Deprecated.

    Type Hint does not support Higher Kind Type, so get a warning.
    Only type checking can determine type violations, and runtime errors may not occur.
    """

    @wraps(context)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> M:
        context_ = context(*args, **kwargs)
        context_type: Optional[Type[M]] = None
        try:
            while True:
                yield_state = next(context_)
                if not isinstance(yield_state, Monad):
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
            return cast(Monad, context_type).lift(return_.value)

    return wrapper


MonadDo: TypeAlias = Generator[M, None, T]
