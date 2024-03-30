"""Pipeline"""

from __future__ import annotations

from typing import Callable, Final, TypeVar

from . import functor

T = TypeVar("T")
A = TypeVar("A")
Ap = TypeVar("Ap", covariant=True)
Bp = TypeVar("Bp", covariant=True)


class Pipeline(functor.Functor[T]):
    """Pipeline"""

    def __init__(self, value: T):
        self.value: Final[T] = value

    def __call__(self: Pipeline[Callable[[A], Bp]], other: A, /) -> Pipeline[Bp]:
        return Pipeline(self.value(other))

    def __lshift__(self: Pipeline[Callable[[A], Bp]], other: A, /) -> Pipeline[Bp]:
        """<<"""
        return Pipeline(self.value(other))

    def __rshift__(self: Pipeline[T], function_: Callable[[T], Ap], /) -> Pipeline[Ap]:
        """>>"""
        return Pipeline(function_(self.value))

    def __invert__(self: Pipeline[T]) -> T:
        """~"""
        return self.value

    def map(self: Pipeline[T], function_: Callable[[T], Ap], /) -> Pipeline[Ap]:
        return Pipeline(function_(self.value))

    def get(self) -> T:
        return self.value
