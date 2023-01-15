"""Try"""
from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Generator
from functools import wraps
from typing import (
    Any,
    Callable,
    Literal,
    Optional,
    ParamSpec,
    TypeAlias,
    TypeVar,
    cast,
    overload,
)

from . import collection, either, extension, extractor, monad, option, processor

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
EE = TypeVar("EE")
U = TypeVar("U")
P = ParamSpec("P")


class Try(ABC, monad.Monad[T], extension.Extension):
    """Try"""

    @abstractmethod
    def __iter__(self) -> Generator[Try[T], None, T]:
        raise NotImplementedError

    @abstractmethod
    def map(self, func: Callable[[T], TT], /) -> Try[TT]:
        raise NotImplementedError

    @staticmethod
    def pure(value: T) -> Try[T]:
        return Success[T](value)

    @abstractmethod
    def flat_map(self, func: Callable[[T], Try[TT]], /) -> Try[TT]:
        raise NotImplementedError

    @abstractmethod
    def recover(self, func: Callable[[Exception], TT], /) -> Try[TT]:
        raise NotImplementedError

    @abstractmethod
    def recover_with(self, func: Callable[[Exception], Try[TT]], /) -> Try[TT]:
        raise NotImplementedError

    @abstractproperty
    def to_either(self) -> either.Either[Exception, T]:
        raise NotImplementedError

    @abstractproperty
    def to_option(self) -> option.Option[T]:
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

    @overload
    @staticmethod
    def hold(func: Callable[P, T], /) -> Callable[P, Try[T]]:
        ...

    @overload
    @staticmethod
    def hold(
        *,
        unmask: Optional[tuple[str, ...]] = None,
        debugger: Optional[Callable[[processor.Arguments], Any]] = None,
    ) -> Callable[[Callable[P, T]], Callable[P, Try[T]]]:
        """

        Unmask and record arguments in case of Failure.
        """

    @staticmethod
    def hold(
        func: Optional[Callable[P, T]] = None,
        /,
        *,
        unmask: Optional[tuple[str, ...]] = None,
        debugger: Optional[Callable[[processor.Arguments], Any]] = None,
    ) -> Callable[P, Try[T]] | Callable[[Callable[P, T]], Callable[P, Try[T]]]:
        def wrap(func: Callable[P, T], /) -> Callable[P, Try[T]]:
            return _hold(func=func, unmask=unmask, debugger=debugger)

        if func is None:
            return wrap
        else:
            return wrap(func)


def _hold(
    *,
    func: Callable[P, T],
    unmask: Optional[tuple[str, ...]] = None,
    debugger: Optional[Callable[[processor.Arguments], Any]] = None,
) -> Callable[P, Try[T]]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Try[T]:
        try:
            return Success[T](func(*args, **kwargs))
        except Exception as exception:
            arguments = processor.arguments(func, *args, **kwargs)
            masked_arguments = processor.masking(arguments=arguments, unmask=unmask)
            parsed_arguments = processor.parse(masked_arguments)
            debug = processor.execute_debugger(debugger=debugger, arguments=arguments)
            report = processor.RuntimeErrorReport(
                arguments=parsed_arguments,
                debug=debug,
            )
            exception.args = tuple(collection.Vector(exception.args).append(report))
            return Failure[T](exception)

    return wrapper


class Failure(Try[T], extractor.Extractor):
    """Failure"""

    __match_args__ = ("exception",)

    def __init__(self, exception: Exception, /):
        self.exception = exception

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.exception)})"

    def __eq__(self, other: Try[T]) -> bool:
        match other.pattern:
            case Failure(exception):
                return self.exception == exception
            case Success():
                return False

    def __iter__(self) -> Generator[Try[T], None, T]:
        raise GeneratorExit(self) from self.exception

    def map(self, _: Callable[[T], TT], /) -> Try[TT]:
        return cast(Failure[TT], self)

    def flat_map(self, _: Callable[[T], Try[TT]], /) -> Try[TT]:
        return cast(Failure[TT], self)

    def recover(self, func: Callable[[Exception], TT], /) -> Try[TT]:
        try:
            if (result := func(self.exception)) is None:
                return cast(Failure[TT], self)
            else:
                return Success[TT](result)
        except Exception as exception:
            return Failure[TT](exception)

    def recover_with(self, func: Callable[[Exception], Try[TT]], /) -> Try[TT]:
        try:
            if (result := func(self.exception)) is None:
                return cast(Failure[TT], self)
            else:
                return result
        except Exception as exception:
            return Failure[TT](exception)

    @property
    def to_either(self) -> either.Either[Exception, T]:
        return either.Left(self.exception)

    @property
    def to_option(self) -> option.Option[T]:
        return option.VOID

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


class Success(Try[T], extractor.Extractor):
    """Success"""

    __match_args__ = ("value",)

    def __init__(self, value: T, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other: Try[T]) -> bool:
        match other.pattern:
            case Failure():
                return False
            case Success(value):
                return self.value == value

    def __iter__(self) -> Generator[Try[T], None, T]:
        yield self
        return self.value

    def map(self, func: Callable[[T], TT], /) -> Try[TT]:
        return Success[TT](func(self.value))

    def flat_map(self, func: Callable[[T], Try[TT]], /) -> Try[TT]:
        return func(self.value)

    def recover(self, _: Callable[[Exception], TT], /) -> Try[TT]:
        return cast(Try[TT], self)

    def recover_with(self, _: Callable[[Exception], Try[TT]], /) -> Try[TT]:
        return cast(Try[TT], self)

    @property
    def to_either(self) -> either.Either[Exception, T]:
        return either.Right(self.value)

    @property
    def to_option(self) -> option.Option[T]:
        return option.Some[T](self.value)

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


SubType: TypeAlias = Failure[T] | Success[T]
TryDo: TypeAlias = Generator[Try[T], None, T]
