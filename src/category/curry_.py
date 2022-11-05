from __future__ import annotations

import inspect
from copy import deepcopy
from functools import wraps
from typing import (
    Any,
    Callable,
    Optional,
    ParamSpec,
    TypeAlias,
    TypeVar,
    Union,
    overload,
)

from . import processor

P = ParamSpec("P")
T = TypeVar("T")
ARG1 = TypeVar("ARG1")
ARG2 = TypeVar("ARG2")
ARG3 = TypeVar("ARG3")
ARG4 = TypeVar("ARG4")
ARG5 = TypeVar("ARG5")
ARG6 = TypeVar("ARG6")
ARG7 = TypeVar("ARG7")
ARG8 = TypeVar("ARG8")
ARG9 = TypeVar("ARG9")
ARG10 = TypeVar("ARG10")
ARG11 = TypeVar("ARG11")
ARG12 = TypeVar("ARG12")
ARG13 = TypeVar("ARG13")
ARG14 = TypeVar("ARG14")

CURRY2: TypeAlias = Callable[[ARG1], Callable[[ARG2], T]]
CURRY3: TypeAlias = Callable[[ARG1], CURRY2[ARG2, ARG3, T]]
CURRY4: TypeAlias = Callable[[ARG1], CURRY3[ARG2, ARG3, ARG4, T]]
CURRY5: TypeAlias = Callable[[ARG1], CURRY4[ARG2, ARG3, ARG4, ARG5, T]]
CURRY6: TypeAlias = Callable[[ARG1], CURRY5[ARG2, ARG3, ARG4, ARG5, ARG6, T]]
CURRY7: TypeAlias = Callable[[ARG1], CURRY6[ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, T]]
CURRY8: TypeAlias = Callable[
    [ARG1], CURRY7[ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, T]
]
CURRY9: TypeAlias = Callable[
    [ARG1], CURRY8[ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, T]
]
CURRY10: TypeAlias = Callable[
    [ARG1],
    Callable[
        [ARG2],
        Callable[
            [ARG3],
            Callable[
                [ARG4],
                Callable[
                    [ARG5],
                    Callable[
                        [ARG6],
                        Callable[
                            [ARG7],
                            Callable[
                                [ARG8],
                                Callable[[ARG9], Callable[[ARG10], T]],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]
CURRY11: TypeAlias = Callable[
    [ARG1],
    Callable[
        [ARG2],
        Callable[
            [ARG3],
            Callable[
                [ARG4],
                Callable[
                    [ARG5],
                    Callable[
                        [ARG6],
                        Callable[
                            [ARG7],
                            Callable[
                                [ARG8],
                                Callable[
                                    [ARG9], Callable[[ARG10], Callable[[ARG11], T]]
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]
CURRY12: TypeAlias = Callable[
    [ARG1],
    Callable[
        [ARG2],
        Callable[
            [ARG3],
            Callable[
                [ARG4],
                Callable[
                    [ARG5],
                    Callable[
                        [ARG6],
                        Callable[
                            [ARG7],
                            Callable[
                                [ARG8],
                                Callable[
                                    [ARG9],
                                    Callable[
                                        [ARG10], Callable[[ARG11], Callable[[ARG12], T]]
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]
CURRY13: TypeAlias = Callable[
    [ARG1],
    Callable[
        [ARG2],
        Callable[
            [ARG3],
            Callable[
                [ARG4],
                Callable[
                    [ARG5],
                    Callable[
                        [ARG6],
                        Callable[
                            [ARG7],
                            Callable[
                                [ARG8],
                                Callable[
                                    [ARG9],
                                    Callable[
                                        [ARG10],
                                        Callable[
                                            [ARG11],
                                            Callable[[ARG12], Callable[[ARG13], T]],
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
]
CURRY14: TypeAlias = Callable[
    [ARG1],
    Callable[
        [ARG2],
        Callable[
            [ARG3],
            Callable[
                [ARG4],
                Callable[
                    [ARG5],
                    Callable[
                        [ARG6],
                        Callable[
                            [ARG7],
                            Callable[
                                [ARG8],
                                Callable[
                                    [ARG9],
                                    Callable[
                                        [ARG10],
                                        Callable[
                                            [ARG11],
                                            Callable[
                                                [ARG12],
                                                Callable[[ARG13], Callable[[ARG14], T]],
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
]


@overload
def curry(function: Callable[[ARG1, ARG2], T], /) -> CURRY2[ARG1, ARG2, T]:
    ...


@overload
def curry(function: Callable[[ARG1, ARG2, ARG3], T], /) -> CURRY3[ARG1, ARG2, ARG3, T]:
    ...


@overload
def curry(
    function: Callable[[ARG1, ARG2, ARG3, ARG4], T], /
) -> CURRY4[ARG1, ARG2, ARG3, ARG4, T]:
    ...


@overload
def curry(
    function: Callable[[ARG1, ARG2, ARG3, ARG4, ARG5], T], /
) -> CURRY5[ARG1, ARG2, ARG3, ARG4, ARG5, T]:
    ...


@overload
def curry(
    function: Callable[[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6], T], /
) -> CURRY6[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, T]:
    ...


@overload
def curry(
    function: Callable[[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7], T], /
) -> CURRY7[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, T]:
    ...


@overload
def curry(
    function: Callable[[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8], T], /
) -> CURRY8[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, T]:
    ...


@overload
def curry(
    function: Callable[[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9], T], /
) -> CURRY9[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, T]:
    ...


@overload
def curry(
    function: Callable[
        [ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10], T
    ],
    /,
) -> CURRY10[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10, T]:
    ...


@overload
def curry(
    function: Callable[
        [ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10, ARG11], T
    ],
    /,
) -> CURRY11[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10, ARG11, T]:
    ...


@overload
def curry(
    function: Callable[
        [ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10, ARG11, ARG12], T
    ],
    /,
) -> CURRY12[
    ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10, ARG11, ARG12, T
]:
    ...


@overload
def curry(
    function: Callable[
        [
            ARG1,
            ARG2,
            ARG3,
            ARG4,
            ARG5,
            ARG6,
            ARG7,
            ARG8,
            ARG9,
            ARG10,
            ARG11,
            ARG12,
            ARG13,
        ],
        T,
    ],
    /,
) -> CURRY13[
    ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10, ARG11, ARG12, ARG13, T
]:
    ...


@overload
def curry(
    function: Callable[
        [
            ARG1,
            ARG2,
            ARG3,
            ARG4,
            ARG5,
            ARG6,
            ARG7,
            ARG8,
            ARG9,
            ARG10,
            ARG11,
            ARG12,
            ARG13,
            ARG14,
        ],
        T,
    ],
    /,
) -> CURRY14[
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    ARG5,
    ARG6,
    ARG7,
    ARG8,
    ARG9,
    ARG10,
    ARG11,
    ARG12,
    ARG13,
    ARG14,
    T,
]:
    ...


def _total_application(function: Callable[..., T], arguments: dict[str, Any]) -> T:
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


LAST_ONE = 1
LIMIT_NUMBER_OF_TYPE_VARIABLES = (
    14  # Limit number of Type variables that can be parsed by the signature.
)


def curry(
    function: Callable[P, T], /
) -> Union[
    CURRY2[ARG1, ARG2, T],
    CURRY3[ARG1, ARG2, ARG3, T],
    CURRY4[ARG1, ARG2, ARG3, ARG4, T],
    CURRY5[ARG1, ARG2, ARG3, ARG4, ARG5, T],
    CURRY6[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, T],
    CURRY7[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, T],
    CURRY8[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, T],
    CURRY9[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, T],
    CURRY10[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10, T],
    CURRY11[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10, ARG11, T],
    CURRY12[
        ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10, ARG11, ARG12, T
    ],
    CURRY13[
        ARG1,
        ARG2,
        ARG3,
        ARG4,
        ARG5,
        ARG6,
        ARG7,
        ARG8,
        ARG9,
        ARG10,
        ARG11,
        ARG12,
        ARG13,
        T,
    ],
    CURRY14[
        ARG1,
        ARG2,
        ARG3,
        ARG4,
        ARG5,
        ARG6,
        ARG7,
        ARG8,
        ARG9,
        ARG10,
        ARG11,
        ARG12,
        ARG13,
        ARG14,
        T,
    ],
]:
    """currying

    - Only positional arguments are supported.
    - No support for keyword-only arguments.
    - Default arguments are not subject to currying.
    """
    initial_arguments = deepcopy(inspect.signature(function).parameters.copy())
    if partial_application_scope(arguments=initial_arguments, function=function) < 2:
        raise TypeError(
            "Signatures that cannot be broken down into partial applications.",
            function,
            initial_arguments,
        )
    if LIMIT_NUMBER_OF_TYPE_VARIABLES < partial_application_scope(
        arguments=initial_arguments, function=function
    ):
        raise TypeError(
            "The number of Type variables that can be parsed by the signature has exceeded the limit.",
            function,
            initial_arguments,
        )

    @wraps(function)
    def closure(
        *,
        function: Callable[P, T],
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

        return partial_application

    return closure(
        function=function,
        arguments=initial_arguments,
        position=0,
    )
