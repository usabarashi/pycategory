from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Callable, Generator, Generic, Literal, Optional, TypeVar, Union

T = TypeVar("T")
TT = TypeVar("TT")
EE = TypeVar("EE")


class Option(ABC, Generic[T]):
    """Option"""

    @abstractmethod
    def __call__(
        self, /, convert: Optional[Callable[[Option[T]], EE]] = None
    ) -> Generator[Union[EE, Option[T]], None, T]:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> T:
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

    @abstractproperty
    def pattern(self) -> SubType[T]:
        raise NotImplementedError

    @staticmethod
    def do(
        generator_fuction: Callable[..., OptionGenerator[T]]
    ) -> Callable[..., Option[T]]:
        def wrapper(*args: Any, **kwargs: Any) -> Option[T]:
            def recur(
                generator: OptionGenerator[T],
                prev: Any,
            ) -> Option[T]:
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

    def convart(self, functor: Callable[[Option[T]], TT]) -> TT:
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class Void(Option[T]):
    """Void"""

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(
        self, /, convert: Optional[Callable[[Option[T]], EE]] = None
    ) -> Generator[Union[EE, Option[T]], None, T]:
        if convert is not None:
            yield convert(self)
            raise GeneratorExit(self)
        else:
            yield self
            raise GeneratorExit(self)

    def get(self) -> T:
        raise ValueError(self)

    def get_or_else(self, default: Optional[Callable[..., TT]] = None) -> Union[T, TT]:
        if default is not None:
            return default()
        raise ValueError(self)

    def map(self, functor: Callable[[T], TT]) -> Option[TT]:
        return Void[T]()

    def flatmap(self, functor: Callable[[T], Option[TT]]) -> Option[TT]:
        return Void[T]()

    def fold(self, /, void: Callable[..., TT], some: Callable[[T], TT]) -> TT:
        return void()

    def is_empty(self) -> Literal[True]:
        return True

    def not_empty(self) -> Literal[False]:
        return False

    @property
    def pattern(self) -> SubType[T]:
        return self

    def convert(self, functor: Callable[[Void[T]], TT]) -> TT:
        return functor(self)


@dataclasses.dataclass(frozen=True)
class Some(Option[T]):
    """Some"""

    value: T

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(
        self, /, convert: Optional[Callable[[Option[T]], EE]] = None
    ) -> Generator[Union[EE, Option[T]], None, T]:
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

    @property
    def pattern(self) -> SubType[T]:
        return self

    def convert(self, functor: Callable[[Some[T]], TT]) -> TT:
        return functor(self)


SubType = Union[Void[T], Some[T]]
OptionDo = Generator[Union[Option[T], Any], Any, T]
OptionGenerator = Generator[
    Union[Option[T], Any],
    Union[Option[T], Any],
    T,
]
