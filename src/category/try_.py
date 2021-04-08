from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Callable, Generator, Generic, Literal, TypeVar, Union

T = TypeVar("T")
TT = TypeVar("TT")
EE = TypeVar("EE")


class Try(ABC, Generic[T]):
    """Try"""

    value: Union[Exception, T]

    @abstractmethod
    def __call__(self) -> Generator[Try[T], None, T]:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_or_else(self, default: Callable[..., TT]) -> Union[T, TT]:
        raise NotImplementedError

    @abstractmethod
    def map(self, functor: Callable[[T], TT]) -> Try[TT]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, functor: Callable[[T], Try[TT]]) -> Try[TT]:
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

    @abstractproperty
    def pattern(self) -> SubType[T]:
        raise NotImplementedError

    @staticmethod
    def hold(fuction: Callable[..., T]) -> Callable[..., Try[T]]:
        def wrapper(*args: Any, **kwargs: Any) -> Try[T]:
            try:
                return Success[T](value=fuction(*args, **kwargs))
            except Exception as error:
                return Failure[T](value=error)

        return wrapper

    @staticmethod
    def do(generator_fuction: Callable[..., TryGenerator[T]]) -> Callable[..., Try[T]]:
        def impl(*args: Any, **kwargs: Any) -> Try[T]:
            def recur(
                generator: TryGenerator[T],
                prev: Any,
            ) -> Try[T]:
                try:
                    result: Union[Try[T], Any] = generator.send(prev)
                except StopIteration as last:
                    # Success case
                    return Success[T](value=last.value)
                # Failure case
                if isinstance(result, Failure):
                    failure = Failure[T](value=result.value)
                    return failure
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl

    @abstractmethod
    def convert(self, functor: Callable[[Try[T]], TT]) -> TT:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class Failure(Try[T]):
    """Failure"""

    value: Exception

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(self) -> Generator[Try[T], None, T]:
        yield self
        raise GeneratorExit(self) from self.value

    def get(self) -> T:
        raise ValueError() from self.value

    def get_or_else(self, default: Callable[..., TT]) -> Union[T, TT]:
        return default()

    def map(self, functor: Callable[[T], TT]) -> Try[TT]:
        return Failure[TT](value=self.value)

    def flatmap(self, functor: Callable[[T], Try[TT]]) -> Try[TT]:
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

    @property
    def pattern(self) -> SubType[T]:
        return self

    def convert(self, functor: Callable[[Failure[T]], TT]) -> TT:
        return functor(self)


@dataclasses.dataclass(frozen=True)
class Success(Try[T]):
    """Success"""

    value: T

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(self) -> Generator[Try[T], None, T]:
        yield self
        return self.value

    def get(self) -> T:
        return self.value

    def get_or_else(self, default: Callable[..., Any]) -> T:
        return self.value

    def map(self, functor: Callable[[T], TT]) -> Try[TT]:
        return Success[TT](value=functor(self.value))

    def flatmap(self, functor: Callable[[T], Try[TT]]) -> Try[TT]:
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

    @property
    def pattern(self) -> SubType[T]:
        return self

    def convert(self, functor: Callable[[Success[T]], TT]) -> TT:
        return functor(self)


SubType = Union[Failure[T], Success[T]]
TryDo = Generator[Try[T], Any, T]
TryGenerator = Generator[
    Union[Try[Any], Any],
    Union[Try[Any], Any],
    T,
]
