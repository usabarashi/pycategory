from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Generic, TypeVar

from . import curry_

A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)
C = TypeVar("C", covariant=True)


@curry_.curry
def functor(self: Functor[A], other: Callable[[A], B]) -> Functor[B]:
    raise NotImplementedError


class Functor(Generic[A]):
    map = abstractmethod(functor)

    @abstractmethod
    def get(self) -> A:
        raise NotImplementedError


@curry_.curry
def functor2(self: Functor[A, B], other: Callable[[B], C]) -> Functor2[A, C]:
    raise NotImplementedError


class Functor2(Generic[A, B]):
    map = abstractmethod(functor2)

    @abstractmethod
    def get(self) -> B:
        raise NotImplementedError
