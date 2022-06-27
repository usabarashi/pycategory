"""Monad"""
from __future__ import annotations

import inspect
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
    POSSIBLE = auto()
    IMPOSSIBLE = auto()


class Monad(ABC):
    """Monad"""

    __match_args__: tuple[()] | tuple[str] = ()

    def __bool__(self) -> bool:
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
                return Composability.IMPOSSIBLE
            case True:
                return Composability.POSSIBLE

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
        state: Any = None
        try:
            while True:
                yield_state = context_.send(state)
                if not isinstance(yield_state, Monad):
                    raise TypeError(yield_state)
                match yield_state.composability(), context_type:
                    case Composability.IMPOSSIBLE, _:
                        return yield_state
                    case Composability.POSSIBLE, None:
                        context_type = type(yield_state)
                        state = yield_state.unapply()
                    case Composability.POSSIBLE, _ if type(
                        yield_state
                    ) is not context_type:
                        raise TypeError(
                            yield_state,
                            f"A different type ${type(yield_state)} from the context ${context_} is specified.",
                        )
                    case Composability.POSSIBLE, _ if type(yield_state) is context_type:
                        state = yield_state.unapply()
                    case _:
                        raise ValueError(context)
        except StopIteration as return_:
            if context_type is None:
                raise TypeError(context, "No context type specification")
            return cast(Monad, context_type).lift(return_.value)

    return wrapper


MonadDo: TypeAlias = Generator[M, Any, T]


class Frame:
    def __init__(self, depth: int = 2):
        self.filename: str = inspect.stack()[depth].filename
        self.line: int = inspect.stack()[depth].frame.f_lineno
        self.function: str = inspect.stack()[depth].function
        self.args: dict[str, Any] = inspect.getargvalues(
            inspect.stack()[depth].frame
        ).locals
        self.stack: list[inspect.FrameInfo] = inspect.stack()
