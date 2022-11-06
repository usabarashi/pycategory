from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Generic, TypeVar

A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)
C = TypeVar("C", covariant=True)


class Functor(Generic[A]):
    def map(self: Functor[A], functor: Callable[[A], B], /) -> Functor[B]:
        """functor: (a -> b) -> self: f a -> return: f b"""
        raise NotImplementedError


class Functor2(Generic[A, B]):
    @abstractmethod
    def map(self: Functor2[A, B], functor: Callable[[B], C], /) -> Functor2[A, C]:
        """functor: (a -> b) -> self: f a -> return: f b"""
        raise NotImplementedError
