from __future__ import annotations

from abc import abstractmethod
from typing import Callable, TypeVar

from . import curry_, functor

A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)
C = TypeVar("C", covariant=True)


@curry_.curry
def applicative(
    self: Applicative[A], other: Applicative[Callable[[A], B]]
) -> Applicative[B]:
    raise NotImplementedError


class Applicative(functor.Functor[A]):
    ap = abstractmethod(applicative)


@curry_.curry
def applicative2(
    self: Applicative2[A, B], other: Applicative2[Callable[[B], C]]
) -> Applicative2[A, C]:
    raise NotImplementedError


class Applicative2(functor.Functor2[A, B]):
    ap = abstractmethod(applicative)
