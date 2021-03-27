from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    Generator,
    Generic,
    Literal,
    NoReturn,
    Optional,
    TypeVar,
    Union,
)

L = TypeVar("L")
R = TypeVar("R")
LL = TypeVar("LL")
RR = TypeVar("RR")
TT = TypeVar("TT")
EE = TypeVar("EE")


class Either(ABC, Generic[L, R]):
    """Either"""

    value: Union[L, R]

    @abstractmethod
    def __call__(
        self, /, if_left_then: Optional[Callable[[L], EE]] = None
    ) -> Generator[Union[EitherST[L, R], EE], None, R]:
        raise NotImplementedError

    @abstractmethod
    def map(self, functor: Callable[[R], RR]) -> EitherST[L, RR]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, functor: Callable[[R], EitherST[L, RR]]) -> EitherST[L, RR]:
        raise NotImplementedError

    @abstractmethod
    def fold(self, /, left: Callable[[L], TT], right: Callable[[R], TT]) -> TT:
        raise NotImplementedError

    @abstractmethod
    def left(self) -> LeftProjection[L, R]:
        raise NotImplementedError

    @abstractmethod
    def right(self) -> RightProjection[L, R]:
        raise NotImplementedError

    @abstractmethod
    def is_left(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_right(self) -> bool:
        raise NotImplementedError

    @staticmethod
    def do(
        generator_fuction: Callable[..., EitherGenerator[L, R]]
    ) -> Callable[..., EitherST[L, R]]:
        def wrapper(*args: Any, **kwargs: Any) -> EitherST[L, R]:
            def recur(
                generator: EitherGenerator[L, R],
                prev: Any,
            ) -> EitherST[L, R]:
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    # Right case
                    return Right(value=last.value)
                # Left case
                if isinstance(result, Left):
                    return result
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return wrapper


class EitherError(Exception):
    ...


@dataclasses.dataclass(frozen=True)
class Left(Either[L, R]):
    """Left"""

    value: L

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(
        self, /, if_left_then: Optional[Callable[[L], EE]] = None
    ) -> Generator[Union[EE, Left[L, R]], None, R]:
        # Type conversion
        if if_left_then is not None:
            converted_left = if_left_then(self.value)
            yield converted_left
            raise GeneratorExit(self)
        else:
            yield self
            raise GeneratorExit(self)

    def map(self, functor: Callable[[R], RR]) -> EitherST[L, RR]:
        return Left[L, RR](self.value)

    def flatmap(self, functor: Callable[[R], EitherST[L, RR]]) -> EitherST[L, RR]:
        return Left[L, RR](value=self.value)

    def fold(self, /, left: Callable[[L], TT], right: Callable[[R], TT]) -> TT:
        return left(self.value)

    def left(self) -> LeftProjection[L, R]:
        return LeftProjection(either=self)

    def right(self) -> RightProjection[L, R]:
        return RightProjection(either=self)

    def is_left(self) -> Literal[True]:
        return True

    def is_right(self) -> Literal[False]:
        return False


@dataclasses.dataclass(frozen=True)
class Right(Either[L, R]):
    """Right"""

    value: R

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(
        self, if_left_then: Optional[Callable[[L], Any]] = None
    ) -> Generator[Right[L, R], None, R]:
        yield self
        return self.value

    def map(self, functor: Callable[[R], RR]) -> EitherST[L, RR]:
        return Right[L, RR](functor(self.value))

    def flatmap(self, functor: Callable[[R], EitherST[L, RR]]) -> EitherST[L, RR]:
        return functor(self.value)

    def fold(self, /, left: Callable[[L], TT], right: Callable[[R], TT]) -> TT:
        return right(self.value)

    def left(self) -> LeftProjection[L, R]:
        return LeftProjection(either=self)

    def right(self) -> RightProjection[L, R]:
        return RightProjection(either=self)

    def is_left(self) -> Literal[False]:
        return False

    def is_right(self) -> Literal[True]:
        return True


@dataclasses.dataclass(frozen=True)
class LeftProjection(Generic[L, R]):
    """LeftProjection"""

    either: EitherST[L, R]

    def __bool__(self) -> bool:
        return bool(self.either)

    def get(self) -> Union[NoReturn, L]:
        if isinstance(self.either, Left):
            return self.either.value
        else:
            raise EitherError()

    def get_or_else(self, default: Callable[..., RR]) -> Union[L, RR]:
        if isinstance(self.either, Left):
            return self.either.value
        else:
            return default()

    def map(self, functor: Callable[[L], LL]) -> EitherST[LL, R]:
        if isinstance(self.either, Left):
            return Left[LL, R](value=functor(self.either.value))
        else:
            return Right[LL, R](value=self.either.value)

    def flatmap(self, functor: Callable[[L], EitherST[LL, R]]) -> EitherST[LL, R]:
        if isinstance(self.either, Left):
            return functor(self.either.value)
        else:
            return Right[LL, R](value=self.either.value)


@dataclasses.dataclass(frozen=True)
class RightProjection(Generic[L, R]):
    """RightProjection"""

    either: EitherST[L, R]

    def __bool__(self) -> bool:
        return bool(self.either)

    def get(self) -> Union[NoReturn, R]:
        if isinstance(self.either, Left):
            raise EitherError()
        else:
            return self.either.value

    def get_or_else(self, default: Callable[..., LL]) -> Union[LL, R]:
        if isinstance(self.either, Left):
            return default()
        else:
            return self.either.value

    def map(self, functor: Callable[[R], RR]) -> EitherST[L, RR]:
        if isinstance(self.either, Left):
            return Left[L, RR](value=self.either.value)
        else:
            return Right[L, RR](value=functor(self.either.value))

    def flatmap(self, functor: Callable[[R], EitherST[L, RR]]) -> EitherST[L, RR]:
        if isinstance(self.either, Left):
            return Left[L, RR](value=self.either.value)
        else:
            return functor(self.either.value)


EitherST = Union[Left[L, R], Right[L, R]]
EitherDo = Generator[Union[EitherST[L, Any], Any], Any, R]
EitherGenerator = Generator[
    Union[EitherST[L, Any], Any],
    Union[EitherST[L, Any], Any],
    R,
]
