"""Functor"""

from __future__ import annotations

from typing import Any, Callable

from pycategory import function_


class Functor[A]:
    """Functor

    class Functor f where
        fmap :: (a -> b) -> f a -> f b
    """

    def map[B](self, function_: Callable[[A], B], /) -> Functor[B]:
        raise NotImplementedError()


def identity_law(F: Functor[Any], /) -> bool:
    """fmap id = id"""
    return F.map(lambda value: value) == F


def composite_law[
    A, B
](*, F: Functor[A], f: Callable[[B], Any], g: Callable[[A], B],) -> bool:
    f_ = function_.Function1(f)
    g_ = function_.Function1(g)

    _ = f_.compose(g_)
    _ = g_.compose(f_)
    _ = f_.and_then(g_)
    _ = g_.and_then(f_)

    """fmap (f . g) = fmap f . fmap g"""
    return F.map(f_.compose(g_)) == F.map(g).map(f)
