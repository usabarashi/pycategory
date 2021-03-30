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


class Option(ABC, Generic[T]):
    """Option"""

    @abstractmethod
    def __call__(
        self, /, convert: Optional[Callable[[OptionST[T]], EE]] = None
    ) -> Generator[Union[EE, OptionST[T]], None, T]:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> Union[NoReturn, T]:
        raise NotImplementedError

    @abstractmethod
    def get_or_else(self, default: Optional[Callable[..., TT]] = None) -> Union[T, TT]:
        raise NotImplementedError

    @abstractmethod
    def map(self, functor: Callable[[T], TT]) -> Option[TT]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, functor: Callable[[T], Option[TT]]) -> Option[TT]:
        raise NotImplementedError

    @abstractmethod
    def fold(self, /, void: Callable[..., TT], some: Callable[[T], TT]) -> TT:
        raise NotImplementedError

    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def not_empty(self) -> bool:
        raise NotImplementedError

    @staticmethod
    def do(
        generator_fuction: Callable[..., OptionGenerator[T]]
    ) -> Callable[..., OptionST[T]]:
        def wrapper(*args: Any, **kwargs: Any) -> OptionST[T]:
            def recur(
                generator: OptionGenerator[T],
                prev: Any,
            ) -> OptionST[T]:
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    # Some case
                    return Some(value=last.value)
                # Void case
                if isinstance(result, Void):
                    return result
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return wrapper


class Void(Option[T]):
    """Void"""

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(
        self, /, convert: Optional[Callable[[OptionST[T]], EE]] = None
    ) -> Generator[Union[EE, OptionST[T]], None, T]:
        if convert is not None:
            yield convert(self)
            raise GeneratorExit(self)
        else:
            yield self
            raise GeneratorExit(self)

    def get(self) -> NoReturn:
        raise ValueError(self)

    def get_or_else(self, default: Optional[Callable[..., TT]] = None) -> Union[T, TT]:
        if default is not None:
            return default()
        raise ValueError(self)

    def map(self, functor: Callable[[T], TT]) -> Option[TT]:
        return Void()

    def flatmap(self, functor: Callable[[T], Option[TT]]) -> Option[TT]:
        return Void()

    def fold(self, /, void: Callable[..., TT], some: Callable[[T], TT]) -> TT:
        return void()

    def is_empty(self) -> Literal[True]:
        return True

    def not_empty(self) -> Literal[False]:
        return False


@dataclasses.dataclass
class Some(Option[T]):
    """Some"""

    value: T

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(
        self, /, convert: Optional[Callable[[OptionST[T]], EE]] = None
    ) -> Generator[Union[EE, OptionST[T]], None, T]:
        if convert is not None:
            yield convert(self)
            raise GeneratorExit(self)
        else:
            yield self
            return self.value

    def get(self) -> T:
        return self.value

    def get_or_else(self, default: Optional[Callable[..., TT]] = None) -> Union[T, TT]:
        return self.value

    def map(self, functor: Callable[[T], TT]) -> Option[TT]:
        return Some(value=functor(self.value))

    def flatmap(self, functor: Callable[[T], Option[TT]]) -> Option[TT]:
        return functor(self.value)

    def fold(self, /, void: Callable[..., TT], some: Callable[[T], TT]) -> TT:
        return some(self.value)

    def is_empty(self) -> Literal[False]:
        return False

    def not_empty(self) -> Literal[True]:
        return True


OptionST = Union[Void[T], Some[T]]
OptionDo = Generator[Union[OptionST[T], Any], Any, T]
OptionGenerator = Generator[
    Union[OptionST[T], Any],
    Union[OptionST[T], Any],
    T,
]
