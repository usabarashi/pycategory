from __future__ import annotations

from typing import Callable, Generic, TypeVar

from . import curry_

S1m = TypeVar("S1m", contravariant=True)
S2m = TypeVar("S2m", contravariant=True)
Sd1m = TypeVar("Sd1m", contravariant=True)
Tp = TypeVar("Tp", covariant=True)
Tdp = TypeVar("Tdp", covariant=True)


class Function:
    ...


class Function1(Generic[S1m, Tp], Function):
    def __init__(self, func: Callable[[S1m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, arg: S1m, /) -> Tp:
        return self._func(arg)

    apply = __call__

    def compose(
        self, other: Callable[[Sd1m], Tdp] | Function1[Sd1m, Tdp]
    ) -> Function1[Sd1m, Tp]:
        return Function1[Sd1m, Tp](lambda arg: self(other(arg)))

    def and_then(
        self, other: Callable[[Sd1m], Tdp] | Function1[Sd1m, Tdp]
    ) -> Function1[Tp, Tdp]:
        return Function1[Tp, Tdp](lambda arg: other(self(arg)))


class Function2(Generic[S1m, S2m, Tp], Function):
    def __init__(self, func: Callable[[S1m, S2m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1m, arg2: S2m) -> Tp:
        return self._func(arg1, arg2)

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1m, S2m], /) -> Tp:
            return self._func(*args[:2])

        return tupled_arg_function
