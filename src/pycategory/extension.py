"""Extension"""

from typing import Callable, TypeVar

A = TypeVar("A")
Bp = TypeVar("Bp", covariant=True)


class Extension:
    def method(self: A, function_: Callable[[A], Bp], /) -> Bp:
        return function_(self)
