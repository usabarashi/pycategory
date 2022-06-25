"""Monad"""
from __future__ import annotations

import inspect
from abc import ABC
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


class Monad(ABC):
    """Monad"""

    @staticmethod
    def send(monad: Any, /) -> Any:
        """

        send a flatmap context.
        """
        ...

    @staticmethod
    def lift(value: Any, /) -> Monad:
        ...

    def get(self) -> Any:
        ...

    def map(self, functor: Any, /) -> Any:
        ...

    def flatmap(self, functor: Any, /) -> Any:
        ...


def do(context: Callable[P, MonadDo[M, T]], /) -> Callable[P, M]:
    """map, flatmap combination syntax sugar.

    Type Hint does not support Higher Kind Type, so get a warning.
    Only type checking can determine type violations, and runtime errors may not occur.
    """

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> M:
        context_ = context(*args, **kwargs)
        context_type: Optional[Type[M]] = None
        state: Any = None
        try:
            while True:
                flatmapped = context_.send(state)
                match isinstance(flatmapped, Monad), bool(flatmapped), context_type:
                    case True, False, _:
                        return flatmapped
                    case True, True, None:
                        context_type = type(flatmapped)
                    case True, True, _ if type(flatmapped) is not context_type:
                        raise TypeError(
                            flatmapped,
                            f"A different type ${type(flatmapped)} from the context ${context_} is specified.",
                        )
                    case True, True, _ if type(flatmapped) is context_type:
                        state = cast(Monad, context_type).send(flatmapped)
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
