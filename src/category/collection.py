from __future__ import annotations

from functools import reduce
from typing import Any, Callable, Iterable, NoReturn, Optional, TypeVar

T = TypeVar("T", covariant=True)
A = TypeVar("A")


class Vector(list[T]):
    """Immutable Collection

    see: https://docs.python.org/3.9/library/collections.abc.html#collections.abc.Sequence
    """

    def __init__(self, items: Optional[list[T] | tuple[T, ...] | tuple[()]] = None):
        if items is None:
            items = list()
        list[T].__init__(self, items)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({[element for element in self]})"

    def __add__(self, other: list[T], /) -> Vector[T]:
        sequence = list(self)
        return self.__class__(sequence.__add__(other))

    def __setitem__(self, slice_: slice, item: Iterable[T]) -> NoReturn:
        raise TypeError("Does not support the __setitem__ method")

    def __delitem__(self, slice_: slice) -> NoReturn:
        raise TypeError("Does not support the __delitem__ method")

    def append(self, obj: T, /) -> Vector[T]:
        sequence = list(self)
        sequence.append(obj)
        return self.__class__(sequence)

    def extend(self, items: Iterable[T], /) -> Vector[T]:
        sequence = list(self)
        sequence.extend(items)
        return self.__class__(sequence)

    def insert(self, *, index: int, obj: T) -> Vector[T]:
        sequence = list(self)
        sequence.insert(index, obj)
        return self.__class__(sequence)

    def remove(self, obj: Any, /) -> Vector[T]:
        sequence = list(self)
        sequence.remove(obj)
        return self.__class__(sequence)

    def pop(self, index: int, /) -> Vector[T]:
        sequence = list(self)
        sequence.pop(index)
        return self.__class__(sequence)

    def clear(self) -> None:
        raise TypeError("Does not support the clear method")

    def index(self, *, obj: T, start: int, end: int) -> int:
        return list[T].index(self, obj, start, end)

    def count(self, obj: T, /) -> int:
        return list[T].count(self, obj)

    def sort(
        self,
        *,
        key: Optional[T] = None,
        reverse: bool = False,
    ) -> Vector[T]:
        sequence = list(self)
        sequence.sort(key=key, reverse=reverse)
        return self.__class__(sequence)

    def __reversed__(self) -> Vector[T]:
        sequence = list(self)
        sequence.reverse()
        return self.__class__(sequence)

    def reverse(self) -> Vector[T]:
        sequence = list(self)
        sequence.reverse()
        return self.__class__(sequence)

    def copy(self) -> Vector[T]:
        return self.__class__(list(self))

    def is_empty(self) -> bool:
        return 0 == len(self)

    def non_empty(self) -> bool:
        return 0 < len(self)

    def size(self) -> int:
        return len(self)

    def map(self, function_: Callable[[T], A], /) -> Vector[A]:
        return self.__class__([function_(element) for element in self])

    def reduce(self, function: Callable[[T, T], T], /) -> T:
        return reduce(function, self)

    def filter(self, function: Callable[[T], bool], /) -> Vector[T]:
        return self.__class__([element for element in self if function(element)])
