from __future__ import annotations

from typing import Callable, TypeVar

from . import functor

A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)


class ApplicativeFunctor(functor.Functor[A]):
    """Applicative Functor

    class (Functor f) => Applicative f where
        pure :: a -> f a
        (<*>) :: f (a -> b) -> f a -> f b
    """

    @staticmethod
    def pure(value: A) -> ApplicativeFunctor[A]:
        raise NotImplementedError

    def ap(
        self: ApplicativeFunctor[A], other: ApplicativeFunctor[Callable[[A], B]]
    ) -> ApplicativeFunctor[B]:
        raise NotImplementedError
