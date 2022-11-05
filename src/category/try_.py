"""Try"""
from __future__ import annotations

from abc import abstractmethod, abstractproperty
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

from . import collection, either, monad, option, processor

T = TypeVar("T", covariant=True)
TT = TypeVar("TT")
EE = TypeVar("EE")
U = TypeVar("U")
P = ParamSpec("P")


class Try(monad.Monad[T]):
    """Try"""

    @abstractmethod
    def __iter__(self) -> Generator[Try[T], None, T]:
        raise NotImplementedError

    @abstractmethod
    def map(self, other: Callable[[T], TT], /) -> Try[TT]:
        raise NotImplementedError

    @abstractmethod
    def flat_map(self, other: Callable[[T], Try[TT]], /) -> Try[TT]:
        raise NotImplementedError

    @abstractmethod
    def recover(self, other: Callable[[Exception], TT], /) -> Try[TT]:
        raise NotImplementedError

    @abstractmethod
    def recover_with(self, other: Callable[[Exception], Try[TT]], /) -> Try[TT]:
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

    @staticmethod
    def do(context: Callable[P, TryDo[T]], /) -> Callable[P, Try[T]]:
        """map, flat_map combination syntax sugar.

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
                        case monad.Composability.Immutable:
                            return yield_state
                        case monad.Composability.Variable:
                            # Priority is given to the value of the sub-generator's monad.
                            ...
            except StopIteration as return_:
                return Success[T].lift(return_.value)

        return wrapper

    @abstractmethod
    def method(self, other: Callable[[Try[T]], TT], /) -> TT:
        raise NotImplementedError

    @overload
    @staticmethod
    def hold(function: Callable[P, T], /) -> Callable[P, Try[T]]:
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
        function: Optional[Callable[P, T]] = None,
        /,
        *,
        unmask: Optional[tuple[str, ...]] = None,
        debugger: Optional[Callable[[processor.Arguments], Any]] = None,
    ) -> Callable[P, Try[T]] | Callable[[Callable[P, T]], Callable[P, Try[T]]]:
        def wrap(function_: Callable[P, T], /) -> Callable[P, Try[T]]:
            return _hold(function=function_, unmask=unmask, debugger=debugger)

        if function is None:
            return wrap
        else:
            return wrap(function)


def _hold(
    *,
    function: Callable[P, T],
    unmask: Optional[tuple[str, ...]] = None,
    debugger: Optional[Callable[[processor.Arguments], Any]] = None,
) -> Callable[P, Try[T]]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Try[T]:
        try:
            return Success[T](function(*args, **kwargs))
        except Exception as exception:
            arguments = processor.arguments(function, *args, **kwargs)
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


class Failure(Try[T]):
    """Failure"""

    __match_args__ = ()

    def __init__(self, exception: Exception, /):
        self.exception = exception

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.exception)})"

    def __bool__(self) -> Literal[False]:
        return False

    def __iter__(self) -> Generator[Try[T], None, T]:
        yield self.flat_map(lambda value: Success[T](value))
        raise GeneratorExit(self) from self.exception

    def map(self, other: Callable[[T], TT], /) -> Try[TT]:
        return cast(Failure[TT], self)

    def flat_map(self, other: Callable[[T], Try[TT]], /) -> Try[TT]:
        return cast(Failure[TT], self)

    def recover(self, other: Callable[[Exception], TT], /) -> Try[TT]:
        try:
            if (result := other(self.exception)) is None:
                return cast(Failure[TT], self)
            else:
                return Success[TT](result)
        except Exception as exception:
            return Failure[TT](exception)

    def recover_with(self, other: Callable[[Exception], Try[TT]], /) -> Try[TT]:
        try:
            if (result := other(self.exception)) is None:
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
        return option.Void[T]()

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

    def method(self, other: Callable[[Failure[T]], TT], /) -> TT:
        return other(self)


class Success(Try[T]):
    """Success"""

    __match_args__ = ("value",)

    def __init__(self, value: T, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __bool__(self) -> Literal[True]:
        return True

    def __iter__(self) -> Generator[Try[T], None, T]:
        yield self.flat_map(lambda value: Success[T](value))
        return self.value

    def map(self, other: Callable[[T], TT], /) -> Try[TT]:
        return Success[TT](other(self.value))

    def flat_map(self, other: Callable[[T], Try[TT]], /) -> Try[TT]:
        return other(self.value)

    def recover(self, other: Callable[[Exception], TT], /) -> Try[TT]:
        return cast(Try[TT], self)

    def recover_with(self, other: Callable[[Exception], Try[TT]], /) -> Try[TT]:
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

    def method(self, other: Callable[[Success[T]], TT], /) -> TT:
        return other(self)


SubType: TypeAlias = Failure[T] | Success[T]
TryDo: TypeAlias = Generator[Try[Any], None, T]
