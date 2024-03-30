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

T = TypeVar("T")
Tp = TypeVar("Tp", covariant=True)
TTp = TypeVar("TTp", covariant=True)
Ep = TypeVar("Ep", covariant=True)
U = TypeVar("U")
P = ParamSpec("P")


class Try(ABC, monad.Monad[Tp], extension.Extension):
    """Try"""

    @abstractmethod
    def __iter__(self) -> Generator[Try[Tp], None, Tp]:
        raise NotImplementedError()

    @abstractmethod
    def map(self, func: Callable[[Tp], TTp], /) -> Try[TTp]:
        raise NotImplementedError()

    @staticmethod
    def pure(value: T) -> Try[T]:
        return Success[T](value)

    @abstractmethod
    def flat_map(self, func: Callable[[Tp], Try[TTp]], /) -> Try[TTp]:  # type: ignore
        raise NotImplementedError()

    @abstractmethod
    def recover(self, func: Callable[[Exception], TTp], /) -> Try[TTp]:
        raise NotImplementedError()

    @abstractmethod
    def recover_with(self, func: Callable[[Exception], Try[TTp]], /) -> Try[TTp]:
        raise NotImplementedError()

    @abstractproperty
    def to_either(self) -> either.Either[Exception, Tp]:
        raise NotImplementedError()

    @abstractproperty
    def to_option(self) -> option.Option[Tp]:
        raise NotImplementedError()

    @abstractmethod
    def fold(
        self,
        *,
        failure: Callable[[Exception], TTp],
        success: Callable[[Tp], TTp],
    ) -> TTp:
        raise NotImplementedError()

    @abstractmethod
    def is_failure(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_success(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> Tp:
        raise NotImplementedError()

    @abstractmethod
    def get_or_else(self, default: Callable[..., Ep], /) -> Ep | Tp:
        raise NotImplementedError()

    @abstractproperty
    def pattern(self) -> SubType[Tp]:
        raise NotImplementedError()

    @staticmethod
    def do(  # type: ignore
        context: Callable[P, Generator[Try[Any], None, Tp]], /
    ) -> Callable[P, Try[Tp]]:
        """map, flat_map combination syntax sugar."""
        return cast(Callable[P, Try[Tp]], monad.Monad.do(context))

    @overload
    @staticmethod
    def hold(func: Callable[P, Tp], /) -> Callable[P, Try[Tp]]:
        """Try context decorator"""

    @overload
    @staticmethod
    def hold(
        *,
        unmask: Optional[tuple[str, ...]] = None,
        debugger: Optional[Callable[[processor.Arguments], Any]] = None,
    ) -> Callable[[Callable[P, Tp]], Callable[P, Try[Tp]]]:
        """Try context decorator

        Unmask and record arguments in case of Failure.
        """

    @staticmethod
    def hold(  # type: ignore
        func: Optional[Callable[P, Tp]] = None,
        /,
        *,
        unmask: Optional[tuple[str, ...]] = None,
        debugger: Optional[Callable[[processor.Arguments], Any]] = None,
    ) -> Callable[P, Try[Tp]] | Callable[[Callable[P, Tp]], Callable[P, Try[Tp]]]:
        """Try context decorator"""

        def wrap(func: Callable[P, Tp], /) -> Callable[P, Try[Tp]]:
            return _hold(func=func, unmask=unmask, debugger=debugger)

        if func is None:
            return wrap
        else:
            return wrap(func)


def _hold(
    *,
    func: Callable[P, Tp],
    unmask: Optional[tuple[str, ...]] = None,
    debugger: Optional[Callable[[processor.Arguments], Any]] = None,
) -> Callable[P, Try[Tp]]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Try[Tp]:
        try:
            return Success[Tp](func(*args, **kwargs))
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
            return Failure[Tp](exception)

    return wrapper


class Failure(Try[Tp], extractor.Extractor):
    """Failure"""

    __match_args__ = ("exception",)

    def __init__(self, exception: Exception, /):
        self.exception = exception

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.exception)})"

    def __eq__(self, other: Try[Tp]) -> bool:  # type: ignore
        match other.pattern:
            case Failure(exception):
                return self.exception == exception
            case Success():
                return False

    def __iter__(self) -> Generator[Try[Tp], None, Tp]:
        raise monad.ShortCircuit(self) from self.exception

    def map(self, _: Callable[[Tp], TTp], /) -> Try[TTp]:
        return cast(Failure[TTp], self)

    def flat_map(self, _: Callable[[Tp], Try[TTp]], /) -> Try[TTp]:
        return cast(Failure[TTp], self)

    def recover(self, func: Callable[[Exception], TTp], /) -> Try[TTp]:
        try:
            if (result := func(self.exception)) is None:
                return cast(Failure[TTp], self)
            else:
                return Success[TTp](result)
        except Exception as exception:
            return Failure[TTp](exception)

    def recover_with(self, func: Callable[[Exception], Try[TTp]], /) -> Try[TTp]:
        return func(self.exception)

    @property
    def to_either(self) -> either.Either[Exception, Tp]:
        return either.Left(self.exception)

    @property
    def to_option(self) -> option.Option[Tp]:
        return option.VOID

    def fold(
        self,
        *,
        failure: Callable[[Exception], U],
        success: Callable[[Tp], U],
    ) -> U:
        return failure(self.exception)

    def is_failure(self) -> Literal[True]:
        return True

    def is_success(self) -> Literal[False]:
        return False

    def get(self) -> Tp:
        raise ValueError() from self.exception

    def get_or_else(self, default: Callable[..., Ep], /) -> Ep:
        return default()

    @property
    def pattern(self) -> SubType[Tp]:
        return self


class Success(Try[Tp], extractor.Extractor):
    """Success"""

    __match_args__ = ("value",)

    def __init__(self, value: Tp, /):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other: Try[Tp]) -> bool:  # type: ignore
        match other.pattern:
            case Failure():
                return False
            case Success(value):
                return self.value == value

    def __iter__(self) -> Generator[Try[Tp], None, Tp]:
        yield self
        return self.value

    def map(self, func: Callable[[Tp], TTp], /) -> Try[TTp]:
        return Success[TTp](func(self.value))

    def flat_map(self, func: Callable[[Tp], Try[TTp]], /) -> Try[TTp]:
        return func(self.value)

    def recover(self, _: Callable[[Exception], TTp], /) -> Try[TTp]:
        return cast(Try[TTp], self)

    def recover_with(self, _: Callable[[Exception], Try[TTp]], /) -> Try[TTp]:
        return cast(Try[TTp], self)

    @property
    def to_either(self) -> either.Either[Exception, Tp]:
        return either.Right(self.value)

    @property
    def to_option(self) -> option.Option[Tp]:
        return option.Some[Tp](self.value)

    def fold(
        self,
        *,
        failure: Callable[[Exception], TTp],
        success: Callable[[Tp], TTp],
    ) -> TTp:
        return success(self.value)

    def is_failure(self) -> Literal[False]:
        return False

    def is_success(self) -> Literal[True]:
        return True

    def get(self) -> Tp:
        return self.value

    def get_or_else(self, default: Callable[..., Any], /) -> Tp:
        return self.value

    @property
    def pattern(self) -> SubType[Tp]:
        return self


SubType: TypeAlias = Failure[Tp] | Success[Tp]
TryDo: TypeAlias = Generator[Try[Any], None, Tp]
