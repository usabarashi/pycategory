"""EitherT"""
from __future__ import annotations

from collections.abc import Generator
from typing import Any, Callable, Generic, Type, TypeVar

from category.either import Either, Left, Right
from category.future import ExecutionContext, Future
from category.try_ import Failure, Success, Try

L = TypeVar("L", covariant=True)
R = TypeVar("R", covariant=True)
RR = TypeVar("RR")
EE = TypeVar("EE")
TT = TypeVar("TT")
U = TypeVar("U")


class EitherTTry(Generic[L, R]):
    """Either Transformer Try"""

    def __init__(self, value: Try[Either[L, R]], /):
        self._value = value

    def __bool__(self) -> bool:
        try_ = self._value
        if isinstance(try_.pattern, Failure):
            return False
        else:
            either = try_.pattern.get()
            return bool(either)

    def __call__(self) -> Generator[Try[Either[L, R]], None, R]:
        try_ = self._value
        if isinstance(try_.pattern, Failure):
            yield try_.pattern
            raise GeneratorExit(self) from try_.pattern.exception
        else:
            either = try_.pattern.get()
            if isinstance(either.pattern, Left):
                yield try_.pattern
                raise GeneratorExit(self)
            else:
                yield try_.pattern
                return either.pattern.get()

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
        try_ = self._value
        if isinstance(try_.pattern, Failure):
            exception: Exception = try_.pattern.exception
            failure = Failure[Either[L, RR]](exception)
            return EitherTTry[L, RR](failure)
        else:
            either = try_.pattern.get()
            if isinstance(either.pattern, Left):
                left = Left[L, RR](either.pattern.left().get())
                success = Success[Left[L, RR]](left)
                return EitherTTry[L, RR](success)
            else:
                return functor(either.pattern.right().get())

    def fold(self, *, left: Callable[[L], U], right: Callable[[R], U]) -> Try[U]:
        def catamorphism(either: Either[L, R]) -> U:
            if isinstance(either.pattern, Left):
                return left(either.pattern.left().get())
            else:
                return right(either.pattern.right().get())

        return self._value.map(catamorphism)

    def method(self, functor: Callable[[EitherTTry[L, R]], TT], /) -> TT:
        return functor(self)

    @staticmethod
    def do(
        generator_fuction: Callable[..., EitherTTryDo[L, R]]
    ) -> Callable[..., EitherTTry[L, R]]:
        def impl(*args: Any, **kwargs: Any) -> EitherTTry[L, R]:
            def recur(
                generator: EitherTTryDo[L, R], prev: Any | EitherTTry[L, Any]
            ) -> EitherTTry[L, R]:
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    right = Right[L, R](last.value)
                    success = Success[Either[L, R]](right)
                    return EitherTTry[L, R](success)
                if isinstance(result, Try):
                    try_ = result
                    if isinstance(try_.pattern, Failure):
                        return EitherTTry[L, R](try_.pattern)
                    if isinstance(try_.pattern, Success) and isinstance(
                        try_.pattern.get().pattern, Left
                    ):
                        return EitherTTry[L, R](try_)
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


EitherTTryDo = Generator[Any | Try[Either[L, Any]], Any | Try[Either[L, Any]], R]


class EitherTFuture(Generic[L, R]):
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

    def __call__(self) -> Generator[Try[Either[L, R]], None, R]:
        try:
            either = self._value.result()
            if isinstance(either.pattern, Left):
                yield Success[Either[L, R]](either.pattern)
                raise GeneratorExit(self)
            else:
                yield Success[Either[L, R]](either.pattern)
                return either.pattern.right().get()
        except Exception as error:
            yield Failure[Either[L, R]](error)
            raise GeneratorExit from error

    def get(self) -> R:
        return self._value.result().get()

    def get_or_else(self, default: Callable[..., EE], /) -> EE | R:
        try:
            either = self._value.result()
            return either.get_or_else(default)
        except Exception:
            return default()

    def map(self, functor: Callable[[R], RR], /) -> Callable[..., EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext], /) -> EitherTFuture[L, RR]:
            future = self._value
            mapped_future = future.map(lambda either: either.map(functor))(ec)
            return EitherTFuture[L, RR](mapped_future)

        return with_context

    def flatmap(
        self, functor: Callable[[R], EitherTFuture[L, RR]], /
    ) -> Callable[..., EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext], /) -> EitherTFuture[L, RR]:
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

        return with_context

    def fold(
        self, *, left: Callable[[L], U], right: Callable[[R], U]
    ) -> Callable[[Type[ExecutionContext]], Future[U]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[U]:
            def catamorphism(either: Either[L, R]) -> U:
                if isinstance(either.pattern, Left):
                    return left(either.pattern.left().get())
                else:
                    return right(either.pattern.right().get())

            future = self._value
            return future.map(catamorphism)(ec)

        return with_context

    def method(self, functor: Callable[[EitherTFuture[L, R]], TT], /) -> TT:
        return functor(self)

    @staticmethod
    def do(
        generator_fuction: Callable[..., EitherTFutureDo[L, R]]
    ) -> Callable[..., EitherTFuture[L, R]]:
        def impl(*args: Any, **kwargs: Any) -> EitherTFuture[L, R]:
            def recur(
                generator: EitherTFutureDo[L, R],
                prev: Any | EitherTFuture[L, Any],
            ) -> EitherTFuture[L, R]:
                try:
                    result: Try[Either[L, R]] | Any = generator.send(prev)
                except StopIteration as last:
                    right = Right[L, R](last.value)
                    future = Future[Right[L, R]].successful(right)
                    return EitherTFuture[L, R](future)
                if isinstance(result, Try):
                    try_ = result
                    if isinstance(try_.pattern, Failure):
                        future = Future[Either[L, R]]()
                        future.set_exception(exception=try_.pattern.exception)
                        return EitherTFuture[L, R](future)
                    if isinstance(try_.pattern, Success) and isinstance(
                        try_.pattern.get().pattern, Left
                    ):
                        left: Left[L, R] = try_.pattern.value.pattern
                        future = Future[Left[L, R]].successful(left)
                        return EitherTFuture[L, R](future)
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


EitherTFutureDo = Generator[Any | Try[Either[L, Any]], Any | Try[Either[L, Any]], R]
