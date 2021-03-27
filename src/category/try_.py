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

T = TypeVar("T")
TT = TypeVar("TT")
EE = TypeVar("EE")


class Try(ABC, Generic[T]):
    """Try"""

    value: Union[Exception, T]

    @abstractmethod
    def __call__(
        self, /, if_failure_then: Optional[Callable[[Exception], EE]] = None
    ) -> Generator[Union[EE, TryST[T]], None, T]:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> Union[NoReturn, T]:
        raise NotImplementedError

    @abstractmethod
    def get_or_else(self, default: Callable[..., TT]) -> Union[T, TT]:
        raise NotImplementedError

    @abstractmethod
    def map(self, functor: Callable[[T], TT]) -> TryST[TT]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, functor: Callable[[T], TryST[TT]]) -> TryST[TT]:
        raise NotImplementedError

    @abstractmethod
    def fold(
        self,
        /,
        failure: Callable[[Exception], TT],
        success: Callable[[T], TT],
    ) -> TT:
        raise NotImplementedError

    @abstractmethod
    def is_failure(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_success(self) -> bool:
        raise NotImplementedError

    @staticmethod
    def hold(fuction: Callable[..., T]) -> Callable[..., TryST[T]]:
        def wrapper(*args: Any, **kwargs: Any) -> TryST[T]:
            try:
                return Success(value=fuction(*args, **kwargs))
            except Exception as error:
                return Failure(value=error)

        return wrapper

    @staticmethod
    def do(
        generator_fuction: Callable[..., TryGenerator[T]]
    ) -> Callable[..., TryST[T]]:
        def impl(*args: Any, **kwargs: Any) -> TryST[T]:
            def recur(
                generator: TryGenerator[T],
                prev: Any,
            ) -> TryST[T]:
                try:
                    result: Union[TryST[T], Any] = generator.send(prev)
                except StopIteration as last:
                    # Success case
                    return Success(value=last.value)
                # Failure case
                if isinstance(result, Failure):
                    return result
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


@dataclasses.dataclass(frozen=True)
class Failure(Try[T]):
    """Failure"""

    value: Exception

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(
        self, /, if_failure_then: Optional[Callable[[Exception], EE]] = None
    ) -> Generator[Union[EE, TryST[T]], None, T]:
        if if_failure_then is not None:
            converted_failure = if_failure_then(self.value)
            yield converted_failure
            raise GeneratorExit(self)
        else:
            yield self
            raise GeneratorExit(self)

    def get(self) -> NoReturn:
        raise ValueError() from self.value

    def get_or_else(self, default: Callable[..., TT]) -> Union[T, TT]:
        return default()

    def map(self, functor: Callable[[T], TT]) -> TryST[TT]:
        return Failure[TT](value=self.value)

    def flatmap(self, functor: Callable[[T], TryST[TT]]) -> TryST[TT]:
        return Failure[TT](value=self.value)

    def fold(
        self,
        /,
        failure: Callable[[Exception], TT],
        success: Callable[[T], TT],
    ) -> TT:
        return failure(self.value)

    def is_failure(self) -> Literal[True]:
        return True

    def is_success(self) -> Literal[False]:
        return False


@dataclasses.dataclass(frozen=True)
class Success(Try[T]):
    """Success"""

    value: T

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(
        self, /, if_failure_then: Optional[Callable[[Exception], EE]] = None
    ) -> Generator[Union[EE, TryST[T]], None, T]:
        yield self
        return self.value

    def get(self) -> T:
        return self.value

    def get_or_else(self, default: Callable[..., Any]) -> T:
        return self.value

    def map(self, functor: Callable[[T], TT]) -> TryST[TT]:
        return Success[TT](value=functor(self.value))

    def flatmap(self, functor: Callable[[T], TryST[TT]]) -> TryST[TT]:
        return functor(self.value)

    def fold(
        self,
        /,
        failure: Callable[[Exception], TT],
        success: Callable[[T], TT],
    ) -> TT:
        return success(self.value)

    def is_failure(self) -> Literal[False]:
        return False

    def is_success(self) -> Literal[True]:
        return True


TryST = Union[Failure[T], Success[T]]
TryDo = Generator[Union[TryST[T], Any], Any, T]
TryGenerator = Generator[
    Union[TryST[Any], Any],
    Union[TryST[Any], Any],
    T,
]
