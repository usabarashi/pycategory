"""Pipeline"""

from __future__ import annotations

from typing import Callable, Final

from pycategory.trait import functor


class Pipeline[A](functor.Functor[A]):
    """Pipeline"""

    def __init__(self, value: A):
        self.value: Final = value

    def __call__[B, C](self: Pipeline[Callable[[B], C]], other: B, /) -> Pipeline[C]:
        return Pipeline(self.value(other))

    def __lshift__[B, C](self: Pipeline[Callable[[B], C]], other: B, /) -> Pipeline[C]:
        """<<"""
        return Pipeline(self.value(other))

    def __rshift__[B](self: Pipeline[A], function_: Callable[[A], B], /) -> Pipeline[B]:
        """>>"""
        return Pipeline(function_(self.value))

    def __invert__(self: Pipeline[A]) -> A:
        """~"""
        return self.value

    def map[B](self: Pipeline[A], function_: Callable[[A], B], /) -> Pipeline[B]:
        return Pipeline(function_(self.value))

    def get(self) -> A:
        return self.value
