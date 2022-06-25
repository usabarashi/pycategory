"""Try"""
from __future__ import annotations

from abc import abstractmethod, abstractproperty
from collections.abc import Generator
from functools import wraps
from typing import Any, Callable, Generic, Literal, ParamSpec, TypeVar, Union

from category.monad import Monad

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
EE = TypeVar("EE")
U = TypeVar("U")
P = ParamSpec("P")


class Try(Monad, Generic[T]):
    """Try"""

    @abstractmethod
    def __iter__(
        self,
    ) -> Generator[
        tuple[Try[T], Callable[[Try[T]], T], Callable[[T], Try[T]]], None, T
    ]:
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
    def get_or_else(self, default: Callable[..., EE], /) -> EE | T:
        raise NotImplementedError

    @abstractproperty
    def pattern(self) -> SubType[T]:
        raise NotImplementedError

    @abstractmethod
    def method(self, functor: Callable[[Try[T]], TT], /) -> TT:
        raise NotImplementedError

    @staticmethod
    def hold(function: Callable[P, T]) -> Callable[P, Try[T]]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Try[T]:
            try:
                return Success[T](function(*args, **kwargs))
            except Exception as error:
                return Failure[T](error)

        return wrapper


class Failure(Try[T]):
    """Failure"""

    __match_args__ = ()

    def __init__(self, exception: Exception, /):
        self.exception = exception

    def __bool__(self) -> Literal[False]:
        return False

    def __iter__(
        self,
    ) -> Generator[
        tuple[Try[T], Callable[[Try[T]], T], Callable[[T], Try[T]]], None, T
    ]:
        lift: Callable[[T], Try[T]] = lambda value: Success[T](value)
        yield self.flatmap(lift), Failure.get, lift
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


class Success(Try[T]):
    """Success"""

    __match_args__ = ("value",)

    def __init__(self, value: T, /):
        self.value = value

    def __bool__(self) -> Literal[True]:
        return True

    def __iter__(
        self,
    ) -> Generator[
        tuple[Try[T], Callable[[Try[T]], T], Callable[[T], Try[T]]], None, T
    ]:
        lift: Callable[[T], Try[T]] = lambda value: Success[T](value)
        yield self.flatmap(lift), Success.get, lift
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


SubType = Failure[T] | Success[T]
TryDo = Generator[
    Union[
        tuple[Try[T], Callable[[Try[T]], T], Callable[[T], Try[T]]],
        tuple[Try[Any], Callable[[Try[Any]], Any], Callable[[Any], Try[Any]]],
    ],
    Union[T, Any],
    T,
]
