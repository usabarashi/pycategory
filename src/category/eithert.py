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
        try_pattern = self.value.pattern()
        if convert is not None:
            yield convert(try_pattern)
            raise GeneratorExit(self)
        # Failure[Either[L, R]] case
        if isinstance(try_pattern, Failure):
            yield try_pattern
            raise GeneratorExit(self) from try_pattern.value
        # Success[Eihter[L, R]] case
        else:
            either_pattern = try_pattern.value.pattern()
            # Success[Left[L , R]] case
            if isinstance(either_pattern, Left):
                yield try_pattern
                raise GeneratorExit(self)
            # Success[Right[L, R]] case
            else:
                yield try_pattern
                return either_pattern.value

    def get(self) -> R:
        try_pattern = self.value.pattern()
        if isinstance(try_pattern, Failure):
            raise ValueError(self)
        else:
            either_pattern = try_pattern.value.pattern()
            if isinstance(either_pattern, Left):
                raise ValueError(self)
            else:
                return either_pattern.value

    def get_or_else(self, default: Callable[..., EE]) -> Union[EE, R]:
        try_pattern = self.value.pattern()
        if isinstance(try_pattern, Failure):
            return default()
        else:
            either_pattern = try_pattern.value.pattern()
            if isinstance(either_pattern, Left):
                return default()
            else:
                return either_pattern.value

    def map(self, functor: Callable[[R], RR]) -> EitherTTry[L, RR]:
        try_pattern = self.value.pattern()
        # Failure case
        if isinstance(try_pattern, Failure):
            exception: Exception = try_pattern.value
            failure = Failure[Either[L, RR]](value=exception)
            return EitherTTry[L, RR](value=failure)
        # Success[Either[L, R]] case
        else:
            either_pattern = try_pattern.value.pattern()
            # Success[Left[L, R]] case
            if isinstance(either_pattern, Left):
                left = Left[L, RR](value=either_pattern.value)
                success = Success[Left[L, RR]](value=left)
                return EitherTTry[L, RR](value=success)
            # Success[Right[L, R]] case
            else:
                mapped_value = functor(either_pattern.value)
                right = Right[L, RR](value=mapped_value)
                success = Success[Right[L, RR]](value=right)
                return EitherTTry[L, RR](value=success)

    def flatmap(self, functor: Callable[[R], EitherTTry[L, RR]]) -> EitherTTry[L, RR]:
        try_pattern = self.value.pattern()
        # Failure case
        if isinstance(try_pattern, Failure):
            exception: Exception = try_pattern.value
            failure = Failure[Either[L, RR]](value=exception)
            return EitherTTry[L, RR](value=failure)
        # Success[Either[L, R]] case
        else:
            either_pattern = try_pattern.value.pattern()
            # Success[Left[L, R]] case
            if isinstance(either_pattern, Left):
                left = Left[L, RR](value=either_pattern.value)
                success = Success[Left[L, RR]](value=left)
                return EitherTTry[L, RR](value=success)
            # Success[Right[L, R]] case
            else:
                return functor(either_pattern.value)

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
                    try_pattern = result.pattern()
                    # Failure[EitherL, R] case
                    if isinstance(try_pattern, Failure):
                        return EitherTTry[L, R](value=try_pattern)
                    # Success[Left[L, R]] case
                    elif isinstance(try_pattern.value, Left):
                        return EitherTTry[L, R](value=result)
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
            either_pattern = self.value.result().pattern()
            if convert is not None:
                yield convert(Success[Either[L, R]](value=either_pattern))
                raise GeneratorExit(self)
            # Success[Left[L , R]] case
            if isinstance(either_pattern, Left):
                yield Success[Either[L, R]](value=either_pattern)
                raise GeneratorExit(self)
            # Success[Right[L, R]] case
            else:
                yield Success[Either[L, R]](value=either_pattern)
                return either_pattern.value

        # Failure[Either[L, R]] case
        except Exception as error:
            if convert is not None:
                yield convert(Failure(value=error))
                raise GeneratorExit(error) from error
            else:
                raise GeneratorExit from error

    def get(self) -> R:
        try:
            either_pattern = self.value.result().pattern()
            if isinstance(either_pattern, Left):
                raise ValueError(self)
            else:
                return either_pattern.value
        except Exception as error:
            raise error

    def get_or_else(self, default: Callable[..., EE]) -> Union[EE, R]:
        try:
            either_pattern = self.value.result().pattern()
            if isinstance(either_pattern, Left):
                return default()
            else:
                return either_pattern.value
        except Exception:
            return default()

    def map(self, functor: Callable[[R], RR]) -> Callable[..., EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext]) -> EitherTFuture[L, RR]:
            def transformer(either: Either[L, R]) -> Either[L, RR]:
                either_pattern = either.pattern()
                if isinstance(either_pattern, Left):
                    return Left[L, RR](value=either_pattern.value)
                else:
                    mapped_value = functor(either_pattern.value)
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
                either_pattern = self.value.result().pattern()
                if isinstance(either_pattern, Left):
                    left = Left[L, RR](value=either_pattern.value)
                    future = Future[Left[L, RR]].successful(value=left)
                    return EitherTFuture[L, RR](value=future)
                else:
                    return functor(either_pattern.value)
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
                    try_pattern = result.pattern()
                    # Failure case
                    if isinstance(try_pattern, Failure):
                        future = Future[Either[L, R]]()
                        future.set_exception(exception=try_pattern.value)
                        return EitherTFuture[L, R](value=future)
                    # Success[Left[L, R]] case
                    elif isinstance(try_pattern.value, Left):
                        left: Left[L, R] = try_pattern.value
                        future = Future[Left[L, R]].successful(value=left)
                        return EitherTFuture[L, R](value=future)
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


EitherTFutureDo = Generator[Union[Any, Try[Either[L, R]]], Any, R]
EitherTFutureGenerator = Generator[
    Union[Any, Try[Either[L, R]]], Union[Any, Try[Either[L, R]]], R
]
