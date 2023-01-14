from __future__ import annotations

from typing import Callable, Generic, TypeVar

from . import curry_

S1m = TypeVar("S1m", contravariant=True)
S2m = TypeVar("S2m", contravariant=True)
S3m = TypeVar("S3m", contravariant=True)
S4m = TypeVar("S4m", contravariant=True)
S5m = TypeVar("S5m", contravariant=True)
S6m = TypeVar("S6m", contravariant=True)
S7m = TypeVar("S7m", contravariant=True)
S8m = TypeVar("S8m", contravariant=True)
S9m = TypeVar("S9m", contravariant=True)
S10m = TypeVar("S10m", contravariant=True)
S11m = TypeVar("S11m", contravariant=True)
S12m = TypeVar("S12m", contravariant=True)
S13m = TypeVar("S13m", contravariant=True)
S14m = TypeVar("S14m", contravariant=True)
S15m = TypeVar("S15m", contravariant=True)
S16m = TypeVar("S16m", contravariant=True)
S17m = TypeVar("S17m", contravariant=True)
S18m = TypeVar("S18m", contravariant=True)
S19m = TypeVar("S19m", contravariant=True)
S20m = TypeVar("S20m", contravariant=True)
S21m = TypeVar("S21m", contravariant=True)
S22m = TypeVar("S22m", contravariant=True)
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
            return self._func(*args)

        return tupled_arg_function


class Function3(Generic[S1m, S2m, S3m, Tp], Function):
    def __init__(self, func: Callable[[S1m, S2m, S3m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1m, arg2: S2m, arg3: S3m) -> Tp:
        return self._func(arg1, arg2, arg3)

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1m, S2m, S3m], /) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function4(Generic[S1m, S2m, S3m, S4m, Tp], Function):
    def __init__(self, func: Callable[[S1m, S2m, S3m, S4m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1m, arg2: S2m, arg3: S3m, arg4: S4m) -> Tp:
        return self._func(arg1, arg2, arg3, arg4)

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1m, S2m, S3m, S4m], /) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function5(Generic[S1m, S2m, S3m, S4m, S5m, Tp], Function):
    def __init__(self, func: Callable[[S1m, S2m, S3m, S4m, S5m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1m, arg2: S2m, arg3: S3m, arg4: S4m, arg5: S5m) -> Tp:
        return self._func(arg1, arg2, arg3, arg4, arg5)

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1m, S2m, S3m, S4m, S5m], /) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function6(Generic[S1m, S2m, S3m, S4m, S5m, S6m, Tp], Function):
    def __init__(self, func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self, /, arg1: S1m, arg2: S2m, arg3: S3m, arg4: S4m, arg5: S5m, arg6: S6m
    ) -> Tp:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6)

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1m, S2m, S3m, S4m, S5m, S6m], /) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function7(Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, Tp], Function):
    def __init__(self, func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
    ) -> Tp:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m], /
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function8(Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, Tp], Function):
    def __init__(self, func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
    ) -> Tp:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8)

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m], /
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function9(Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, Tp], Function):
    def __init__(
        self, func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m], Tp], /
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
    ) -> Tp:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9)

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m], /
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function10(
    Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, Tp], Function
):
    def __init__(
        self, func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m], Tp], /
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
    ) -> Tp:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10)

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m], /
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function11(
    Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, Tp], Function
):
    def __init__(
        self,
        func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m], Tp],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
    ) -> Tp:
        return self._func(
            arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m], /
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function12(
    Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, Tp], Function
):
    def __init__(
        self,
        func: Callable[
            [S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m], Tp
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
    ) -> Tp:
        return self._func(
            arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function13(
    Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m, Tp],
    Function,
):
    def __init__(
        self,
        func: Callable[
            [S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m], Tp
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
        arg13: S13m,
    ) -> Tp:
        return self._func(
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            arg6,
            arg7,
            arg8,
            arg9,
            arg10,
            arg11,
            arg12,
            arg13,
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[
                S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m
            ],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function14(
    Generic[
        S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m, S14m, Tp
    ],
    Function,
):
    def __init__(
        self,
        func: Callable[
            [S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m, S14m],
            Tp,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
        arg13: S13m,
        arg14: S14m,
    ) -> Tp:
        return self._func(
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            arg6,
            arg7,
            arg8,
            arg9,
            arg10,
            arg11,
            arg12,
            arg13,
            arg14,
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
            ],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function15(
    Generic[
        S1m,
        S2m,
        S3m,
        S4m,
        S5m,
        S6m,
        S7m,
        S8m,
        S9m,
        S10m,
        S11m,
        S12m,
        S13m,
        S14m,
        S15m,
        Tp,
    ],
    Function,
):
    def __init__(
        self,
        func: Callable[
            [
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
            ],
            Tp,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
        arg13: S13m,
        arg14: S14m,
        arg15: S15m,
    ) -> Tp:
        return self._func(
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            arg6,
            arg7,
            arg8,
            arg9,
            arg10,
            arg11,
            arg12,
            arg13,
            arg14,
            arg15,
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
            ],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function16(
    Generic[
        S1m,
        S2m,
        S3m,
        S4m,
        S5m,
        S6m,
        S7m,
        S8m,
        S9m,
        S10m,
        S11m,
        S12m,
        S13m,
        S14m,
        S15m,
        S16m,
        Tp,
    ],
    Function,
):
    def __init__(
        self,
        func: Callable[
            [
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
            ],
            Tp,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
        arg13: S13m,
        arg14: S14m,
        arg15: S15m,
        arg16: S16m,
    ) -> Tp:
        return self._func(
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            arg6,
            arg7,
            arg8,
            arg9,
            arg10,
            arg11,
            arg12,
            arg13,
            arg14,
            arg15,
            arg16,
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
            ],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function17(
    Generic[
        S1m,
        S2m,
        S3m,
        S4m,
        S5m,
        S6m,
        S7m,
        S8m,
        S9m,
        S10m,
        S11m,
        S12m,
        S13m,
        S14m,
        S15m,
        S16m,
        S17m,
        Tp,
    ],
    Function,
):
    def __init__(
        self,
        func: Callable[
            [
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
            ],
            Tp,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
        arg13: S13m,
        arg14: S14m,
        arg15: S15m,
        arg16: S16m,
        arg17: S17m,
    ) -> Tp:
        return self._func(
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            arg6,
            arg7,
            arg8,
            arg9,
            arg10,
            arg11,
            arg12,
            arg13,
            arg14,
            arg15,
            arg16,
            arg17,
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
            ],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function18(
    Generic[
        S1m,
        S2m,
        S3m,
        S4m,
        S5m,
        S6m,
        S7m,
        S8m,
        S9m,
        S10m,
        S11m,
        S12m,
        S13m,
        S14m,
        S15m,
        S16m,
        S17m,
        S18m,
        Tp,
    ],
    Function,
):
    def __init__(
        self,
        func: Callable[
            [
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
                S18m,
            ],
            Tp,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
        arg13: S13m,
        arg14: S14m,
        arg15: S15m,
        arg16: S16m,
        arg17: S17m,
        arg18: S18m,
    ) -> Tp:
        return self._func(
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            arg6,
            arg7,
            arg8,
            arg9,
            arg10,
            arg11,
            arg12,
            arg13,
            arg14,
            arg15,
            arg16,
            arg17,
            arg18,
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
                S18m,
            ],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function19(
    Generic[
        S1m,
        S2m,
        S3m,
        S4m,
        S5m,
        S6m,
        S7m,
        S8m,
        S9m,
        S10m,
        S11m,
        S12m,
        S13m,
        S14m,
        S15m,
        S16m,
        S17m,
        S18m,
        S19m,
        Tp,
    ],
    Function,
):
    def __init__(
        self,
        func: Callable[
            [
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
                S18m,
                S19m,
            ],
            Tp,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
        arg13: S13m,
        arg14: S14m,
        arg15: S15m,
        arg16: S16m,
        arg17: S17m,
        arg18: S18m,
        arg19: S19m,
    ) -> Tp:
        return self._func(
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            arg6,
            arg7,
            arg8,
            arg9,
            arg10,
            arg11,
            arg12,
            arg13,
            arg14,
            arg15,
            arg16,
            arg17,
            arg18,
            arg19,
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
                S18m,
                S19m,
            ],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function20(
    Generic[
        S1m,
        S2m,
        S3m,
        S4m,
        S5m,
        S6m,
        S7m,
        S8m,
        S9m,
        S10m,
        S11m,
        S12m,
        S13m,
        S14m,
        S15m,
        S16m,
        S17m,
        S18m,
        S19m,
        S20m,
        Tp,
    ],
    Function,
):
    def __init__(
        self,
        func: Callable[
            [
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
                S18m,
                S19m,
                S20m,
            ],
            Tp,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
        arg13: S13m,
        arg14: S14m,
        arg15: S15m,
        arg16: S16m,
        arg17: S17m,
        arg18: S18m,
        arg19: S19m,
        arg20: S20m,
    ) -> Tp:
        return self._func(
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            arg6,
            arg7,
            arg8,
            arg9,
            arg10,
            arg11,
            arg12,
            arg13,
            arg14,
            arg15,
            arg16,
            arg17,
            arg18,
            arg19,
            arg20,
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
                S18m,
                S19m,
                S20m,
            ],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function21(
    Generic[
        S1m,
        S2m,
        S3m,
        S4m,
        S5m,
        S6m,
        S7m,
        S8m,
        S9m,
        S10m,
        S11m,
        S12m,
        S13m,
        S14m,
        S15m,
        S16m,
        S17m,
        S18m,
        S19m,
        S20m,
        S21m,
        Tp,
    ],
    Function,
):
    def __init__(
        self,
        func: Callable[
            [
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
                S18m,
                S19m,
                S20m,
                S21m,
            ],
            Tp,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
        arg13: S13m,
        arg14: S14m,
        arg15: S15m,
        arg16: S16m,
        arg17: S17m,
        arg18: S18m,
        arg19: S19m,
        arg20: S20m,
        arg21: S21m,
    ) -> Tp:
        return self._func(
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            arg6,
            arg7,
            arg8,
            arg9,
            arg10,
            arg11,
            arg12,
            arg13,
            arg14,
            arg15,
            arg16,
            arg17,
            arg18,
            arg19,
            arg20,
            arg21,
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
                S18m,
                S19m,
                S20m,
                S21m,
            ],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function22(
    Generic[
        S1m,
        S2m,
        S3m,
        S4m,
        S5m,
        S6m,
        S7m,
        S8m,
        S9m,
        S10m,
        S11m,
        S12m,
        S13m,
        S14m,
        S15m,
        S16m,
        S17m,
        S18m,
        S19m,
        S20m,
        S21m,
        S22m,
        Tp,
    ],
    Function,
):
    def __init__(
        self,
        func: Callable[
            [
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
                S18m,
                S19m,
                S20m,
                S21m,
                S22m,
            ],
            Tp,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1m,
        arg2: S2m,
        arg3: S3m,
        arg4: S4m,
        arg5: S5m,
        arg6: S6m,
        arg7: S7m,
        arg8: S8m,
        arg9: S9m,
        arg10: S10m,
        arg11: S11m,
        arg12: S12m,
        arg13: S13m,
        arg14: S14m,
        arg15: S15m,
        arg16: S16m,
        arg17: S17m,
        arg18: S18m,
        arg19: S19m,
        arg20: S20m,
        arg21: S21m,
        arg22: S22m,
    ) -> Tp:
        return self._func(
            arg1,
            arg2,
            arg3,
            arg4,
            arg5,
            arg6,
            arg7,
            arg8,
            arg9,
            arg10,
            arg11,
            arg12,
            arg13,
            arg14,
            arg15,
            arg16,
            arg17,
            arg18,
            arg19,
            arg20,
            arg21,
            arg22,
        )

    def apply(self, *args: ..., **kwargs: ...):
        return self.__call__(*args, **kwargs)

    @property
    def curried(self):
        return curry_.curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[
                S1m,
                S2m,
                S3m,
                S4m,
                S5m,
                S6m,
                S7m,
                S8m,
                S9m,
                S10m,
                S11m,
                S12m,
                S13m,
                S14m,
                S15m,
                S16m,
                S17m,
                S18m,
                S19m,
                S20m,
                S21m,
                S22m,
            ],
            /,
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function
