from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generator, Generic, Optional, TypeVar, Union

from category.either import EitherST, Left, Right
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
        self, /, failure_then: Optional[Callable[[Exception], EE]] = None
    ) -> Generator[Union[EE, TryST[EitherST[L, R]]], None, R]:
        try_ = self.value
        # Failure[Either[L, R]] case
        if isinstance(try_, Failure):
            if failure_then is not None:
                converted_failure = failure_then(try_.value)
                yield converted_failure
                raise EOFError(self)
            else:
                yield try_
                raise EOFError(self)
        # Success[Eihter[L, R]] case
        else:
            either = try_.value
            # Success[Left[L , R]] case
            if isinstance(either, Left):
                yield try_
                raise EOFError(self)
            # Success[Right[L, R]] case
            else:
                yield try_
                return either.value

    def map(self, functor: Callable[[R], RR]) -> EitherTTry[L, RR]:
        try_ = self.value
        # Failure case
        if isinstance(try_, Failure):
            exception: Exception = try_.value
            return EitherTTry[L, RR](value=Failure(value=exception))
        # Success[Either[L, R]] case
        else:
            either = try_.value
            # Success[Left[L, R]] case
            if isinstance(either, Left):
                return EitherTTry[L, RR](
                    value=Success(value=Left[L, RR](value=either.value))
                )
            # Success[Right[L, R]] case
            else:
                mapped_value = functor(either.value)
                return EitherTTry[L, RR](
                    value=Success(value=Right[L, RR](value=mapped_value))
                )

    def flatmap(self, functor: Callable[[R], EitherTTry[L, RR]]) -> EitherTTry[L, RR]:
        try_ = self.value
        # Failure case
        if isinstance(try_, Failure):
            exception: Exception = try_.value
            return EitherTTry[L, RR](value=Failure(value=exception))
        # Success[Either[L, R]] case
        else:
            either = try_.value
            # Success[Left[L, R]] case
            if isinstance(either, Left):
                return EitherTTry[L, RR](
                    value=Success(value=Left[L, RR](value=either.value))
                )
            # Success[Right[L, R]] case
            else:
                return functor(either.value)

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

    @staticmethod
    def do(
        generator_fuction: Callable[..., EitherTTryGenerator[L, R]]
    ) -> Callable[..., EitherTTry[L, R]]:
        def impl(*args: Any, **kwargs: Any) -> TryST[EitherST[L, R]]:
            def recur(
                generator: EitherTTryGenerator[L, R],
                prev: Any,
            ) -> EitherTTry[L, R]:
                try:
                    result: Union[TryST[EitherST[L, R]], Any] = generator.send(prev)
                # Success[Right[L, R]] case
                except StopIteration as last:
                    return EitherTTry[L, R](
                        value=Success(value=Right[L, R](value=last.value))
                    )
                # Failure case
                if isinstance(result, Failure):
                    return EitherTTry[L, R](value=result)
                # Success[Left[L, R]] case
                elif isinstance(result, Success) and isinstance(result.value, Left):
                    return EitherTTry[L, R](value=Success(value=result.value))
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


EitherTTryDo = Generator[Union[TryST[EitherST[L, Any]], Any], Any, R]
EitherTTryGenerator = Generator[
    Union[TryST[EitherST[L, Any]], Any], Union[TryST[EitherST[L, Any]], Any], R
]
