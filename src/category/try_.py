"""Try"""
from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Generator
from typing import Any, Callable, Generic, Literal, TypeVar, Union

T = TypeVar("T", covariant=True)
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
                    failure = Failure[T](result._exception)
                    return failure
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return impl


class Failure(Try[T]):
    """Failure"""

    def __init__(self, exception: Exception, /):
        self._exception = exception

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(self) -> Generator[Try[T], Try[T], T]:
        yield self
        raise GeneratorExit(self) from self._exception

    def map(self, functor: Callable[[T], TT], /) -> Try[TT]:
        return Failure[TT](self._exception)

    def flatmap(self, functor: Callable[[T], Try[TT]], /) -> Try[TT]:
        return Failure[TT](self._exception)

    def fold(
        self,
        *,
        failure: Callable[[Exception], U],
        success: Callable[[T], U],
    ) -> U:
        return failure(self._exception)

    def is_failure(self) -> Literal[True]:
        return True

    def is_success(self) -> Literal[False]:
        return False

    def get(self) -> T:
        raise ValueError() from self._exception

    def get_or_else(self, default: Callable[..., EE], /) -> EE:
        return default()

    @property
    def pattern(self) -> SubType[T]:
        return self

    def method(self, functor: Callable[[Failure[T]], TT], /) -> TT:
        return functor(self)


class Success(Try[T]):
    """Success"""

    def __init__(self, value: T, /):
        self._value = value

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(self) -> Generator[Try[T], Try[T], T]:
        yield self
        return self._value

    def map(self, functor: Callable[[T], TT], /) -> Try[TT]:
        return Success[TT](functor(self._value))

    def flatmap(self, functor: Callable[[T], Try[TT]], /) -> Try[TT]:
        return functor(self._value)

    def fold(
        self,
        *,
        failure: Callable[[Exception], TT],
        success: Callable[[T], TT],
    ) -> TT:
        return success(self._value)

    def is_failure(self) -> Literal[False]:
        return False

    def is_success(self) -> Literal[True]:
        return True

    def get(self) -> T:
        return self._value

    def get_or_else(self, default: Callable[..., EE], /) -> T:
        return self._value

    @property
    def pattern(self) -> SubType[T]:
        return self

    def method(self, functor: Callable[[Success[T]], TT], /) -> TT:
        return functor(self)


SubType = Union[Failure[T], Success[T]]
TryDo = Generator[Union[Any, Try[Any]], Union[Any, Try[Any]], T]
