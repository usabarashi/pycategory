from __future__ import annotations

from typing import Callable, Final, TypeVar

from . import functor

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")


class Pipeline(functor.Functor[T]):
    """Pipeline"""

    def __init__(self, value: T):
        self.value: Final[T] = value

    def __call__(self: Pipeline[Callable[[A], B]], other: A, /) -> Pipeline[B]:
        return Pipeline(self.value(other))

    def __lshift__(self: Pipeline[Callable[[A], B]], other: A, /) -> Pipeline[B]:
        """<<"""
        return Pipeline(self.value(other))

    def __rshift__(self: Pipeline[T], functor: Callable[[T], A], /) -> Pipeline[A]:
        """>>"""
        return Pipeline(functor(self.value))

    def __invert__(self: Pipeline[T]) -> T:
        """~"""
        return self.value

    def map(self: Pipeline[T], functor: Callable[[T], A], /) -> Pipeline[A]:
        return Pipeline(functor(self.value))

    def get(self) -> T:
        return self.value
