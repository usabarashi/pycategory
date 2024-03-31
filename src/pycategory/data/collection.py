from __future__ import annotations

import sys
from functools import reduce
from typing import Any, Callable, Iterable, NoReturn, Optional, cast


class Vector[A](list[A]):
    """Immutable Collection

    see: https://docs.python.org/3.9/library/collections.abc.html#collections.abc.Sequence
    """

    def __init__(self, items: Optional[list[A] | tuple[A, ...] | tuple[()]] = None):
        if items is None:
            items = list()
        list[A].__init__(self, items)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({[element for element in self]})"

    def __add__(self, other: list[A], /) -> Vector[A]:  # type: ignore
        sequence = list(self)
        return self.__class__(sequence.__add__(other))

    def __setitem__(self, slice_: slice, item: Iterable[A]) -> NoReturn:  # type: ignore
        raise TypeError("Does not support the __setitem__ method")

    def __delitem__(self, slice_: slice) -> NoReturn:  # type: ignore
        raise TypeError("Does not support the __delitem__ method")

    def append(self, obj: A, /) -> Vector[A]:  # type: ignore
        sequence = list(self)
        sequence.append(obj)
        return self.__class__(sequence)

    def extend(self, items: Iterable[A], /) -> Vector[A]:  # type: ignore
        sequence = list(self)
        sequence.extend(items)
        return self.__class__(sequence)

    def insert(self, *, index: int, obj: A) -> Vector[A]:  # type: ignore
        sequence = list(self)
        sequence.insert(index, obj)
        return self.__class__(sequence)

    def remove(self, obj: Any, /) -> Vector[A]:  # type: ignore
        sequence = list(self)
        sequence.remove(obj)
        return self.__class__(sequence)

    def pop(self, index: int, /) -> Vector[A]:  # type: ignore
        sequence = list(self)
        sequence.pop(index)
        return self.__class__(sequence)

    def clear(self) -> None:
        raise TypeError("Does not support the clear method")

    def index(self, *, obj: A, start: int = 0, end: int = sys.maxsize) -> int:  # type: ignore
        return list[A].index(self, obj, start, end)

    def count(self, obj: A, /) -> int:
        return list[A].count(self, obj)

    def sort(  # type: ignore
        self,
        *,
        key: Optional[A] = None,
        reverse: bool = False,
    ) -> Vector[A]:
        sequence = list(self)
        sequence.sort(key=key, reverse=reverse)  # type: ignore
        return self.__class__(sequence)

    def __reversed__(self) -> Vector[A]:  # type: ignore
        sequence = list(self)
        sequence.reverse()
        return self.__class__(sequence)

    def reverse(self) -> Vector[A]:  # type: ignore
        sequence = list(self)
        sequence.reverse()
        return self.__class__(sequence)

    def copy(self) -> Vector[A]:
        return self.__class__(list(self))

    def is_empty(self) -> bool:
        return 0 == len(self)

    def non_empty(self) -> bool:
        return 0 < len(self)

    def size(self) -> int:
        return len(self)

    def map[B](self, function_: Callable[[A], B], /) -> Vector[B]:
        return cast(Vector[B], self.__class__([function_(element) for element in self]))

    def reduce(self, function: Callable[[A, A], A], /) -> A:
        return reduce(function, self)

    def filter(self, function: Callable[[A], bool], /) -> Vector[A]:
        return self.__class__([element for element in self if function(element)])
