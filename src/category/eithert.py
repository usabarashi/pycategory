"""EitherT"""
from __future__ import annotations

from collections.abc import Generator
from copy import deepcopy
from typing import Any, Callable, Generic, Type, TypeVar, cast

from category.either import Either, Left, Right
from category.future import ExecutionContext, Future
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

    def __iter__(self) -> Generator[EitherTTry[L, R], None, R]:
        lift: Callable[[R], EitherTTry[L, R]] = lambda right: EitherTTry[L, R](
            Success[Either[L, R]](Right[L, R](right))
        )
        match self._value:
            case Failure() as failure:
                yield self.flatmap(lift)
                raise GeneratorExit(self) from failure.exception
            case Success(Left()):
                yield self.flatmap(lift)
                raise GeneratorExit(self)
            case Success(Right(value)):
                yield self.flatmap(lift)
                return value
            case _:
                raise ValueError(self)

    @staticmethod
    def send(monad: EitherTTry[L, R], /) -> R:
        return monad.get()

    @staticmethod
    def lift(value: R) -> EitherTTry[L, R]:
        return EitherTTry[L, R](Success[Either[L, R]](Right[L, R](value)))

    def get(self) -> R:
        return self._value.get().get()

    def get_or_else(self, default: Callable[..., EE], /) -> EE | R:
        match self._value.pattern:
            case Failure() as failure:
                raise failure.exception
            case Success(either):
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
            case Success(Left()):
                return cast(EitherTTry[L, RR], deepcopy(self))
            case Success(Right(value)):
                return functor(value)
            case _:
                raise ValueError(self)

    def fold(self, *, left: Callable[[L], U], right: Callable[[R], U]) -> Try[U]:
        def catamorphism(either: Either[L, R]) -> U:
            match either.pattern:
                case Left(value):
                    return left(value)
                case Right(value):
                    return right(value)

        return self._value.map(catamorphism)

    def method(self, functor: Callable[[EitherTTry[L, R]], TT], /) -> TT:
        return functor(self)


EitherTTryDo = Generator[EitherTTry[L, R], Any, R]


class EitherTFuture(Monad, Generic[L, R]):
    """Either Transformer Future"""

    def __init__(self, value: Future[Either[L, R]], /):
        self._value = value

    def __bool__(self) -> bool:
        future = self._value
        if not future.done():
            return False
        else:
            match future.value.pattern:
                case Failure():
                    return False
                case Success(either):
                    return bool(either)

    def __iter__(self) -> Generator[EitherTFuture[L, R], None, R]:
        lift: Callable[[R], EitherTFuture[L, R]] = lambda right: EitherTFuture[L, R](
            Future[Either[L, R]].successful(Right[L, R](right))
        )
        try:
            match self._value.result().pattern:
                case Left():
                    yield self.flatmap(lift)(ExecutionContext)
                    raise GeneratorExit(self)
                case Right(value):
                    yield self.flatmap(lift)(ExecutionContext)
                    return value
        except Exception as error:
            future = Future[Either[L, R]]()
            future.set_exception(error)

            yield EitherTFuture[L, R](future)
            raise GeneratorExit from error

    @staticmethod
    def send(monad: EitherTFuture[L, R]) -> R:
        return monad.get()

    @staticmethod
    def lift(value: R) -> EitherTFuture[L, R]:
        return EitherTFuture[L, R](Future[Either[L, R]].successful(Right[L, R](value)))

    def get(self) -> R:
        return self._value.result().get()

    def get_or_else(self, default: Callable[..., EE], /) -> EE | R:
        try:
            either = self._value.result()
            return either.get_or_else(default)
        except Exception:
            return default()

    def map(
        self, functor: Callable[[R], RR], /
    ) -> Callable[[Type[ExecutionContext]], EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext], /) -> EitherTFuture[L, RR]:
            future = self._value
            mapped_future = future.map(lambda either: either.map(functor))(ec)
            return EitherTFuture[L, RR](mapped_future)

        return with_context

    def flatmap(
        self, functor: Callable[[R], EitherTFuture[L, RR]], /
    ) -> Callable[[Type[ExecutionContext]], EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext], /) -> EitherTFuture[L, RR]:
            # FIXME: Threaded processing
            try:
                match self._value.result().pattern:
                    case Left(value):
                        left = Left[L, RR](value)
                        future = Future[Left[L, RR]].successful(left)
                        return EitherTFuture[L, RR](future)
                    case Right(value):
                        return functor(value)
            except Exception as error:
                future = Future[Either[L, RR]]()
                future.set_exception(exception=error)
                return EitherTFuture[L, RR](future)

        return with_context

    def fold(
        self, *, left: Callable[[L], U], right: Callable[[R], U]
    ) -> Callable[[Type[ExecutionContext]], Future[U]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[U]:
            def catamorphism(either: Either[L, R], /) -> U:
                match either.pattern:
                    case Left(value):
                        return left(value)
                    case Right(value):
                        return right(value)

            future = self._value
            return future.map(catamorphism)(ec)

        return with_context

    def method(self, functor: Callable[[EitherTFuture[L, R]], TT], /) -> TT:
        return functor(self)


EitherTFutureDo = Generator[EitherTFuture[L, R], Any, R]
