import inspect
from functools import wraps
from typing import (
    Callable,
    Optional,
    ParamSpec,
    Type,
    TypeVar,
    overload,
)

T = TypeVar("T")
Implicit = Optional[T]

IMPLICIT_PARAMETER_PREFIX = "__implicit_parameter_"
ONE_STEP_CALL_BACK: int = 1


def parameter(type_: Type[T], /, *, depth: int = 1) -> Optional[T]:
    """

    of the specified type Look for implicit parameters.
    """
    variables = inspect.getargvalues(
        inspect.stack()[depth + ONE_STEP_CALL_BACK].frame
    ).locals
    try:
        return next(
            value
            for key, value in variables.items()
            if key.startswith(IMPLICIT_PARAMETER_PREFIX) and isinstance(value, type_)
        )
    except StopIteration:
        ...
    try:
        return next(value for value in variables.values() if isinstance(value, type_))
    except StopIteration:
        return None


def find_parameter(
    *, implicit_parameter: Implicit[T], target: Type[T], depth: int = 1
) -> Optional[T]:
    """

    Find implicit parameters for optional variables.
    """
    if isinstance(implicit_parameter, target):
        return implicit_parameter
    elif (
        found_parameter := parameter(target, depth=depth + ONE_STEP_CALL_BACK)
    ) is None:
        return None
    else:
        return found_parameter


P = ParamSpec("P")
EP = ParamSpec("EP")
ET1 = TypeVar("ET1")
ET2 = TypeVar("ET2")
ET3 = TypeVar("ET3")
ET4 = TypeVar("ET4")
ET5 = TypeVar("ET5")
ET6 = TypeVar("ET6")
ET7 = TypeVar("ET7")
ET8 = TypeVar("ET8")
ET9 = TypeVar("ET9")
ET10 = TypeVar("ET10")
ET11 = TypeVar("ET11")
ET12 = TypeVar("ET12")
ET13 = TypeVar("ET13")
ET14 = TypeVar("ET14")
ET15 = TypeVar("ET15")


@overload
def explicit_hold(
    arg1: Type[ET1],
    /,
) -> Callable[[Callable[P, T]], Callable[P, Callable[[ET1], T]]]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    /,
) -> Callable[[Callable[P, T]], Callable[P, Callable[[ET1, ET2], T]]]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    /,
) -> Callable[[Callable[P, T]], Callable[P, Callable[[ET1, ET2, ET3], T]]]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    /,
) -> Callable[[Callable[P, T]], Callable[P, Callable[[ET1, ET2, ET3, ET4], T]]]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    /,
) -> Callable[[Callable[P, T]], Callable[P, Callable[[ET1, ET2, ET3, ET4, ET5], T]]]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    arg6: Type[ET6],
    /,
) -> Callable[
    [Callable[P, T]], Callable[P, Callable[[ET1, ET2, ET3, ET4, ET5, ET6], T]]
]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    arg6: Type[ET6],
    arg7: Type[ET7],
    /,
) -> Callable[
    [Callable[P, T]], Callable[P, Callable[[ET1, ET2, ET3, ET4, ET5, ET6, ET7], T]]
]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    arg6: Type[ET6],
    arg7: Type[ET7],
    arg8: Type[ET8],
    /,
) -> Callable[
    [Callable[P, T]], Callable[P, Callable[[ET1, ET2, ET3, ET4, ET5, ET6, ET7, ET8], T]]
]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    arg6: Type[ET6],
    arg7: Type[ET7],
    arg8: Type[ET8],
    arg9: Type[ET9],
    /,
) -> Callable[
    [Callable[P, T]],
    Callable[P, Callable[[ET1, ET2, ET3, ET4, ET5, ET6, ET7, ET8, ET9], T]],
]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    arg6: Type[ET6],
    arg7: Type[ET7],
    arg8: Type[ET8],
    arg9: Type[ET9],
    arg10: Type[ET10],
    /,
) -> Callable[
    [Callable[P, T]],
    Callable[P, Callable[[ET1, ET2, ET3, ET4, ET5, ET6, ET7, ET8, ET9, ET10], T]],
]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    arg6: Type[ET6],
    arg7: Type[ET7],
    arg8: Type[ET8],
    arg9: Type[ET9],
    arg10: Type[ET10],
    arg11: Type[ET11],
    /,
) -> Callable[
    [Callable[P, T]],
    Callable[P, Callable[[ET1, ET2, ET3, ET4, ET5, ET6, ET7, ET8, ET9, ET10, ET11], T]],
]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    arg6: Type[ET6],
    arg7: Type[ET7],
    arg8: Type[ET8],
    arg9: Type[ET9],
    arg10: Type[ET10],
    arg11: Type[ET11],
    arg12: Type[ET12],
    /,
) -> Callable[
    [Callable[P, T]],
    Callable[
        P, Callable[[ET1, ET2, ET3, ET4, ET5, ET6, ET7, ET8, ET9, ET10, ET11, ET12], T]
    ],
]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    arg6: Type[ET6],
    arg7: Type[ET7],
    arg8: Type[ET8],
    arg9: Type[ET9],
    arg10: Type[ET10],
    arg11: Type[ET11],
    arg12: Type[ET12],
    arg13: Type[ET13],
    /,
) -> Callable[
    [Callable[P, T]],
    Callable[
        P,
        Callable[
            [ET1, ET2, ET3, ET4, ET5, ET6, ET7, ET8, ET9, ET10, ET11, ET12, ET13], T
        ],
    ],
]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    arg6: Type[ET6],
    arg7: Type[ET7],
    arg8: Type[ET8],
    arg9: Type[ET9],
    arg10: Type[ET10],
    arg11: Type[ET11],
    arg12: Type[ET12],
    arg13: Type[ET13],
    arg14: Type[ET14],
    /,
) -> Callable[
    [Callable[P, T]],
    Callable[
        P,
        Callable[
            [ET1, ET2, ET3, ET4, ET5, ET6, ET7, ET8, ET9, ET10, ET11, ET12, ET13, ET14],
            T,
        ],
    ],
]:
    ...


@overload
def explicit_hold(
    arg1: Type[ET1],
    arg2: Type[ET2],
    arg3: Type[ET3],
    arg4: Type[ET4],
    arg5: Type[ET5],
    arg6: Type[ET6],
    arg7: Type[ET7],
    arg8: Type[ET8],
    arg9: Type[ET9],
    arg10: Type[ET10],
    arg11: Type[ET11],
    arg12: Type[ET12],
    arg13: Type[ET13],
    arg14: Type[ET14],
    arg15: Type[ET15],
    /,
) -> Callable[
    [Callable[P, T]],
    Callable[
        P,
        Callable[
            [
                ET1,
                ET2,
                ET3,
                ET4,
                ET5,
                ET6,
                ET7,
                ET8,
                ET9,
                ET10,
                ET11,
                ET12,
                ET13,
                ET14,
                ET15,
            ],
            T,
        ],
    ],
]:
    ...


def explicit_hold(*explicit_arg_types: ...):
    """

    Explicitly specify the type of implicit value to be bound to the stack immediately before the
    function.
    """

    def _hold_function(func: Callable[P, T]) -> Callable[P, Callable[EP, T]]:
        @wraps(func)
        def _hold_function_parameters(
            *args: P.args, **kwargs: P.kwargs
        ) -> Callable[EP, T]:
            def _hold_explicit_parameters(
                *explicit_args: ...,
            ) -> T:
                # Binding to implicit parameters in the current stack
                [
                    exec(f"{IMPLICIT_PARAMETER_PREFIX}{count} = explicit_args[{count}]")
                    for count in range(len[explicit_args])
                ]
                return func(*args, **kwargs)

            return _hold_explicit_parameters

        return _hold_function_parameters

    return _hold_function
