"""Try"""

from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Generator
from functools import wraps
from typing import Any, Callable, Final, Literal, Optional, cast, overload

from pycategory.data import collection, either, option
from pycategory.runtime import processor
from pycategory.trait import extension, monad
from pycategory.type import extractor


class Try[A](extension.Extension, monad.Monad[A], ABC):
    """Try"""

    @abstractmethod
    def __iter__(self) -> Generator[Try[A], None, A]:
        raise NotImplementedError()

    @abstractmethod
    def map[B](self, func: Callable[[A], B], /) -> Try[B]:
        raise NotImplementedError()

    @staticmethod
    def pure(value: A) -> Try[A]:  # type: ignore
        return Success[A](value)

    @abstractmethod
    def flat_map[B](self, func: Callable[[A], Try[B]], /) -> Try[B]:  # type: ignore
        raise NotImplementedError()

    @abstractmethod
    def recover[E](self, func: Callable[[Exception], E], /) -> Try[E]:
        raise NotImplementedError()

    @abstractmethod
    def recover_with[E](self, func: Callable[[Exception], Try[E]], /) -> Try[E]:
        raise NotImplementedError()

    @abstractproperty
    def to_either(self) -> either.Either[Exception, A]:
        raise NotImplementedError()

    @abstractproperty
    def to_option(self) -> option.Option[A]:
        raise NotImplementedError()

    @abstractmethod
    def fold[
        U
    ](self, *, failure: Callable[[Exception], U], success: Callable[[A], U],) -> U:
        raise NotImplementedError()

    @abstractmethod
    def is_failure(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_success(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> A:
        raise NotImplementedError()

    @abstractmethod
    def get_or_else[E](self, default: Callable[..., E], /) -> E | A:
        raise NotImplementedError()

    @abstractproperty
    def pattern(self) -> SubType[A]:
        raise NotImplementedError()

    @staticmethod
    def do[  # type: ignore
        **P
    ](context: Callable[P, Generator[Try[Any], None, A]], /) -> Callable[P, Try[A]]:  # type: ignore
        """map, flat_map combination syntax sugar."""
        return cast(Callable[P, Try[A]], monad.Monad.do(context))

    @overload
    @staticmethod
    def hold[**P](func: Callable[P, A], /) -> Callable[P, Try[A]]:
        """Try context decorator"""

    @overload
    @staticmethod
    def hold[
        **P
    ](
        *,
        unmask: Optional[tuple[str, ...]] = None,
        debugger: Optional[Callable[[processor.Arguments], Any]] = None,
    ) -> Callable[[Callable[P, A]], Callable[P, Try[A]]]:
        """Try context decorator

        Unmask and record arguments in case of Failure.
        """

    @staticmethod
    def hold[
        **P
    ](  # type: ignore
        func: Optional[Callable[P, A]] = None,
        /,
        *,
        unmask: Optional[tuple[str, ...]] = None,
        debugger: Optional[Callable[[processor.Arguments], Any]] = None,
    ) -> (Callable[P, Try[A]] | Callable[[Callable[P, A]], Callable[P, Try[A]]]):
        """Try context decorator"""

        def wrap(func: Callable[P, A], /) -> Callable[P, Try[A]]:
            return _hold(func=func, unmask=unmask, debugger=debugger)

        if func is None:
            return wrap
        else:
            return wrap(func)


def _hold[
    **P, A
](
    *,
    func: Callable[P, A],
    unmask: Optional[tuple[str, ...]] = None,
    debugger: Optional[Callable[[processor.Arguments], Any]] = None,
) -> Callable[P, Try[A]]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Try[A]:
        try:
            return Success[A](func(*args, **kwargs))
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
            return Failure[A](exception)

    return wrapper


class Failure[A](Try[A], extractor.Extractor):
    """Failure"""

    __match_args__ = ("exception",)

    def __init__(self, exception: Exception, /):
        self.exception: Final = exception

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.exception)})"

    def __eq__(self, other: Try[A]) -> bool:  # type: ignore
        match other.pattern:
            case Failure(exception):
                return self.exception == exception
            case Success():
                return False

    def __iter__(self) -> Generator[Try[A], None, A]:
        raise monad.ShortCircuit(self) from self.exception

    def map[B](self, _: Callable[[A], B], /) -> Try[B]:
        return cast(Failure[B], self)

    def flat_map[B](self, _: Callable[[A], Try[B]], /) -> Try[B]:
        return cast(Failure[B], self)

    def recover[E](self, func: Callable[[Exception], E], /) -> Try[E]:
        try:
            if (result := func(self.exception)) is None:
                return cast(Failure[E], self)
            else:
                return Success[E](result)
        except Exception as exception:
            return Failure[E](exception)

    def recover_with[E](self, func: Callable[[Exception], Try[E]], /) -> Try[E]:
        return func(self.exception)

    @property
    def to_either(self) -> either.Either[Exception, A]:
        return either.Left(self.exception)

    @property
    def to_option(self) -> option.Option[A]:
        return option.VOID

    def fold[
        U
    ](self, *, failure: Callable[[Exception], U], success: Callable[[A], U],) -> U:
        return failure(self.exception)

    def is_failure(self) -> Literal[True]:
        return True

    def is_success(self) -> Literal[False]:
        return False

    def get(self) -> A:
        raise ValueError() from self.exception

    def get_or_else[E](self, default: Callable[..., E], /) -> E:
        return default()

    @property
    def pattern(self) -> SubType[A]:
        return self


class Success[A](Try[A], extractor.Extractor):
    """Success"""

    __match_args__ = ("value",)

    def __init__(self, value: A, /):
        self.value: Final = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other: Try[A]) -> bool:  # type: ignore
        match other.pattern:
            case Failure():
                return False
            case Success(value):
                return self.value == value

    def __iter__(self) -> Generator[Try[A], None, A]:
        yield self
        return self.value

    def map[B](self, func: Callable[[A], B], /) -> Try[B]:
        return Success[B](func(self.value))

    def flat_map[B](self, func: Callable[[A], Try[B]], /) -> Try[B]:
        return func(self.value)

    def recover[E](self, _: Callable[[Exception], E], /) -> Try[E]:
        return cast(Try[E], self)

    def recover_with[E](self, _: Callable[[Exception], Try[E]], /) -> Try[E]:
        return cast(Try[E], self)

    @property
    def to_either(self) -> either.Either[Exception, A]:
        return either.Right(self.value)

    @property
    def to_option(self) -> option.Option[A]:
        return option.Some[A](self.value)

    def fold[
        U
    ](self, *, failure: Callable[[Exception], U], success: Callable[[A], U],) -> U:
        return success(self.value)

    def is_failure(self) -> Literal[False]:
        return False

    def is_success(self) -> Literal[True]:
        return True

    def get(self) -> A:
        return self.value

    def get_or_else(self, default: Callable[..., Any], /) -> A:
        return self.value

    @property
    def pattern(self) -> SubType[A]:
        return self


type SubType[A] = Failure[A] | Success[A]
type TryDo[A] = Generator[Try[Any], None, A]
