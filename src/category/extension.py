from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B", covariant=True)


class Extension:
    def method(self: A, function_: Callable[[A], B], /) -> B:
        return function_(self)
