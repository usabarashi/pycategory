from __future__ import annotations

from typing import Callable

from pycategory.trait import functor


class Applicative[A](functor.Functor[A]):
    """Applicative Functor

    class (Functor f) => Applicative f where
        pure :: a -> f a
        (<*>) :: f (a -> b) -> f a -> f b
    """

    @staticmethod
    def pure(value: A) -> Applicative[A]:
        raise NotImplementedError()

    def ap[
        B
    ](self, other: Applicative[Callable[[A], B]],) -> Applicative[B]:
        raise NotImplementedError()
