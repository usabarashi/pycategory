"""Try"""
from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Generator
from typing import Any, Callable, Generic, Literal, TypeVar, Union

T = TypeVar("T")
TT = TypeVar("TT")
EE = TypeVar("EE")
U = TypeVar("U")


class Try(ABC, Generic[T]):
    """Try"""

    @abstractmethod
    def __call__(self) -> Generator[Try[T], Try[T], T]:
        raise NotImplementedError

    @abstractmethod
    def map(self, functor: Callable[[T], TT], /) -> Try[TT]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, functor: Callable[[T], Try[TT]], /) -> Try[TT]:
        raise NotImplementedError

    @abstractmethod
    def fold(
        self,
        *,
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

    @abstractmethod
    def get(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_or_else(self, default: Callable[..., EE], /) -> Union[EE, T]:
        raise NotImplementedError

    @abstractproperty
    def pattern(self) -> SubType[T]:
        raise NotImplementedError

    @abstractmethod
    def method(self, functor: Callable[[Try[T]], TT], /) -> TT:
        raise NotImplementedError

    @staticmethod
    def hold(fuction: Callable[..., T]) -> Callable[..., Try[T]]:
        def wrapper(*args: Any, **kwargs: Any) -> Try[T]:
            try:
                return Success[T](fuction(*args, **kwargs))
            except Exception as error:
                return Failure[T](error)

        return wrapper

    @staticmethod
    def do(generator_fuction: Callable[..., TryDo[T]]) -> Callable[..., Try[T]]:
        def impl(*args: Any, **kwargs: Any) -> Try[T]:
            def recur(
                generator: TryDo[T],
                prev: Union[Any, Try[T]],
            ) -> Try[T]:
                try:
                    result: Union[Try[T], Any] = generator.send(prev)
                except StopIteration as last:
                    return Success[T](last.value)
                if isinstance(result, Failure):
                    failure = Failure[T](result.exception)
                    return failure
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


@dataclasses.dataclass(frozen=True)
class Failure(Try[T]):
    """Failure"""

    exception: Exception

    def __new__(cls, exception: Exception, /):
        return super().__new__(cls)

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(self) -> Generator[Try[T], Try[T], T]:
        yield self
        raise GeneratorExit(self) from self.exception

    def map(self, functor: Callable[[T], TT], /) -> Try[TT]:
        return Failure[TT](self.exception)

    def flatmap(self, functor: Callable[[T], Try[TT]], /) -> Try[TT]:
        return Failure[TT](self.exception)

    def fold(
        self,
        *,
        failure: Callable[[Exception], U],
        success: Callable[[T], U],
    ) -> U:
        return failure(self.exception)

    def is_failure(self) -> Literal[True]:
        return True

    def is_success(self) -> Literal[False]:
        return False

    def get(self) -> T:
        raise ValueError() from self.exception

    def get_or_else(self, default: Callable[..., EE], /) -> EE:
        return default()

    @property
    def pattern(self) -> SubType[T]:
        return self

    def method(self, functor: Callable[[Failure[T]], TT], /) -> TT:
        return functor(self)


@dataclasses.dataclass(frozen=True)
class Success(Try[T]):
    """Success"""

    value: T

    def __new__(cls, value: T, /):
        return super().__new__(cls)

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(self) -> Generator[Try[T], Try[T], T]:
        yield self
        return self.value

    def map(self, functor: Callable[[T], TT], /) -> Try[TT]:
        return Success[TT](functor(self.value))

    def flatmap(self, functor: Callable[[T], Try[TT]], /) -> Try[TT]:
        return functor(self.value)

    def fold(
        self,
        *,
        failure: Callable[[Exception], TT],
        success: Callable[[T], TT],
    ) -> TT:
        return success(self.value)

    def is_failure(self) -> Literal[False]:
        return False

    def is_success(self) -> Literal[True]:
        return True

    def get(self) -> T:
        return self.value

    def get_or_else(self, default: Callable[..., EE], /) -> T:
        return self.value

    @property
    def pattern(self) -> SubType[T]:
        return self

    def method(self, functor: Callable[[Success[T]], TT], /) -> TT:
        return functor(self)


SubType = Union[Failure[T], Success[T]]
TryDo = Generator[Union[Any, Try[Any]], Union[Any, Try[Any]], T]
