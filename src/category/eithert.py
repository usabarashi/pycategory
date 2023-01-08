"""EitherT"""
from __future__ import annotations

from collections.abc import Generator
from functools import wraps
from typing import Any, Callable, Generic, ParamSpec, TypeAlias, TypeVar, cast

from . import either, extension, future, monad, try_

L = TypeVar("L", covariant=True)
R = TypeVar("R", covariant=True)
RR = TypeVar("RR")
EE = TypeVar("EE")
TT = TypeVar("TT")
U = TypeVar("U")
P = ParamSpec("P")


class EitherTTry(Generic[L, R], monad.Monad[R], extension.Extension):
    """Either Transformer Try"""

    def __init__(self, value: try_.Try[either.Either[L, R]], /):
        self._value = value

    def __iter__(self) -> Generator[EitherTTry[L, R], None, R]:
        match self._value:
            case try_.Failure() as failure:
                raise GeneratorExit(self) from failure.exception
            case try_.Success(either.Left()):
                raise GeneratorExit(self)
            case try_.Success(either.Right(value)):
                yield self
                return value
            case _:
                raise ValueError(self)

    @staticmethod
    def pure(value: R) -> EitherTTry[L, R]:
        return EitherTTry[L, R](
            try_.Success[either.Either[L, R]](either.Right[L, R](value))
        )

    def get(self) -> R:
        return self._value.get().get()

    def get_or_else(self, default: Callable[..., EE], /) -> EE | R:
        match self._value.pattern:
            case try_.Failure() as failure:
                raise failure.exception
            case try_.Success(either_):
                return either_.get_or_else(default)

    def map(self, function_: Callable[[R], RR], /) -> EitherTTry[L, RR]:
        try__ = self._value
        mapped_try = try__.map(lambda either_: either_.map(function_))
        return EitherTTry[L, RR](mapped_try)

    def flat_map(
        self, function_: Callable[[R], EitherTTry[L, RR]], /
    ) -> EitherTTry[L, RR]:
        match self._value:
            case try_.Failure():
                return cast(EitherTTry[L, RR], self)
            case try_.Success(either.Left()):
                return cast(EitherTTry[L, RR], self)
            case try_.Success(either.Right(value)):
                return function_(value)
            case _:
                raise ValueError(self)

    def fold(self, *, left: Callable[[L], U], right: Callable[[R], U]) -> try_.Try[U]:
        def catamorphism(either_: either.Either[L, R]) -> U:
            match either_.pattern:
                case either.Left(value):
                    return left(value)
                case either.Right(value):
                    return right(value)

        return self._value.map(catamorphism)

    @staticmethod
    def do(
        context: Callable[P, EitherTTryDo[L, R]], /
    ) -> Callable[P, EitherTTry[L, R]]:
        """map, flat_map combination syntax sugar.

        Only type checking can determine type violations, and runtime errors may not occur.
        """

        @wraps(context)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> EitherTTry[L, R]:
            context_ = context(*args, **kwargs)
            try:
                while True:
                    yield_state = next(context_)
                    if not isinstance(yield_state, EitherTTry):
                        raise TypeError(yield_state)
            except GeneratorExit as exit:
                return cast(EitherTTry[L, R], exit.args[monad.FixedMonad])
            except StopIteration as return_:
                return EitherTTry[L, R].pure(return_.value)

        return wrapper


EitherTTryDo: TypeAlias = Generator[EitherTTry[L, R], Any, R]


class EitherTFuture(Generic[L, R], monad.Monad[R]):
    """Either Transformer Future"""

    def __init__(self, value: future.Future[either.Either[L, R]], /):
        self._value = value

    def __iter__(self) -> Generator[EitherTFuture[L, R], None, R]:
        lift: Callable[[R], EitherTFuture[L, R]] = lambda right: EitherTFuture[L, R](
            future.Future[either.Either[L, R]].successful(either.Right[L, R](right))
        )
        try:
            match self._value.result().pattern:
                case either.Left():
                    raise GeneratorExit(self)
                case either.Right(value):
                    yield self.flat_map(lift)(future.ExecutionContext)
                    return value
        except Exception as error:
            future_ = future.Future[either.Either[L, R]]()
            future_.set_exception(error)
            eithert_future = EitherTFuture[L, R](future_)
            raise GeneratorExit(eithert_future) from error

    @staticmethod
    def pure(value: R) -> EitherTFuture[L, R]:
        return EitherTFuture[L, R](
            future.Future[either.Either[L, R]].successful(either.Right[L, R](value))
        )

    def get(self) -> R:
        return self._value.result().get()

    def get_or_else(self, default: Callable[..., EE], /) -> EE | R:
        try:
            either_ = self._value.result()
            return either_.get_or_else(default)
        except Exception:
            return default()

    def map(
        self, function_: Callable[[R], RR], /
    ) -> Callable[[future.ExecutionContext], EitherTFuture[L, RR]]:
        def with_context(executor: future.ExecutionContext, /) -> EitherTFuture[L, RR]:
            future_ = self._value
            mapped_future = future_.map(lambda either_: either_.map(function_))(
                executor
            )
            return EitherTFuture[L, RR](mapped_future)

        return with_context

    def flat_map(
        self, function_: Callable[[R], EitherTFuture[L, RR]], /
    ) -> Callable[[future.ExecutionContext], EitherTFuture[L, RR]]:
        def with_context(executor: future.ExecutionContext, /) -> EitherTFuture[L, RR]:
            try:
                match self._value.result().pattern:
                    case either.Left(value):
                        left = either.Left[L, RR](value)
                        future_ = future.Future[either.Left[L, RR]].successful(left)
                        return EitherTFuture[L, RR](future_)
                    case either.Right(value):
                        return function_(value)
            except Exception as error:
                future_ = future.Future[either.Either[L, RR]]()
                future_.set_exception(exception=error)
                return EitherTFuture[L, RR](future_)

        return with_context

    def fold(
        self, *, left: Callable[[L], U], right: Callable[[R], U]
    ) -> Callable[[future.ExecutionContext], future.Future[U]]:
        def with_context(executor: future.ExecutionContext, /) -> future.Future[U]:
            def catamorphism(either_: either.Either[L, R], /) -> U:
                match either_.pattern:
                    case either.Left(value):
                        return left(value)
                    case either.Right(value):
                        return right(value)

            future_ = self._value
            return future_.map(catamorphism)(executor)

        return with_context

    @staticmethod
    def do(
        context: Callable[P, EitherTFutureDo[L, R]], /
    ) -> Callable[P, EitherTFuture[L, R]]:
        """map, flat_map combination syntax sugar.

        Only type checking can determine type violations, and runtime errors may not occur.
        """

        @wraps(context)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> EitherTFuture[L, R]:
            context_ = context(*args, **kwargs)
            try:
                while True:
                    yield_state = next(context_)
                    if not isinstance(yield_state, EitherTFuture):
                        raise TypeError(yield_state)
            except GeneratorExit as exit:
                return cast(EitherTFuture[L, R], exit.args[monad.FixedMonad])
            except StopIteration as return_:
                return EitherTFuture[L, R].pure(return_.value)

        return wrapper


EitherTFutureDo: TypeAlias = Generator[EitherTFuture[L, Any], Any, R]
