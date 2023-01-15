from __future__ import annotations

from typing import Callable, Generic, TypeVar

from . import function_

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
    f: Callable[[B], C],
    g: Callable[[A], B],
) -> bool:

    f_ = function_.Function1(f)
    g_ = function_.Function1(g)

    _ = f_.compose(g_)
    _ = g_.compose(f_)
    _ = f_.and_then(g_)
    _ = g_.and_then(f_)

    """fmap (f . g) = fmap f . fmap g"""
    return F.map(f_.compose(g_)) == F.map(g).map(f)
