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

    def __bool__(self) -> bool:
        # Success and Right
        return bool(self.value) and bool(self.value.value)

    def __call__(self) -> Generator[Try[Either[L, R]], None, R]:
        try_ = self.value
        # Failure[Either[L, R]] case
        if isinstance(try_.pattern, Failure):
            yield try_.pattern
            raise GeneratorExit(self) from try_.pattern.value
        # Success[Eihter[L, R]] case
        else:
            either = try_.pattern.get()
            # Success[Left[L , R]] case
            if isinstance(either.pattern, Left):
                yield try_.pattern
                raise GeneratorExit(self)
            # Success[Right[L, R]] case
            else:
                yield try_.pattern
                return either.pattern.get()

    def get(self) -> R:
        return self.value.get().get()

    def get_or_else(self, default: Callable[..., EE]) -> Union[EE, R]:
        try_ = self.value
        if isinstance(try_.pattern, Failure):
            raise try_.pattern.value
        else:
            either = try_.pattern.get()
            return either.get_or_else(default=default)

    def map(self, functor: Callable[[R], RR]) -> EitherTTry[L, RR]:
        try_ = self.value
        mapped_try = try_.map(functor=lambda either: either.map(functor=functor))
        return EitherTTry[L, RR](value=mapped_try)

    def flatmap(self, functor: Callable[[R], EitherTTry[L, RR]]) -> EitherTTry[L, RR]:
        try_ = self.value
        # Failure case
        if isinstance(try_.pattern, Failure):
            exception: Exception = try_.pattern.value
            failure = Failure[Either[L, RR]](value=exception)
            return EitherTTry[L, RR](value=failure)
        # Success[Either[L, R]] case
        else:
            either = try_.pattern.get()
            # Success[Left[L, R]] case
            if isinstance(either.pattern, Left):
                left = Left[L, RR](value=either.pattern.left().get())
                success = Success[Left[L, RR]](value=left)
                return EitherTTry[L, RR](value=success)
            # Success[Right[L, R]] case
            else:
                return functor(either.pattern.right().get())

    def fold(self, left: Callable[[L], U], right: Callable[[R], U]) -> Try[U]:
        def catamorphism(either: Either[L, R]) -> U:
            if isinstance(either.pattern, Left):
                return left(either.pattern.left().get())
            else:
                return right(either.pattern.right().get())

        return self.value.map(functor=catamorphism)

    def method(self, functor: Callable[[EitherTTry[L, R]], TT]) -> TT:
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
                    right = Right[L, R](value=last.value)
                    success = Success[Either[L, R]](value=right)
                    return EitherTTry[L, R](value=success)
                if isinstance(result, Try):
                    try_ = result
                    # Failure case
                    if isinstance(try_.pattern, Failure):
                        return EitherTTry[L, R](value=try_.pattern)
                    # Success[Left[L, R]] case
                    if isinstance(try_.pattern, Success) and isinstance(
                        try_.pattern.value.pattern, Left
                    ):
                        return EitherTTry[L, R](value=try_)
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

    def __bool__(self) -> bool:
        # Complete and Success and Right
        return (
            bool(self.value) and bool(self.value.value) and bool(self.value.value.value)
        )

    def __call__(self) -> Generator[Try[Either[L, R]], None, R]:
        try:
            either = self.value.result()
            # Success[Left[L , R]] case
            if isinstance(either.pattern, Left):
                yield Success[Either[L, R]](value=either.pattern)
                raise GeneratorExit(self)
            # Success[Right[L, R]] case
            else:
                yield Success[Either[L, R]](value=either.pattern)
                return either.pattern.right().get()

        # Failure[Either[L, R]] case
        except Exception as error:
            yield Failure[Either[L, R]](value=error)
            raise GeneratorExit from error

    def get(self) -> R:
        return self.value.result().get()

    def get_or_else(self, default: Callable[..., EE]) -> Union[EE, R]:
        try:
            either = self.value.result()
            return either.get_or_else(default=default)
        except Exception:
            return default()

    def map(self, functor: Callable[[R], RR]) -> Callable[..., EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext], /) -> EitherTFuture[L, RR]:

            future = self.value
            mapped_future = future.map(
                functor=lambda either: either.map(functor=functor)
            )(ec)
            return EitherTFuture[L, RR](value=mapped_future)

        return with_context

    def flatmap(
        self, functor: Callable[[R], EitherTFuture[L, RR]]
    ) -> Callable[..., EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext], /) -> EitherTFuture[L, RR]:
            # FIXME: Threaded processing
            try:
                either = self.value.result()
                if isinstance(either.pattern, Left):
                    left = Left[L, RR](value=either.pattern.value)
                    future = Future[Left[L, RR]].successful(value=left)
                    return EitherTFuture[L, RR](value=future)
                else:
                    return functor(either.pattern.value)
            except Exception as error:
                future = Future[Either[L, RR]]()
                future.set_exception(exception=error)
                return EitherTFuture[L, RR](value=future)

        return with_context

    def fold(
        self, left: Callable[[L], U], right: Callable[[R], U]
    ) -> Callable[[Type[ExecutionContext]], Future[U]]:
        def with_context(ec: Type[ExecutionContext], /) -> Future[U]:
            def catamorphism(either: Either[L, R]) -> U:
                if isinstance(either.pattern, Left):
                    return left(either.pattern.left().get())
                else:
                    return right(either.pattern.right().get())

            future = self.value
            return future.map(functor=catamorphism)(ec)

        return with_context

    def method(self, functor: Callable[[EitherTFuture[L, R]], TT]) -> TT:
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
                    right = Right[L, R](value=last.value)
                    future = Future[Right[L, R]].successful(value=right)
                    return EitherTFuture[L, R](value=future)
                if isinstance(result, Try):
                    try_ = result
                    # Failure case
                    if isinstance(try_.pattern, Failure):
                        future = Future[Either[L, R]]()
                        future.set_exception(exception=try_.pattern.value)
                        return EitherTFuture[L, R](value=future)
                    # Success[Left[L, R]] case
                    if isinstance(try_.pattern, Success) and isinstance(
                        try_.pattern.value.pattern, Left
                    ):
                        left: Left[L, R] = try_.pattern.value.pattern
                        future = Future[Left[L, R]].successful(value=left)
                        return EitherTFuture[L, R](value=future)
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


EitherTFutureDo = Generator[
    Union[Any, Try[Either[L, Any]]], Union[Any, Try[Either[L, Any]]], R
]
