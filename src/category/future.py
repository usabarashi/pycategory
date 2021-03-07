from __future__ import annotations

import dataclasses
from typing import Callable, Generic, NoReturn, TypeVar

from category.try_ import Success, TryST

T = TypeVar("T")
TT = TypeVar("TT")


@dataclasses.dataclass(frozen=True)
class Future(Generic[T]):
    value: TryST[T]

    def on_complete(self, functor: Callable[[TryST[T]], NoReturn]) -> NoReturn:
        functor(self.value)

    def transform(self, functor: Callable[[TryST[T]], TryST[TT]]) -> Future[TT]:
        return Future(value=functor(self.value))

    def transform_with(self, functor: Callable[[TryST[T]], Future[TT]]) -> Future[TT]:
        return functor(self.value)

    @staticmethod
    def successful(value: T) -> Future[T]:
        return Future[T](value=Success(value=value))


@dataclasses.dataclass(frozen=True)
class Promise(Generic[T]):
    value: TryST[T]

    @property
    def future(self) -> Future[T]:
        return Future[T](value=self.value)

    def try_complete(self, result: TryST[T]) -> bool:
        """try_comple

        False: Already set the value.
        True: I was able to set the value.
        """
        return False
