from __future__ import annotations

import inspect
from collections.abc import Callable
from copy import deepcopy
from functools import wraps
from typing import Any, Generic, Optional, ParamSpec, TypeVar, overload

from . import processor

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
P = ParamSpec("P")

LAST_ONE = 1
# Limit number of Type variables that can be parsed by the signature.
LIMIT_NUMBER_OF_TYPE_VARIABLES = 22


class Function(Callable):
    ...


class Function1(Generic[S1m, Tp], Function):
    def __init__(self, func: Callable[[S1m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, arg: S1m, /) -> Tp:
        return self._func(arg)

    apply = __call__

    def compose(self, other: Callable[[S2m], S1m]) -> Function1[S2m, Tp]:
        return Function1[Sd1m, Tp](lambda arg: self(other(arg)))

    def and_then(self, other: Callable[[Tp], Tdp]) -> Function1[S1m, Tdp]:
        return Function1[S1m, Tdp](lambda arg: other(self(arg)))


class FunctionN(Function):
    ...


class Function2(Generic[S1m, S2m, Tp], FunctionN):
    def __init__(self, func: Callable[[S1m, S2m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1m, arg2: S2m) -> Tp:
        return self._func(arg1, arg2)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1m, S2m], /) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function3(Generic[S1m, S2m, S3m, Tp], FunctionN):
    def __init__(self, func: Callable[[S1m, S2m, S3m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1m, arg2: S2m, arg3: S3m) -> Tp:
        return self._func(arg1, arg2, arg3)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1m, S2m, S3m], /) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function4(Generic[S1m, S2m, S3m, S4m, Tp], FunctionN):
    def __init__(self, func: Callable[[S1m, S2m, S3m, S4m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1m, arg2: S2m, arg3: S3m, arg4: S4m) -> Tp:
        return self._func(arg1, arg2, arg3, arg4)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1m, S2m, S3m, S4m], /) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function5(Generic[S1m, S2m, S3m, S4m, S5m, Tp], FunctionN):
    def __init__(self, func: Callable[[S1m, S2m, S3m, S4m, S5m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1m, arg2: S2m, arg3: S3m, arg4: S4m, arg5: S5m) -> Tp:
        return self._func(arg1, arg2, arg3, arg4, arg5)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1m, S2m, S3m, S4m, S5m], /) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function6(Generic[S1m, S2m, S3m, S4m, S5m, S6m, Tp], FunctionN):
    def __init__(self, func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m], Tp], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self, /, arg1: S1m, arg2: S2m, arg3: S3m, arg4: S4m, arg5: S5m, arg6: S6m
    ) -> Tp:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1m, S2m, S3m, S4m, S5m, S6m], /) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function7(Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, Tp], FunctionN):
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m], /
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function8(Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, Tp], FunctionN):
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m], /
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function9(Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, Tp], FunctionN):
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m], /
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function10(
    Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, Tp], FunctionN
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m], /
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function11(
    Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, Tp], FunctionN
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m], /
        ) -> Tp:
            return self._func(*args)

        return tupled_arg_function


class Function12(
    Generic[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, Tp],
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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
    FunctionN,
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

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

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


@overload
def function(func: Callable[[S1m], Tp], /) -> Function1[S1m, Tp]:
    ...


@overload
def function(func: Callable[[S1m, S2m], Tp], /) -> Function2[S1m, S2m, Tp]:
    ...


@overload
def function(func: Callable[[S1m, S2m, S3m], Tp], /) -> Function3[S1m, S2m, S3m, Tp]:
    ...


@overload
def function(
    func: Callable[[S1m, S2m, S3m, S4m], Tp], /
) -> Function4[S1m, S2m, S3m, S4m, Tp]:
    ...


@overload
def function(
    func: Callable[[S1m, S2m, S3m, S4m, S5m], Tp], /
) -> Function5[S1m, S2m, S3m, S4m, S5m, Tp]:
    ...


@overload
def function(
    func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m], Tp], /
) -> Function6[S1m, S2m, S3m, S4m, S5m, S6m, Tp]:
    ...


@overload
def function(
    func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m], Tp], /
) -> Function7[S1m, S2m, S3m, S4m, S5m, S6m, S7m, Tp]:
    ...


@overload
def function(
    func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m], Tp], /
) -> Function8[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, Tp]:
    ...


@overload
def function(
    func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m], Tp], /
) -> Function9[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, Tp]:
    ...


@overload
def function(
    func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m], Tp], /
) -> Function10[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, Tp]:
    ...


@overload
def function(
    func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m], Tp], /
) -> Function11[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, Tp]:
    ...


@overload
def function(
    func: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m], Tp],
    /,
) -> Function12[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, Tp]:
    ...


@overload
def function(
    func: Callable[
        [S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m], Tp
    ],
    /,
) -> Function13[
    S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m, Tp
]:
    ...


@overload
def function(
    func: Callable[
        [S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m, S14m], Tp
    ],
    /,
) -> Function14[
    S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m, S14m, Tp
]:
    ...


@overload
def function(
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
) -> Function15[
    S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m, S14m, S15m, Tp
]:
    ...


@overload
def function(
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
) -> Function16[
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
]:
    ...


@overload
def function(
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
) -> Function17[
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
]:
    ...


@overload
def function(
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
) -> Function18[
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
]:
    ...


@overload
def function(
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
) -> Function19[
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
]:
    ...


@overload
def function(
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
) -> Function20[
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
]:
    ...


@overload
def function(
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
) -> Function21[
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
]:
    ...


@overload
def function(
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
) -> Function22[
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
]:
    ...


def function(func: Callable[P, Tp], /):
    arguments = inspect.signature(func).parameters.copy()
    match partial_application_scope(arguments=arguments, function=function):
        case 0:
            raise TypeError(func)
        case 1:
            return Function1(func)
        case 2:
            return Function2(func)
        case 3:
            return Function3(func)
        case 4:
            return Function4(func)
        case 5:
            return Function5(func)
        case 6:
            return Function6(func)
        case 7:
            return Function7(func)
        case 8:
            return Function8(func)
        case 9:
            return Function9(func)
        case 10:
            return Function10(func)
        case 11:
            return Function11(func)
        case 12:
            return Function12(func)
        case 13:
            return Function13(func)
        case 14:
            return Function14(func)
        case 15:
            return Function15(func)
        case 16:
            return Function16(func)
        case 17:
            return Function17(func)
        case 18:
            return Function18(func)
        case 19:
            return Function19(func)
        case 20:
            return Function20(func)
        case 21:
            return Function21(func)
        case 22:
            return Function22(func)
        case _:
            raise TypeError(func)


@overload
def curry(function: Callable[[S1m, S2m], Tp], /) -> Function1[S1m, Function1[S2m, Tp]]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m], Tp], /
) -> Function1[S1m, Function1[S2m, Function1[S3m, Tp]]]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m], Tp], /
) -> Function1[S1m, Function1[S2m, Function1[S3m, Function1[S4m, Tp]]]]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m], Tp], /
) -> Function1[S1m, Function1[S2m, Function1[S3m, Function1[S4m, Function1[S5m, Tp]]]]]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m], Tp], /
) -> Function1[
    S1m,
    Function1[S2m, Function1[S3m, Function1[S4m, Function1[S5m, Function1[S6m, Tp]]]]],
]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m], Tp], /
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m, Function1[S4m, Function1[S5m, Function1[S6m, Function1[S7m, Tp]]]]
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m], Tp], /
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m, Function1[S5m, Function1[S6m, Function1[S7m, Function1[S8m, Tp]]]]
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m], Tp], /
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[S6m, Function1[S7m, Function1[S8m, Function1[S9m, Tp]]]],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m], Tp],
    /,
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[S9m, Function1[S10m, Tp]],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m], Tp],
    /,
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[S9m, Function1[S10m, Function1[S11m, Tp]]],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
        [S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m], Tp
    ],
    /,
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m, Function1[S11m, Function1[S12m, Tp]]
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
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
        ],
        T,
    ],
    /,
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m,
                                        Function1[
                                            S11m,
                                            Function1[S12m, Function1[S13m, Tp]],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
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
        ],
        Tp,
    ],
    /,
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m,
                                        Function1[
                                            S11m,
                                            Function1[
                                                S12m,
                                                Function1[S13m, Function1[S14m, Tp]],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
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
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m,
                                        Function1[
                                            S11m,
                                            Function1[
                                                S12m,
                                                Function1[
                                                    S13m,
                                                    Function1[
                                                        S14m, Function1[S15m, Tp]
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
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
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m,
                                        Function1[
                                            S11m,
                                            Function1[
                                                S12m,
                                                Function1[
                                                    S13m,
                                                    Function1[
                                                        S14m,
                                                        Function1[
                                                            S15m, Function1[S16m, Tp]
                                                        ],
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
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
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m,
                                        Function1[
                                            S11m,
                                            Function1[
                                                S12m,
                                                Function1[
                                                    S13m,
                                                    Function1[
                                                        S14m,
                                                        Function1[
                                                            S15m,
                                                            Function1[
                                                                S16m,
                                                                Function1[S17m, Tp],
                                                            ],
                                                        ],
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
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
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m,
                                        Function1[
                                            S11m,
                                            Function1[
                                                S12m,
                                                Function1[
                                                    S13m,
                                                    Function1[
                                                        S14m,
                                                        Function1[
                                                            S15m,
                                                            Function1[
                                                                S16m,
                                                                Function1[
                                                                    S17m,
                                                                    Function1[S18m, Tp],
                                                                ],
                                                            ],
                                                        ],
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
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
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m,
                                        Function1[
                                            S11m,
                                            Function1[
                                                S12m,
                                                Function1[
                                                    S13m,
                                                    Function1[
                                                        S14m,
                                                        Function1[
                                                            S15m,
                                                            Function1[
                                                                S16m,
                                                                Function1[
                                                                    S17m,
                                                                    Function1[
                                                                        S18m,
                                                                        Function1[
                                                                            S19m, Tp
                                                                        ],
                                                                    ],
                                                                ],
                                                            ],
                                                        ],
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
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
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m,
                                        Function1[
                                            S11m,
                                            Function1[
                                                S12m,
                                                Function1[
                                                    S13m,
                                                    Function1[
                                                        S14m,
                                                        Function1[
                                                            S15m,
                                                            Function1[
                                                                S16m,
                                                                Function1[
                                                                    S17m,
                                                                    Function1[
                                                                        S18m,
                                                                        Function1[
                                                                            S19m,
                                                                            Function1[
                                                                                S20m,
                                                                                Tp,
                                                                            ],
                                                                        ],
                                                                    ],
                                                                ],
                                                            ],
                                                        ],
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
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
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m,
                                        Function1[
                                            S11m,
                                            Function1[
                                                S12m,
                                                Function1[
                                                    S13m,
                                                    Function1[
                                                        S14m,
                                                        Function1[
                                                            S15m,
                                                            Function1[
                                                                S16m,
                                                                Function1[
                                                                    S17m,
                                                                    Function1[
                                                                        S18m,
                                                                        Function1[
                                                                            S19m,
                                                                            Function1[
                                                                                S20m,
                                                                                Function1[
                                                                                    S21m,
                                                                                    Tp,
                                                                                ],
                                                                            ],
                                                                        ],
                                                                    ],
                                                                ],
                                                            ],
                                                        ],
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


@overload
def curry(
    function: Callable[
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
) -> Function1[
    S1m,
    Function1[
        S2m,
        Function1[
            S3m,
            Function1[
                S4m,
                Function1[
                    S5m,
                    Function1[
                        S6m,
                        Function1[
                            S7m,
                            Function1[
                                S8m,
                                Function1[
                                    S9m,
                                    Function1[
                                        S10m,
                                        Function1[
                                            S11m,
                                            Function1[
                                                S12m,
                                                Function1[
                                                    S13m,
                                                    Function1[
                                                        S14m,
                                                        Function1[
                                                            S15m,
                                                            Function1[
                                                                S16m,
                                                                Function1[
                                                                    S17m,
                                                                    Function1[
                                                                        S18m,
                                                                        Function1[
                                                                            S19m,
                                                                            Function1[
                                                                                S20m,
                                                                                Function1[
                                                                                    S21m,
                                                                                    Function1[
                                                                                        S22m,
                                                                                        Tp,
                                                                                    ],
                                                                                ],
                                                                            ],
                                                                        ],
                                                                    ],
                                                                ],
                                                            ],
                                                        ],
                                                    ],
                                                ],
                                            ],
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]:
    ...


def _total_application(function: Callable[..., Tp], arguments: dict[str, Any]) -> Tp:
    defaults_applied_arguments = processor.apply_defaults(
        arguments=arguments, function=function
    )
    partial_range = partial_application_scope(
        arguments=defaults_applied_arguments, function=function
    )
    position_parameter = tuple(arguments.values())[:partial_range]
    return function(*position_parameter, **{})


def partial_application_scope(
    *, arguments: processor.Arguments, function: Callable[..., Any]
) -> int:
    """Scope of Partially applicable.

    - Position only no default arguments.
    - Position or keyword no default arguments.
    """
    defaults_size = 0 if function.__defaults__ is None else len(function.__defaults__)
    kwdefaults_size = (
        +0 if function.__kwdefaults__ is None else len(function.__kwdefaults__)
    )
    return len(arguments) - (defaults_size + kwdefaults_size)


def next_partial_position(position: int, /) -> int:
    return position + 1


def curry(func: Callable[P, Tp], /):
    """currying

    - Only positional arguments are supported.
    - No support for keyword-only arguments.
    - Default arguments are not subject to currying.
    """
    initial_arguments = deepcopy(inspect.signature(func).parameters.copy())
    if partial_application_scope(arguments=initial_arguments, function=func) < 2:
        raise TypeError(
            "Signatures that cannot be broken down into partial applications.",
            func,
            initial_arguments,
        )
    if LIMIT_NUMBER_OF_TYPE_VARIABLES < partial_application_scope(
        arguments=initial_arguments, function=func
    ):
        raise TypeError(
            "The number of Type variables that can be parsed by the signature has exceeded the limit.",
            func,
            initial_arguments,
        )

    @wraps(func)
    def closure(
        *,
        function: Callable[P, Tp],
        arguments: processor.Arguments,
        position: int,
    ):
        def partial_application(value: Optional[Any] = None, /):
            key = list(arguments)[position]
            partial_applied_arguments = deepcopy(arguments)
            partial_applied_arguments[key] = value
            if (
                position
                < partial_application_scope(
                    arguments=partial_applied_arguments, function=function
                )
                - LAST_ONE
            ):
                return closure(
                    function=function,
                    arguments=partial_applied_arguments,
                    position=next_partial_position(position),
                )
            else:
                return _total_application(
                    function=function, arguments=partial_applied_arguments
                )

        return Function1(partial_application)

    return closure(
        function=func,
        arguments=initial_arguments,
        position=0,
    )
