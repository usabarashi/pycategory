"""Try"""
from __future__ import annotations

from abc import abstractmethod, abstractproperty
from collections.abc import Generator
from functools import wraps
from typing import Any, Callable, Generic, Literal, ParamSpec, TypeAlias, TypeVar

from category import monad

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
EE = TypeVar("EE")
U = TypeVar("U")
P = ParamSpec("P")


class Try(monad.Monad, Generic[T]):
    """Try"""

    @abstractmethod
    def __iter__(self) -> Generator[Try[T], None, T]:
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

    @staticmethod
    def do(context: Callable[P, TryDo[T]], /) -> Callable[P, Try[T]]:
        """map, flatmap combination syntax sugar.

        Only type checking can determine type violations, and runtime errors may not occur.
        """

        @wraps(context)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Try[T]:
            context_ = context(*args, **kwargs)
            try:
                while True:
                    yield_state = next(context_)
                    if not isinstance(yield_state, Try):
                        raise TypeError(yield_state)
                    match yield_state.composability():
                        case monad.Composability.IMPOSSIBLE:
                            return yield_state
                        case monad.Composability.POSSIBLE:
                            # Priority is given to the value of the sub-generator's monad.
                            ...
            except StopIteration as return_:
                return Success[T].lift(return_.value)

        return wrapper

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

    def __iter__(self) -> Generator[Try[T], None, T]:
        yield self.flatmap(lambda value: Success[T](value))
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

    def __iter__(self) -> Generator[Try[T], None, T]:
        yield self.flatmap(lambda value: Success[T](value))
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


SubType: TypeAlias = Failure[T] | Success[T]
TryDo: TypeAlias = Generator[Try[Any], None, T]
