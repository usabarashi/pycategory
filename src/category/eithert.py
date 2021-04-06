from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generator, Generic, Optional, Type, TypeVar, Union

from category.either import Either, Left, Right
from category.future import ExecutionContext, Future
from category.try_ import Failure, Success, Try

L = TypeVar("L")
R = TypeVar("R")
RR = TypeVar("RR")
EE = TypeVar("EE")


@dataclass(frozen=True)
class EitherTTry(Generic[L, R]):
    """Either Transformer Try"""

    value: Try[Either[L, R]]

    def __bool__(self) -> bool:
        # Success and Right
        return bool(self.value) and bool(self.value.value)

    def __call__(
        self, /, convert: Optional[Callable[[Try[Either[L, R]]], EE]] = None
    ) -> Generator[Union[EE, Try[Either[L, R]]], None, R]:
        try_ = self.value
        if convert is not None:
            yield convert(try_)
            raise GeneratorExit(self)
        # Failure[Either[L, R]] case
        if isinstance(try_.pattern, Failure):
            yield try_.pattern
            raise GeneratorExit(self) from try_.pattern.value
        # Success[Eihter[L, R]] case
        else:
            either = try_.pattern.value
            # Success[Left[L , R]] case
            if isinstance(either.pattern, Left):
                yield try_.pattern
                raise GeneratorExit(self)
            # Success[Right[L, R]] case
            else:
                yield try_.pattern
                return either.pattern.value

    def get(self) -> R:
        try_ = self.value
        if isinstance(try_.pattern, Failure):
            raise ValueError(self)
        else:
            either = try_.pattern.value
            if isinstance(either.pattern, Left):
                raise ValueError(self)
            else:
                return either.pattern.value

    def get_or_else(self, default: Callable[..., EE]) -> Union[EE, R]:
        try_ = self.value
        if isinstance(try_.pattern, Failure):
            return default()
        else:
            either = try_.pattern.value
            if isinstance(either.pattern, Left):
                return default()
            else:
                return either.pattern.value

    def map(self, functor: Callable[[R], RR]) -> EitherTTry[L, RR]:
        try_ = self.value
        # Failure case
        if isinstance(try_.pattern, Failure):
            exception: Exception = try_.pattern.value
            failure = Failure[Either[L, RR]](value=exception)
            return EitherTTry[L, RR](value=failure)
        # Success[Either[L, R]] case
        else:
            either = try_.pattern.value
            # Success[Left[L, R]] case
            if isinstance(either.pattern, Left):
                left = Left[L, RR](value=either.pattern.value)
                success = Success[Left[L, RR]](value=left)
                return EitherTTry[L, RR](value=success)
            # Success[Right[L, R]] case
            else:
                mapped_value = functor(either.pattern.value)
                right = Right[L, RR](value=mapped_value)
                success = Success[Right[L, RR]](value=right)
                return EitherTTry[L, RR](value=success)

    def flatmap(self, functor: Callable[[R], EitherTTry[L, RR]]) -> EitherTTry[L, RR]:
        try_ = self.value
        # Failure case
        if isinstance(try_.pattern, Failure):
            exception: Exception = try_.pattern.value
            failure = Failure[Either[L, RR]](value=exception)
            return EitherTTry[L, RR](value=failure)
        # Success[Either[L, R]] case
        else:
            either = try_.pattern.value
            # Success[Left[L, R]] case
            if isinstance(either.pattern, Left):
                left = Left[L, RR](value=either.pattern.value)
                success = Success[Left[L, RR]](value=left)
                return EitherTTry[L, RR](value=success)
            # Success[Right[L, R]] case
            else:
                return functor(either.pattern.value)

    @staticmethod
    def do(
        generator_fuction: Callable[..., EitherTTryGenerator[L, R]]
    ) -> Callable[..., EitherTTry[L, R]]:
        def impl(
            *args: Any, **kwargs: Any
        ) -> Union[Success[Left[L, R]], Success[Right[L, R]]]:
            def recur(
                generator: EitherTTryGenerator[L, R],
                prev: Any,
            ) -> EitherTTry[L, R]:
                try:
                    result: Union[Any, Try[Either[L, R]]] = generator.send(prev)
                except StopIteration as last:
                    right = Right[L, R](value=last.value)
                    success = Success[Either[L, R]](value=right)
                    return EitherTTry[L, R](value=success)
                if isinstance(result, Try):
                    try_ = result
                    # Failure[EitherL, R] case
                    if isinstance(try_.pattern, Failure):
                        return EitherTTry[L, R](value=try_.pattern)
                    # Success[Left[L, R]] case
                    else:
                        either = try_.pattern.value
                        if isinstance(either.pattern, Left):
                            return EitherTTry[L, R](value=try_)
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


EitherTTryDo = Generator[Union[Left[L, Any], Right[L, Any], Any], Any, R]
EitherTTryGenerator = Generator[
    Union[Left[L, Any], Right[L, R], Any], Union[Left[L, Any], Right[L, Any], Any], R
]


@dataclass(frozen=True)
class EitherTFuture(Generic[L, R]):
    """Either Transformer Future"""

    value: Future[Either[L, R]]

    def __bool__(self) -> bool:
        # Success and Right
        return bool(self.value) and bool(self.value.value)

    def __call__(
        self, /, convert: Optional[Callable[[Try[Either[L, R]]], EE]] = None
    ) -> Generator[Union[EE, Try[Either[L, R]]], None, R]:
        try:
            either = self.value.result()
            if convert is not None:
                yield convert(Success[Either[L, R]](value=either))
                raise GeneratorExit(self)
            # Success[Left[L , R]] case
            if isinstance(either.pattern, Left):
                yield Success[Either[L, R]](value=either.pattern)
                raise GeneratorExit(self)
            # Success[Right[L, R]] case
            else:
                yield Success[Either[L, R]](value=either.pattern)
                return either.pattern.value

        # Failure[Either[L, R]] case
        except Exception as error:
            if convert is not None:
                yield convert(Failure(value=error))
                raise GeneratorExit(error) from error
            else:
                raise GeneratorExit from error

    def get(self) -> R:
        try:
            either = self.value.result()
            if isinstance(either.pattern, Left):
                raise ValueError(self)
            else:
                return either.pattern.value
        except Exception as error:
            raise error

    def get_or_else(self, default: Callable[..., EE]) -> Union[EE, R]:
        try:
            either = self.value.result()
            if isinstance(either.pattern, Left):
                return default()
            else:
                return either.pattern.value
        except Exception:
            return default()

    def map(self, functor: Callable[[R], RR]) -> Callable[..., EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext]) -> EitherTFuture[L, RR]:
            def transformer(either: Either[L, R]) -> Either[L, RR]:
                if isinstance(either.pattern, Left):
                    return Left[L, RR](value=either.pattern.value)
                else:
                    mapped_value = functor(either.pattern.value)
                    return Right[L, RR](value=mapped_value)

            future = self.value
            mapped_future = future.map(functor=transformer)(ec=ec)
            return EitherTFuture[L, RR](value=mapped_future)

        return with_context

    def flatmap(
        self, functor: Callable[[R], EitherTFuture[L, RR]]
    ) -> Callable[..., EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext]) -> EitherTFuture[L, RR]:
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

    @staticmethod
    def do(
        generator_fuction: Callable[..., EitherTFutureGenerator[L, R]]
    ) -> Callable[..., EitherTFuture[L, R]]:
        def impl(*args: Any, **kwargs: Any) -> EitherTFuture[L, R]:
            def recur(
                generator: EitherTFutureGenerator[L, R],
                prev: Any,
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
                    elif isinstance(try_.pattern.value, Left):
                        left: Left[L, R] = try_.pattern.value
                        future = Future[Left[L, R]].successful(value=left)
                        return EitherTFuture[L, R](value=future)
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


EitherTFutureDo = Generator[Union[Any, Try[Either[L, R]]], Any, R]
EitherTFutureGenerator = Generator[
    Union[Any, Try[Either[L, R]]], Union[Any, Try[Either[L, R]]], R
]