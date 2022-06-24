"""EitherT"""
from __future__ import annotations

from collections.abc import Generator
from copy import deepcopy
from typing import Any, Callable, Generic, Type, TypeVar, cast

from category.either import Either, Left, Right
from category.future import ExecutionContext as ec
from category.future import Future
from category.monad import Monad
from category.try_ import Failure, Success, Try

L = TypeVar("L", covariant=True)
R = TypeVar("R", covariant=True)
RR = TypeVar("RR")
EE = TypeVar("EE")
TT = TypeVar("TT")
U = TypeVar("U")


class EitherTTry(Monad, Generic[L, R]):
    """Either Transformer Try"""

    def __init__(self, value: Try[Either[L, R]], /):
        self._value = value

    def __bool__(self) -> bool:
        match self._value:
            case Success(Right()):
                return True
            case _:
                return False

    def __iter__(
        self,
    ) -> EitherTTryDo[L, R]:
        lift: Callable[[R], EitherTTry[L, R]] = lambda right: EitherTTry[L, R](
            Success[Either[L, R]](Right[L, R](right))
        )
        match self._value:
            case Failure() as failure:
                yield self, EitherTTry.get, lift
                raise GeneratorExit(self) from failure.exception
            case Success(Left()):
                yield self, EitherTTry.get, lift
                raise GeneratorExit(self)
            case Success(Right(value)):
                yield self, EitherTTry.get, lift
                return value
            case _:
                raise ValueError(self)

    def get(self) -> R:
        return self._value.get().get()

    def get_or_else(self, default: Callable[..., EE], /) -> EE | R:
        try_ = self._value
        if isinstance(try_.pattern, Failure):
            raise try_.pattern.exception
        else:
            either = try_.pattern.get()
            return either.get_or_else(default)

    def map(self, functor: Callable[[R], RR], /) -> EitherTTry[L, RR]:
        try_ = self._value
        mapped_try = try_.map(lambda either: either.map(functor))
        return EitherTTry[L, RR](mapped_try)

    def flatmap(
        self, functor: Callable[[R], EitherTTry[L, RR]], /
    ) -> EitherTTry[L, RR]:
        match self._value:
            case Failure():
                return cast(EitherTTry[L, RR], deepcopy(self))
            case Success(either) if isinstance(either, Left):
                return cast(EitherTTry[L, RR], deepcopy(self))
            case Success(either) if isinstance(either, Right):
                return functor(either.get())
            case _:
                raise ValueError(self)

    def fold(self, *, left: Callable[[L], U], right: Callable[[R], U]) -> Try[U]:
        def catamorphism(either: Either[L, R]) -> U:
            if isinstance(either.pattern, Left):
                return left(either.pattern.left().get())
            else:
                return right(either.pattern.right().get())

        return self._value.map(catamorphism)

    def method(self, functor: Callable[[EitherTTry[L, R]], TT], /) -> TT:
        return functor(self)


EitherTTryDo = Generator[
    tuple[
        EitherTTry[L, R],
        Callable[[EitherTTry[L, Any]], Any],
        Callable[[R], EitherTTry[L, R]],
    ],
    tuple[
        EitherTTry[L, R],
        Callable[[EitherTTry[L, Any]], Any],
        Callable[[R], EitherTTry[L, R]],
    ],
    R,
]


class EitherTFuture(Monad, Generic[L, R]):
    """Either Transformer Future"""

    def __init__(self, value: Future[Either[L, R]], /):
        self._value = value

    def __bool__(self) -> bool:
        future = self._value
        if not future.done():
            return False
        else:
            try_ = future.value
            if isinstance(try_.pattern, Failure):
                return False
            else:
                either = try_.pattern.get()
                return bool(either)

    def __iter__(
        self,
    ) -> EitherTFutureDo[L, R]:
        lift: Callable[[R], EitherTFuture[L, R]] = lambda right: EitherTFuture[L, R](
            Future[Either[L, R]].successful(Right[L, R](right))
        )
        try:
            match self._value.result().pattern:
                case Left():
                    yield self.flatmap(ec)(lift), EitherTFuture.get, lift
                    raise GeneratorExit(self)
                case Right(value):
                    yield self.flatmap(ec)(lift), EitherTFuture.get, lift
                    return value
        except Exception as error:
            future = Future[Either[L, R]]()
            future.set_exception(error)

            yield EitherTFuture[L, R](future), EitherTFuture.get, lift
            raise GeneratorExit from error

    def get(self) -> R:
        return self._value.result().get()

    def get_or_else(self, default: Callable[..., EE], /) -> EE | R:
        try:
            either = self._value.result()
            return either.get_or_else(default)
        except Exception:
            return default()

    def map(
        self, ec: Type[ec], /
    ) -> Callable[[Callable[[R], RR]], EitherTFuture[L, RR]]:
        def wrapper(functor: Callable[[R], RR], /) -> EitherTFuture[L, RR]:
            future = self._value
            mapped_future = future.map(ec)(lambda either: either.map(functor))
            return EitherTFuture[L, RR](mapped_future)

        return wrapper

    def flatmap(
        self, ec: Type[ec] = ec, /
    ) -> Callable[[Callable[[R], EitherTFuture[L, RR]]], EitherTFuture[L, RR]]:
        def wrapper(
            functor: Callable[[R], EitherTFuture[L, RR]], /
        ) -> EitherTFuture[L, RR]:
            # FIXME: Threaded processing
            try:
                either = self._value.result()
                if isinstance(either.pattern, Left):
                    left = Left[L, RR](either.pattern.value)
                    future = Future[Left[L, RR]].successful(left)
                    return EitherTFuture[L, RR](future)
                else:
                    return functor(either.pattern.value)
            except Exception as error:
                future = Future[Either[L, RR]]()
                future.set_exception(exception=error)
                return EitherTFuture[L, RR](future)

        return wrapper

    def fold(
        self, *, left: Callable[[L], U], right: Callable[[R], U]
    ) -> Callable[[Type[ec]], Future[U]]:
        def with_context(ec: Type[ec], /) -> Future[U]:
            def catamorphism(either: Either[L, R]) -> U:
                if isinstance(either.pattern, Left):
                    return left(either.pattern.left().get())
                else:
                    return right(either.pattern.right().get())

            future = self._value
            return future.map(ec)(catamorphism)

        return with_context

    def method(self, functor: Callable[[EitherTFuture[L, R]], TT], /) -> TT:
        return functor(self)


EitherTFutureDo = Generator[
    tuple[
        EitherTFuture[L, R],
        Callable[[EitherTFuture[L, R]], R],
        Callable[[R], EitherTFuture[L, R]],
    ],
    tuple[
        EitherTFuture[L, R],
        Callable[[EitherTFuture[L, R]], R],
        Callable[[R], EitherTFuture[L, R]],
    ],
    R,
]
