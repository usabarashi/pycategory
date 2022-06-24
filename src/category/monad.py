"""Monad"""
from __future__ import annotations

import inspect
from typing import (
    Any,
    Callable,
    Generator,
    Optional,
    ParamSpec,
    Type,
    TypeAlias,
    TypeVar,
)

T = TypeVar("T", covariant=True)
M = TypeVar("M", covariant=True)
P = ParamSpec("P")


class Monad:
    """Monad"""

    def get(self) -> Any:
        ...

    def map(self, functor: Any, /) -> Any:
        ...

    def flatmap(self, functor: Any, /) -> Any:
        ...


def do(context: Callable[P, MonadDo[M, T]], /) -> Callable[P, M]:
    """map, flatmap combination syntax sugar.

    Type Hint does not support Higher Kind Type, so get a warning.
    """

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> M:
        context_ = context(*args, **kwargs)
        type_: Optional[Type[M]] = None
        lift: Callable[[T], M] = None  # type: ignore
        state: Any = None
        try:
            while True:
                flattend, send, lift = context_.send(state)
                match bool(flattend), type_:
                    case False, _:
                        return flattend
                    case True, None:
                        type_, state, lift = type(flattend), send(flattend), lift
                    case True, _ if type(flattend) is type_:
                        state = send(flattend)
                    case _:
                        raise ValueError(context)
        except StopIteration as return_:
            if type_ is None:
                raise ValueError(context)
            return lift(return_.value)

    return wrapper


MonadDo: TypeAlias = Generator[
    # tuple[M[T], Callable[[M[T]], T], Callable[[T], M[T]]],
    tuple[M, Callable[[M], T], Callable[[T], M]],
    # tuple[M[T], Callable[[M[T]], T], Callable[[T], M[T]]],
    tuple[M, Callable[[M], T], Callable[[T], M]],
    T,
]


class Frame:
    def __init__(self, depth: int = 2):
        self.filename: str = inspect.stack()[depth].filename
        self.line: int = inspect.stack()[depth].frame.f_lineno
        self.function: str = inspect.stack()[depth].function
        self.args: dict[str, Any] = inspect.getargvalues(
            inspect.stack()[depth].frame
        ).locals
        self.stack: list[inspect.FrameInfo] = inspect.stack()
