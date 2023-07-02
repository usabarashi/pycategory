from __future__ import annotations

from typing import Callable, TypeVar

from . import functor

A = TypeVar("A")
Ap = TypeVar("Ap", covariant=True)
Bp = TypeVar("Bp", covariant=True)


class Applicative(functor.Functor[Ap]):
    """Applicative Functor

    class (Functor f) => Applicative f where
        pure :: a -> f a
        (<*>) :: f (a -> b) -> f a -> f b
    """

    @staticmethod
    def pure(value: A) -> Applicative[A]:
        raise NotImplementedError()

    def ap(
        self: Applicative[Ap],
        other: Applicative[Callable[[Ap], Bp]],
    ) -> Applicative[Bp]:
        raise NotImplementedError()
