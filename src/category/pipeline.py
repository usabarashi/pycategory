from __future__ import annotations

from typing import Callable, Final, Generic, TypeVar

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")


class Pipeline(Generic[T]):
    """Pipeline"""

    def __init__(self, value: T):
        self.value: Final[T] = value

    def __call__(self: Pipeline[Callable[[A], B]], other: A, /) -> Pipeline[B]:
        return Pipeline(self.value(other))

    def __lshift__(self: Pipeline[Callable[[A], B]], other: A, /) -> Pipeline[B]:
        """<<"""
        return Pipeline(self.value(other))

    def __rshift__(self: Pipeline[T], other: Callable[[T], A], /) -> Pipeline[A]:
        """>>"""
        return Pipeline(other(self.value))

    def __invert__(self: Pipeline[T]) -> T:
        """~"""
        return self.value

    def get(self) -> T:
        return self.value
