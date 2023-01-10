from __future__ import annotations

from typing import Callable, Generic, TypeVar

A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)
C = TypeVar("C", covariant=True)


class Functor(Generic[A]):
    """Functor

    class Functor f where
        fmap :: (a -> b) -> f a -> f b
    """

    def map(self, function_: Callable[[A], B], /) -> Functor[B]:
        raise NotImplementedError


def identity_law(F: Functor[A], /) -> bool:
    """fmap id = id"""
    return F.map(lambda value: value) == F


def composite_law(
    *,
    F: Functor[A],
    f: Callable[[A], B],
    g: Callable[[B], C],
) -> bool:
    """fmap (f . g) = fmap f . fmap g"""
    return F.map(lambda value: g(f(value))) == F.map(f).map(g)
