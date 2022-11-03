from __future__ import annotations

from typing import Callable, Final, Generic, TypeVar

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")


class Pipeline(Generic[T]):
    """Pipeline"""

    def __init__(self, value: T):
        self.value: Final[T] = value

    def __call__(self: Pipeline[Callable[[A], B]], value: A, /) -> Pipeline[B]:
        return Pipeline(self.value(value))

    def __lshift__(self: Pipeline[Callable[[A], B]], value: A, /) -> Pipeline[B]:
        """<<"""
        return Pipeline(self.value(value))

    def __rshift__(self: Pipeline[T], function: Callable[[T], A], /) -> Pipeline[A]:
        """>>"""
        return Pipeline(function(self.value))
