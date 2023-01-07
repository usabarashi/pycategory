from __future__ import annotations

from typing import Callable, Generic, TypeVar

A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)


class Functor(Generic[A]):
    """Functor

    class Functor f where
        fmap :: (a -> b) -> f a -> f b
    """

    def map(self: Functor[A], function: Callable[[A], B], /) -> Functor[B]:
        raise NotImplementedError
