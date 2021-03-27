from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generator, Generic, Optional, Type, TypeVar, Union

from category.either import EitherST, Left, Right
from category.future import ExecutionContext, Future
from category.try_ import Failure, Success, TryST

L = TypeVar("L")
R = TypeVar("R")
RR = TypeVar("RR")
EE = TypeVar("EE")


@dataclass(frozen=True)
class EitherTTry(Generic[L, R]):
    """Either Transformer Try"""

    value: TryST[EitherST[L, R]]

    def __bool__(self) -> bool:
        # Success and Right
        return bool(self.value) and bool(self.value.value)

    def __call__(
        self, /, if_failure_then: Optional[Callable[[Exception], EE]] = None
    ) -> Generator[Union[EE, Left[L, R], Right[L, R]], None, R]:
        try_ = self.value
        # Failure[Either[L, R]] case
        if isinstance(try_, Failure):
            if if_failure_then is not None:
                converted_failure = if_failure_then(try_.value)
                yield converted_failure
                raise GeneratorExit(self) from try_.value
            else:
                raise GeneratorExit(self) from try_.value
        # Success[Eihter[L, R]] case
        else:
            either: EitherST[L, R] = try_.value
            # Success[Left[L , R]] case
            if isinstance(either, Left):
                yield either
                raise GeneratorExit(self)
            # Success[Right[L, R]] case
            else:
                yield either
                return either.value

    def get(self) -> R:
        try_ = self.value
        if isinstance(try_, Failure):
            raise ValueError(self)
        else:
            either = try_.value
            if isinstance(either, Left):
                raise ValueError(self)
            else:
                return either.value

    def get_or_else(self, default: Callable[..., EE]) -> Union[EE, R]:
        try_ = self.value
        if isinstance(try_, Failure):
            return default()
        else:
            either = try_.value
            if isinstance(either, Left):
                return default()
            else:
                return either.value

    def map(self, functor: Callable[[R], RR]) -> EitherTTry[L, RR]:
        try_ = self.value
        # Failure case
        if isinstance(try_, Failure):
            exception: Exception = try_.value
            failure = Failure[EitherST[L, R]](value=exception)
            return EitherTTry[L, RR](value=failure)
        # Success[Either[L, R]] case
        else:
            either = try_.value
            # Success[Left[L, R]] case
            if isinstance(either, Left):
                left = Left[L, RR](value=either.value)
                success = Success[Left[L, RR]](value=left)
                return EitherTTry[L, RR](value=success)
            # Success[Right[L, R]] case
            else:
                mapped_value = functor(either.value)
                right = Right[L, RR](value=mapped_value)
                success = Success[Right[L, RR]](value=right)
                return EitherTTry[L, RR](value=success)

    def flatmap(self, functor: Callable[[R], EitherTTry[L, RR]]) -> EitherTTry[L, RR]:
        try_ = self.value
        # Failure case
        if isinstance(try_, Failure):
            exception: Exception = try_.value
            failure = Failure[EitherST[L, RR]](value=exception)
            return EitherTTry[L, RR](value=failure)
        # Success[Either[L, R]] case
        else:
            either = try_.value
            # Success[Left[L, R]] case
            if isinstance(either, Left):
                left = Left[L, RR](value=either.value)
                success = Success[Left[L, RR]](value=left)
                return EitherTTry[L, RR](value=success)
            # Success[Right[L, R]] case
            else:
                return functor(either.value)

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
                    result: Union[Left[L, R], Right[L, R], Any] = generator.send(prev)
                # Success[Right[L, R]] case
                except StopIteration as last:
                    right = Right[L, R](value=last.value)
                    success = Success[EitherST[L, R]](value=right)
                    return EitherTTry[L, R](value=success)
                # Success[Left[L, R]] case
                if isinstance(result, Left):
                    left: Left[L, R] = result
                    success = Success[EitherST[L, R]](value=left)
                    return EitherTTry[L, R](value=success)
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

    value: Future[EitherST[L, R]]

    def __bool__(self) -> bool:
        # Success and Right
        return bool(self.value) and bool(self.value.value)

    def __call__(
        self, /, if_failure_then: Optional[Callable[[Exception], EE]] = None
    ) -> Generator[Union[EE, Left[L, R], Right[L, R]], None, R]:
        # Success[Eihter[L, R]] case
        try:
            either = self.value.result()
            # Success[Left[L , R]] case
            if isinstance(either, Left):
                yield either
                raise GeneratorExit(self)
            # Success[Right[L, R]] case
            else:
                yield either
                return either.value

        # Failure[Either[L, R]] case
        except Exception as error:
            if if_failure_then is not None:
                converted_failure = if_failure_then(error)
                yield converted_failure
                raise GeneratorExit(error)
            else:
                raise GeneratorExit from error

    def get(self) -> R:
        try:
            either = self.value.result()
            if isinstance(either, Left):
                raise ValueError(self)
            else:
                return either.value
        except Exception as error:
            raise error

    def get_or_else(self, default: Callable[..., EE]) -> Union[EE, R]:
        try:
            either = self.value.result()
            if isinstance(either, Left):
                return default()
            else:
                return either.value
        except Exception:
            return default()

    def map(self, functor: Callable[[R], RR]) -> Callable[..., EitherTFuture[L, RR]]:
        def with_context(ec: Type[ExecutionContext]) -> EitherTFuture[L, RR]:
            def transformer(either: EitherST[L, R]) -> EitherST[L, RR]:
                if isinstance(either, Left):
                    return Left[L, RR](value=either.value)
                else:
                    mapped_value = functor(either.value)
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
                if isinstance(either, Left):
                    left = Left[L, RR](value=either.value)
                    future = Future[Left[L, RR]].successful(value=left)
                    return EitherTFuture[L, RR](value=future)
                else:
                    return functor(either.value)
            except Exception as error:
                future = Future[EitherST[L, RR]]()
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
                    result: Union[TryST[EitherST[L, R]], Any] = generator.send(prev)
                # Success[Right[L, R]] case
                except StopIteration as last:
                    right = Right[L, R](value=last.value)
                    future = Future[Right[L, R]].successful(value=right)
                    return EitherTFuture[L, R](value=future)
                # Failure case
                if isinstance(result, Left):
                    left: Left[L, R] = result
                    future = Future[Left[L, R]].successful(value=left)
                    return EitherTFuture[L, R](value=future)
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


EitherTFutureDo = Generator[Union[Left[L, R], Right[L, R], Any], Any, R]
EitherTFutureGenerator = Generator[
    Union[Left[L, Any], Right[L, Any], Any], Union[Left[L, Any], Right[L, Any], Any], R
]
