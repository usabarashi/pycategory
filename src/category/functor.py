"""Functor"""
from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

from . import function_

Ap = TypeVar("Ap", covariant=True)
Bp = TypeVar("Bp", covariant=True)


class Functor(Generic[Ap]):
    """Functor

    class Functor f where
        fmap :: (a -> b) -> f a -> f b
    """

    def map(self, function_: Callable[[Ap], Bp], /) -> Functor[Bp]:
        raise NotImplementedError()


def identity_law(F: Functor[Any], /) -> bool:
    """fmap id = id"""
    return F.map(lambda value: value) == F


def composite_law(
    *,
    F: Functor[Ap],
    f: Callable[[Bp], Any],
    g: Callable[[Ap], Bp],
) -> bool:
    f_ = function_.Function1(f)
    g_ = function_.Function1(g)

    _ = f_.compose(g_)
    _ = g_.compose(f_)
    _ = f_.and_then(g_)
    _ = g_.and_then(f_)

    """fmap (f . g) = fmap f . fmap g"""
    return F.map(f_.compose(g_)) == F.map(g).map(f)
