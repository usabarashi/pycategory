"""Function"""

from __future__ import annotations

import inspect
from copy import deepcopy
from functools import wraps
from typing import Any, Callable, Optional, cast, overload

from pycategory.runtime import processor

LAST_ONE = 1
# Limit number of Type variables that can be parsed by the signature.
LIMIT_OF_TYPE_VARIABLES = 22


@overload
def curry[
    S1, S2, T
](function: Callable[[S1, S2,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        T,
    ],
]: ...


@overload
def curry[
    S1, S2, S3, T
](function: Callable[[S1, S2, S3,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            T,
        ],
    ],
]: ...


@overload
def curry[
    S1, S2, S3, S4, T
](function: Callable[[S1, S2, S3, S4,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                T,
            ],
        ],
    ],
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, T
](function: Callable[[S1, S2, S3, S4, S5,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    T,
                ],
            ],
        ],
    ],
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, T
](function: Callable[[S1, S2, S3, S4, S5, S6,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        T,
                    ],
                ],
            ],
        ],
    ],
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, T
](function: Callable[[S1, S2, S3, S4, S5, S6, S7,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            T,
                        ],
                    ],
                ],
            ],
        ],
    ],
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, T
](function: Callable[[S1, S2, S3, S4, S5, S6, S7, S8,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                T,
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, T
](function: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    T,
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, T
](function: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        T,
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, T
](function: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            T,
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
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, T
](function: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12,], T,], /,) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                T,
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
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, T
](
    function: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
        ],
        T,
    ],
    /,
) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                Callable[
                                                    [S13],
                                                    T,
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
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, T
](
    function: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
        ],
        T,
    ],
    /,
) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                Callable[
                                                    [S13],
                                                    Callable[
                                                        [S14],
                                                        T,
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
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, T
](
    function: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
        ],
        T,
    ],
    /,
) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                Callable[
                                                    [S13],
                                                    Callable[
                                                        [S14],
                                                        Callable[
                                                            [S15],
                                                            T,
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
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, T
](
    function: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
        ],
        T,
    ],
    /,
) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                Callable[
                                                    [S13],
                                                    Callable[
                                                        [S14],
                                                        Callable[
                                                            [S15],
                                                            Callable[
                                                                [S16],
                                                                T,
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
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, T
](
    function: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
        ],
        T,
    ],
    /,
) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                Callable[
                                                    [S13],
                                                    Callable[
                                                        [S14],
                                                        Callable[
                                                            [S15],
                                                            Callable[
                                                                [S16],
                                                                Callable[
                                                                    [S17],
                                                                    T,
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
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, T
](
    function: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
            S18,
        ],
        T,
    ],
    /,
) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                Callable[
                                                    [S13],
                                                    Callable[
                                                        [S14],
                                                        Callable[
                                                            [S15],
                                                            Callable[
                                                                [S16],
                                                                Callable[
                                                                    [S17],
                                                                    Callable[
                                                                        [S18],
                                                                        T,
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
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, T
](
    function: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
            S18,
            S19,
        ],
        T,
    ],
    /,
) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                Callable[
                                                    [S13],
                                                    Callable[
                                                        [S14],
                                                        Callable[
                                                            [S15],
                                                            Callable[
                                                                [S16],
                                                                Callable[
                                                                    [S17],
                                                                    Callable[
                                                                        [S18],
                                                                        Callable[
                                                                            [S19],
                                                                            T,
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
]: ...


@overload
def curry[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, S20, T
](
    function: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
            S18,
            S19,
            S20,
        ],
        T,
    ],
    /,
) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                Callable[
                                                    [S13],
                                                    Callable[
                                                        [S14],
                                                        Callable[
                                                            [S15],
                                                            Callable[
                                                                [S16],
                                                                Callable[
                                                                    [S17],
                                                                    Callable[
                                                                        [S18],
                                                                        Callable[
                                                                            [S19],
                                                                            Callable[
                                                                                [S20],
                                                                                T,
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
]: ...


@overload
def curry[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    S20,
    S21,
    T,
](
    function: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
            S18,
            S19,
            S20,
            S21,
        ],
        T,
    ],
    /,
) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                Callable[
                                                    [S13],
                                                    Callable[
                                                        [S14],
                                                        Callable[
                                                            [S15],
                                                            Callable[
                                                                [S16],
                                                                Callable[
                                                                    [S17],
                                                                    Callable[
                                                                        [S18],
                                                                        Callable[
                                                                            [S19],
                                                                            Callable[
                                                                                [S20],
                                                                                Callable[
                                                                                    [S21],
                                                                                    T,
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
]: ...


@overload
def curry[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    S20,
    S21,
    S22,
    T,
](
    function: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
            S18,
            S19,
            S20,
            S21,
            S22,
        ],
        T,
    ],
    /,
) -> Callable[
    [S1],
    Callable[
        [S2],
        Callable[
            [S3],
            Callable[
                [S4],
                Callable[
                    [S5],
                    Callable[
                        [S6],
                        Callable[
                            [S7],
                            Callable[
                                [S8],
                                Callable[
                                    [S9],
                                    Callable[
                                        [S10],
                                        Callable[
                                            [S11],
                                            Callable[
                                                [S12],
                                                Callable[
                                                    [S13],
                                                    Callable[
                                                        [S14],
                                                        Callable[
                                                            [S15],
                                                            Callable[
                                                                [S16],
                                                                Callable[
                                                                    [S17],
                                                                    Callable[
                                                                        [S18],
                                                                        Callable[
                                                                            [S19],
                                                                            Callable[
                                                                                [S20],
                                                                                Callable[
                                                                                    [S21],
                                                                                    Callable[
                                                                                        [S22],
                                                                                        T,
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
]: ...


def _has_not_supported_signature_by_culling(func: Callable[..., Any], /) -> bool:
    """Availability of signatures not supported by culling

    - Exclude default arguments
    - Exclude the keyword only argument
    """
    unsupported_signatures_size = len(
        {
            name: param
            for name, param in inspect.signature(func).parameters.items()
            if param.default is not inspect.Parameter.empty or param.kind is param.KEYWORD_ONLY
        }
    )
    return 0 < unsupported_signatures_size


def _is_not_necessary_for_currying(func: Callable[..., Any]) -> bool:
    """Whether or not the argument needs to be broken down."""
    supported_signatures_size = len(
        {
            name: param
            for name, param in inspect.signature(func).parameters.items()
            if param.default is inspect.Parameter.empty or param.kind is not param.KEYWORD_ONLY
        }
    )
    return supported_signatures_size < 2


def _has_over_type_parameters(func: Callable[..., Any], limit: int, /) -> bool:
    """Type parameters not supported by type inference are excluded."""
    supported_signatures_size = len(
        {
            name: param
            for name, param in inspect.signature(func).parameters.items()
            if param.default is not inspect.Parameter.empty or param.kind is param.KEYWORD_ONLY
        }
    )
    return limit < supported_signatures_size


def _apply_scope(arguments: processor.Arguments, func: Callable[..., Any]) -> int:
    defaults_size = 0 if func.__defaults__ is None else len(func.__defaults__)
    kwdefaults_size = (
        +0
        if cast(Optional[dict[str, Any]], func.__kwdefaults__) is None
        else len(func.__kwdefaults__)
    )
    return len(arguments) - (defaults_size + kwdefaults_size)


def _next(position: int, /) -> int:
    return position + 1


def curry[**P, A](func: Callable[P, A], /):  # type: ignore
    """Currying a function

    - Position only no default arguments.
    """
    if _has_not_supported_signature_by_culling(func):
        raise TypeError(
            "Signatures that cannot be broken down into partial applications.",
            inspect.getsource(func),
        )
    if _is_not_necessary_for_currying(func):
        raise TypeError("Signatures that do not require currying.", inspect.getsource(func))
    if _has_over_type_parameters(func, LIMIT_OF_TYPE_VARIABLES):
        raise TypeError(
            f"Type parameter exceeds the upper limit of {LIMIT_OF_TYPE_VARIABLES}.",
            inspect.getsource(func),
        )

    @wraps(func)
    def _partial(func: Callable[P, A], arguments_state: processor.Arguments, position: int):

        def _apply(value: Optional[Any] = None, /):
            name = list(arguments_state)[position]
            applied_arguments = deepcopy(arguments_state)
            applied_arguments[name] = value
            if position < _apply_scope(applied_arguments, func) - LAST_ONE:
                return _partial(func, applied_arguments, _next(position))
            else:
                return _complete(func, applied_arguments)

        return _apply

    def _complete(func: Callable[P, A], arguments_state: processor.Arguments) -> A:
        defaults_applied_arguments = processor.apply_defaults(arguments_state, func)
        position_range = _apply_scope(arguments=defaults_applied_arguments, func=func)
        position_parameter = tuple(arguments_state.values())[:position_range]
        return func(*position_parameter, **{})  # type: ignore

    initial_signature = deepcopy(inspect.signature(func).parameters.copy())
    return _partial(func, initial_signature, 0)


class Function: ...


class Function1[S1, A](Function):
    def __init__(self, func: Callable[[S1], A], /):
        if not callable(func):
            raise TypeError(func)
        self._func = func

    def __call__(self, arg: S1, /) -> A:
        return self._func(arg)

    apply = __call__

    def compose[B](self, other: Callable[[B], S1] | Function1[B, S1]) -> Function1[B, A]:
        return Function1[B, A](lambda arg: self(other(arg)))

    def and_then[B](self, other: Callable[[A], B] | Function1[A, B]) -> Function1[S1, B]:
        return Function1[S1, B](lambda arg: other(self(arg)))


class FunctionN(Function): ...


class Function2[S1, S2, A](FunctionN):
    def __init__(self, func: Callable[[S1, S2], A], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1, arg2: S2) -> A:
        return self._func(arg1, arg2)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1, S2], /) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function3[S1, S2, S3, A](FunctionN):
    def __init__(self, func: Callable[[S1, S2, S3], A], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1, arg2: S2, arg3: S3) -> A:
        return self._func(arg1, arg2, arg3)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1, S2, S3], /) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function4[S1, S2, S3, S4, A](FunctionN):
    def __init__(self, func: Callable[[S1, S2, S3, S4], A], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1, arg2: S2, arg3: S3, arg4: S4) -> A:
        return self._func(arg1, arg2, arg3, arg4)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1, S2, S3, S4], /) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function5[S1, S2, S3, S4, S5, A](FunctionN):
    def __init__(self, func: Callable[[S1, S2, S3, S4, S5], A], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1, arg2: S2, arg3: S3, arg4: S4, arg5: S5) -> A:
        return self._func(arg1, arg2, arg3, arg4, arg5)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1, S2, S3, S4, S5], /) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function6[S1, S2, S3, S4, S5, S6, A](FunctionN):
    def __init__(self, func: Callable[[S1, S2, S3, S4, S5, S6], A], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(self, /, arg1: S1, arg2: S2, arg3: S3, arg4: S4, arg5: S5, arg6: S6) -> A:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1, S2, S3, S4, S5, S6], /) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function7[S1, S2, S3, S4, S5, S6, S7, A](FunctionN):
    def __init__(self, func: Callable[[S1, S2, S3, S4, S5, S6, S7], A], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
    ) -> A:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6, arg7)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1, S2, S3, S4, S5, S6, S7], /) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function8[S1, S2, S3, S4, S5, S6, S7, S8, A](FunctionN):
    def __init__(self, func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8], A], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
    ) -> A:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1, S2, S3, S4, S5, S6, S7, S8], /) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function9[S1, S2, S3, S4, S5, S6, S7, S8, S9, A](FunctionN):
    def __init__(self, func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9], A], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
    ) -> A:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1, S2, S3, S4, S5, S6, S7, S8, S9], /) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function10[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, A](FunctionN):
    def __init__(self, func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10], A], /):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
    ) -> A:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10], /) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function11[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, A](FunctionN):
    def __init__(
        self,
        func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11], A],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
    ) -> A:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(args: tuple[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11], /) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function12[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, A](FunctionN):
    def __init__(
        self,
        func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12], A],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
    ) -> A:
        return self._func(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12)

    @property
    def apply(self):
        return self.__call__

    @property
    def curried(self):
        return curry(self._func)

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function13[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, A](FunctionN):
    def __init__(
        self,
        func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13], A],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
        arg13: S13,
    ) -> A:
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
    def curried(self):  # type: ignore # Type inference
        return curry(self._func)  # type: ignore # Type inference

    @property
    def tupled(self):
        def tupled_arg_function(
            args: tuple[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function14[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, A](FunctionN):
    def __init__(
        self,
        func: Callable[
            [S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14],
            A,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
        arg13: S13,
        arg14: S14,
    ) -> A:
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
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
            ],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function15[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    A,
](FunctionN):
    def __init__(
        self,
        func: Callable[
            [
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
            ],
            A,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
        arg13: S13,
        arg14: S14,
        arg15: S15,
    ) -> A:
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
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
            ],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function16[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    A,
](FunctionN):
    def __init__(
        self,
        func: Callable[
            [
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
            ],
            A,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
        arg13: S13,
        arg14: S14,
        arg15: S15,
        arg16: S16,
    ) -> A:
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
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
            ],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function17[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    A,
](FunctionN):
    def __init__(
        self,
        func: Callable[
            [
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
            ],
            A,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
        arg13: S13,
        arg14: S14,
        arg15: S15,
        arg16: S16,
        arg17: S17,
    ) -> A:
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
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
            ],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function18[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, A
](FunctionN):
    def __init__(
        self,
        func: Callable[
            [
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
                S18,
            ],
            A,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
        arg13: S13,
        arg14: S14,
        arg15: S15,
        arg16: S16,
        arg17: S17,
        arg18: S18,
    ) -> A:
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
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
                S18,
            ],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function19[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    A,
](FunctionN):
    def __init__(
        self,
        func: Callable[
            [
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
                S18,
                S19,
            ],
            A,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
        arg13: S13,
        arg14: S14,
        arg15: S15,
        arg16: S16,
        arg17: S17,
        arg18: S18,
        arg19: S19,
    ) -> A:
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
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
                S18,
                S19,
            ],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function20[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    S20,
    A,
](FunctionN):
    def __init__(
        self,
        func: Callable[
            [
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
                S18,
                S19,
                S20,
            ],
            A,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
        arg13: S13,
        arg14: S14,
        arg15: S15,
        arg16: S16,
        arg17: S17,
        arg18: S18,
        arg19: S19,
        arg20: S20,
    ) -> A:
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
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
                S18,
                S19,
                S20,
            ],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function21[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    S20,
    S21,
    A,
](FunctionN):
    def __init__(
        self,
        func: Callable[
            [
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
                S18,
                S19,
                S20,
                S21,
            ],
            A,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
        arg13: S13,
        arg14: S14,
        arg15: S15,
        arg16: S16,
        arg17: S17,
        arg18: S18,
        arg19: S19,
        arg20: S20,
        arg21: S21,
    ) -> A:
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
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
                S18,
                S19,
                S20,
                S21,
            ],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


class Function22[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    S20,
    S21,
    S22,
    A,
](FunctionN):
    def __init__(
        self,
        func: Callable[
            [
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
                S18,
                S19,
                S20,
                S21,
                S22,
            ],
            A,
        ],
        /,
    ):
        if not callable(func):
            raise TypeError
        self._func = func

    def __call__(
        self,
        /,
        arg1: S1,
        arg2: S2,
        arg3: S3,
        arg4: S4,
        arg5: S5,
        arg6: S6,
        arg7: S7,
        arg8: S8,
        arg9: S9,
        arg10: S10,
        arg11: S11,
        arg12: S12,
        arg13: S13,
        arg14: S14,
        arg15: S15,
        arg16: S16,
        arg17: S17,
        arg18: S18,
        arg19: S19,
        arg20: S20,
        arg21: S21,
        arg22: S22,
    ) -> A:
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
                S1,
                S2,
                S3,
                S4,
                S5,
                S6,
                S7,
                S8,
                S9,
                S10,
                S11,
                S12,
                S13,
                S14,
                S15,
                S16,
                S17,
                S18,
                S19,
                S20,
                S21,
                S22,
            ],
            /,
        ) -> A:
            return self._func(*args)

        return tupled_arg_function


@overload
def extend[S1, A](func: Callable[[S1], A], /) -> Function1[S1, A]: ...


@overload
def extend[S1, S2, A](func: Callable[[S1, S2], A], /) -> Function2[S1, S2, A]: ...


@overload
def extend[S1, S2, S3, A](func: Callable[[S1, S2, S3], A], /) -> Function3[S1, S2, S3, A]: ...


@overload
def extend[
    S1, S2, S3, S4, A
](func: Callable[[S1, S2, S3, S4], A], /) -> Function4[S1, S2, S3, S4, A]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, A
](func: Callable[[S1, S2, S3, S4, S5], A], /) -> Function5[S1, S2, S3, S4, S5, A]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, A
](func: Callable[[S1, S2, S3, S4, S5, S6], A], /) -> Function6[S1, S2, S3, S4, S5, S6, A]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, A
](func: Callable[[S1, S2, S3, S4, S5, S6, S7], A], /) -> Function7[
    S1, S2, S3, S4, S5, S6, S7, A
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, A
](func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8], A], /) -> Function8[
    S1, S2, S3, S4, S5, S6, S7, S8, A
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, A
](func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9], A], /) -> Function9[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, A
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, A
](func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10], A], /) -> Function10[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, A
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, A
](func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11], A], /) -> Function11[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, A
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, A
](
    func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12], A],
    /,
) -> Function12[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, A
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, A
](
    func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13], A],
    /,
) -> Function13[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, A
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, A
](
    func: Callable[[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14], A],
    /,
) -> Function14[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, A]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, A
](
    func: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
        ],
        A,
    ],
    /,
) -> Function15[S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, A]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, A
](
    func: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
        ],
        A,
    ],
    /,
) -> Function16[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    A,
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, A
](
    func: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
        ],
        A,
    ],
    /,
) -> Function17[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    A,
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, A
](
    func: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
            S18,
        ],
        A,
    ],
    /,
) -> Function18[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    A,
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, A
](
    func: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
            S18,
            S19,
        ],
        A,
    ],
    /,
) -> Function19[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    A,
]: ...


@overload
def extend[
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, S20, A
](
    func: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
            S18,
            S19,
            S20,
        ],
        A,
    ],
    /,
) -> Function20[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    S20,
    A,
]: ...


@overload
def extend[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    S20,
    S21,
    A,
](
    func: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
            S18,
            S19,
            S20,
            S21,
        ],
        A,
    ],
    /,
) -> Function21[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    S20,
    S21,
    A,
]: ...


@overload
def extend[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    S20,
    S21,
    S22,
    A,
](
    func: Callable[
        [
            S1,
            S2,
            S3,
            S4,
            S5,
            S6,
            S7,
            S8,
            S9,
            S10,
            S11,
            S12,
            S13,
            S14,
            S15,
            S16,
            S17,
            S18,
            S19,
            S20,
            S21,
            S22,
        ],
        A,
    ],
    /,
) -> Function22[
    S1,
    S2,
    S3,
    S4,
    S5,
    S6,
    S7,
    S8,
    S9,
    S10,
    S11,
    S12,
    S13,
    S14,
    S15,
    S16,
    S17,
    S18,
    S19,
    S20,
    S21,
    S22,
    A,
]: ...


def extend(func: Callable[..., Any], /):  # type: ignore # Type inference
    """Applying Extended Methods to Functions."""
    arguments = inspect.signature(func).parameters.copy()
    match _apply_scope(arguments, func):
        case 0:
            raise TypeError(inspect.getsource(func))
        case 1:
            return Function1(func)  # type: ignore
        case 2:
            return Function2(func)  # type: ignore
        case 3:
            return Function3(func)  # type: ignore
        case 4:
            return Function4(func)  # type: ignore
        case 5:
            return Function5(func)  # type: ignore
        case 6:
            return Function6(func)  # type: ignore
        case 7:
            return Function7(func)  # type: ignore
        case 8:
            return Function8(func)  # type: ignore
        case 9:
            return Function9(func)  # type: ignore
        case 10:
            return Function10(func)  # type: ignore
        case 11:
            return Function11(func)  # type: ignore
        case 12:
            return Function12(func)  # type: ignore
        case 13:
            return Function13(func)  # type: ignore
        case 14:
            return Function14(func)  # type: ignore
        case 15:
            return Function15(func)  # type: ignore
        case 16:
            return Function16(func)  # type: ignore
        case 17:
            return Function17(func)  # type: ignore
        case 18:
            return Function18(func)  # type: ignore
        case 19:
            return Function19(func)  # type: ignore
        case 20:
            return Function20(func)  # type: ignore
        case 21:
            return Function21(func)  # type: ignore
        case 22:
            return Function22(func)  # type: ignore
        case _:
            raise TypeError(
                f"Type parameter exceeds the upper limit of {LIMIT_OF_TYPE_VARIABLES}.",
                inspect.getsource(func),
            )
