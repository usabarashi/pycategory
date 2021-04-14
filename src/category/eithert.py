"""EitherT"""
from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass
from typing import Any, Callable, Generic, Type, TypeVar, Union

from category.either import Either, Left, Right
from category.future import ExecutionContext, Future
from category.try_ import Failure, Success, Try

L = TypeVar("L")
R = TypeVar("R")
RR = TypeVar("RR")
EE = TypeVar("EE")
TT = TypeVar("TT")
U = TypeVar("U")


@dataclass(frozen=True)
class EitherTTry(Generic[L, R]):
    """Either Transformer Try"""

    value: Try[Either[L, R]]

    def __new__(cls, value: Try[Either[L, R]], /):
        return super().__new__(cls)

    def __bool__(self) -> bool:
        try_ = self.value
        if isinstance(try_.pattern, Failure):
            return False
        else:
            either = try_.pattern.value
            return bool(either)

    def __call__(self) -> Generator[Try[Either[L, R]], None, R]:
        try_ = self.value
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
        return self.value.get().get()

    def get_or_else(self, default: Callable[..., EE], /) -> Union[EE, R]:
        try_ = self.value
        if isinstance(try_.pattern, Failure):
            raise try_.pattern.exception
        else:
            either = try_.pattern.get()
            return either.get_or_else(default)

    def map(self, functor: Callable[[R], RR], /) -> EitherTTry[L, RR]:
        try_ = self.value
        mapped_try = try_.map(lambda either: either.map(functor))
        return EitherTTry[L, RR](mapped_try)

    def flatmap(
        self, functor: Callable[[R], EitherTTry[L, RR]], /
    ) -> EitherTTry[L, RR]:
        try_ = self.value
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

        return self.value.map(catamorphism)

    def method(self, functor: Callable[[EitherTTry[L, R]], TT], /) -> TT:
        return functor(self)

    @staticmethod
    def do(
        generator_fuction: Callable[..., EitherTTryDo[L, R]]
    ) -> Callable[..., EitherTTry[L, R]]:
        def impl(*args: Any, **kwargs: Any) -> EitherTTry[L, R]:
            def recur(
                generator: EitherTTryDo[L, R], prev: Union[Any, EitherTTry[L, Any]]
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
                        try_.pattern.value.pattern, Left
                    ):
                        return EitherTTry[L, R](try_)
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


EitherTTryDo = Generator[
    Union[Any, Try[Either[L, Any]]], Union[Any, Try[Either[L, Any]]], R
]


@dataclass(frozen=True)
class EitherTFuture(Generic[L, R]):
    """Either Transformer Future"""

    value: Future[Either[L, R]]

    def __new__(cls, value: Future[Either[L, R]], /):
        return super().__new__(cls)

    def __bool__(self) -> bool:
        future = self.value
        if not future.done():
            return False
        else:
            try_ = future.value
            if isinstance(try_.pattern, Failure):
                return False
            else:
                either = try_.pattern.value
                return bool(either)

    def __call__(self) -> Generator[Try[Either[L, R]], None, R]:
        try:
            either = self.value.result()
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
        return self.value.result().get()

    def get_or_else(self, default: Callable[..., EE], /) -> Union[EE, R]:
        try:
            either = self.value.result()
            return either.get_or_else(default)
        except Exception:
            return default()

    def map(self, functor: Callable[[R], RR], /) -> Callable[..., EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext], /) -> EitherTFuture[L, RR]:
            future = self.value
            mapped_future = future.map(lambda either: either.map(functor))(ec)
            return EitherTFuture[L, RR](mapped_future)

        return with_context

    def flatmap(
        self, functor: Callable[[R], EitherTFuture[L, RR]], /
    ) -> Callable[..., EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext], /) -> EitherTFuture[L, RR]:
            # FIXME: Threaded processing
            try:
                either = self.value.result()
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

            future = self.value
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
                prev: Union[Any, EitherTFuture[L, Any]],
            ) -> EitherTFuture[L, R]:
                try:
                    result: Union[Try[Either[L, R]], Any] = generator.send(prev)
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
                        try_.pattern.value.pattern, Left
                    ):
                        left: Left[L, R] = try_.pattern.value.pattern
                        future = Future[Left[L, R]].successful(left)
                        return EitherTFuture[L, R](future)
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


EitherTFutureDo = Generator[
    Union[Any, Try[Either[L, Any]]], Union[Any, Try[Either[L, Any]]], R
]
