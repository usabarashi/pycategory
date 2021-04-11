"""Option"""
from __future__ import annotations

import dataclasses
from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Callable, Generator, Generic, Literal, TypeVar, Union

T = TypeVar("T")
TT = TypeVar("TT")
EE = TypeVar("EE")
U = TypeVar("U")


class Option(ABC, Generic[T]):
    """Option"""

    @abstractmethod
    def __call__(self) -> Generator[Option[T], Option[T], T]:
        raise NotImplementedError

    @abstractmethod
    def map(self, functor: Callable[[T], TT]) -> Option[TT]:
        raise NotImplementedError

    @abstractmethod
    def flatmap(self, functor: Callable[[T], Option[TT]]) -> Option[TT]:
        raise NotImplementedError

    @abstractmethod
    def fold(self, *, void: Callable[..., U], some: Callable[[T], U]) -> U:
        raise NotImplementedError

    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def not_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_or_else(self, default: Callable[..., EE]) -> Union[EE, T]:
        raise NotImplementedError

    @abstractproperty
    def pattern(self) -> SubType[T]:
        raise NotImplementedError

    def method(self, functor: Callable[[Option[T]], TT]) -> TT:
        raise NotImplementedError

    @staticmethod
    def do(generator_fuction: Callable[..., OptionDo[T]]) -> Callable[..., Option[T]]:
        def wrapper(*args: Any, **kwargs: Any) -> Option[T]:
            def recur(
                generator: OptionDo[T],
                prev: Union[Any, Option[Any]],
            ) -> Option[T]:
                try:
                    result = generator.send(prev)
                except StopIteration as last:
                    # Some case
                    return Some[T](value=last.value)
                # Void case
                if isinstance(result, Void):
                    return result
                return recur(generator, result)

            return recur(generator_fuction(*args, **kwargs), None)

        return wrapper


@dataclasses.dataclass(frozen=True)
class Void(Option[T]):
    """Void"""

    def __new__(cls) -> Void[T]:
        if not hasattr(cls, "_singleton"):
            cls._singleton = super(Void, cls).__new__(cls)
        return cls._singleton

    def __bool__(self) -> Literal[False]:
        return False

    def __call__(self) -> Generator[Void[T], Void[T], T]:
        yield self
        raise GeneratorExit(self)

    def map(self, functor: Callable[[T], TT]) -> Void[TT]:
        return Void[TT]()

    def flatmap(self, functor: Callable[[T], Option[TT]]) -> Void[TT]:
        return Void[TT]()

    def fold(self, *, void: Callable[..., U], some: Callable[[T], U]) -> U:
        return void()

    def is_empty(self) -> Literal[True]:
        return True

    def not_empty(self) -> Literal[False]:
        return False

    def get(self) -> T:
        raise ValueError(self)

    def get_or_else(self, default: Callable[..., EE]) -> EE:
        return default()

    @property
    def pattern(self) -> SubType[T]:
        return self

    def method(self, functor: Callable[[Void[T]], TT]) -> TT:
        return functor(self)


@dataclasses.dataclass(frozen=True)
class Some(Option[T]):
    """Some"""

    value: T

    def __bool__(self) -> Literal[True]:
        return True

    def __call__(self) -> Generator[Some[T], Some[T], T]:
        yield self
        return self.value

    def map(self, functor: Callable[[T], TT]) -> Some[TT]:
        return Some[TT](value=functor(self.value))

    def flatmap(self, functor: Callable[[T], Option[TT]]) -> Option[TT]:
        return functor(self.value)

    def fold(self, *, void: Callable[..., U], some: Callable[[T], U]) -> U:
        return some(self.value)

    def is_empty(self) -> Literal[False]:
        return False

    def not_empty(self) -> Literal[True]:
        return True

    def get(self) -> T:
        return self.value

    def get_or_else(self, default: Callable[..., Any]) -> T:
        return self.value

    @property
    def pattern(self) -> SubType[T]:
        return self

    def method(self, functor: Callable[[Some[T]], TT]) -> TT:
        return functor(self)


SubType = Union[Void[T], Some[T]]
OptionDo = Generator[Union[Any, Option[Any]], Union[Any, Option[Any]], T]
