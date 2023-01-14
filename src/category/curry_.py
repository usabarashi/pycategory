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
    overload,
)

from . import processor

P = ParamSpec("P")
T = TypeVar("T")
S1m = TypeVar("S1m")
S2m = TypeVar("S2m")
S3m = TypeVar("S3m")
S4m = TypeVar("S4m")
S5m = TypeVar("S5m")
S6m = TypeVar("S6m")
S7m = TypeVar("S7m")
S8m = TypeVar("S8m")
S9m = TypeVar("S9m")
S10m = TypeVar("S10m")
S11m = TypeVar("S11m")
S12m = TypeVar("S12m")
S13m = TypeVar("S13m")
S14m = TypeVar("S14m")
S15m = TypeVar("S15m")
S16m = TypeVar("S16m")
S17m = TypeVar("S17m")
S18m = TypeVar("S18m")
S19m = TypeVar("S19m")
S20m = TypeVar("S20m")
S21m = TypeVar("S21m")
S22m = TypeVar("S22m")

CURRY2: TypeAlias = Callable[[S1m], Callable[[S2m], T]]
CURRY3: TypeAlias = Callable[[S1m], CURRY2[S2m, S3m, T]]
CURRY4: TypeAlias = Callable[[S1m], CURRY3[S2m, S3m, S4m, T]]
CURRY5: TypeAlias = Callable[[S1m], CURRY4[S2m, S3m, S4m, S5m, T]]
CURRY6: TypeAlias = Callable[[S1m], CURRY5[S2m, S3m, S4m, S5m, S6m, T]]
CURRY7: TypeAlias = Callable[[S1m], CURRY6[S2m, S3m, S4m, S5m, S6m, S7m, T]]
CURRY8: TypeAlias = Callable[[S1m], CURRY7[S2m, S3m, S4m, S5m, S6m, S7m, S8m, T]]
CURRY9: TypeAlias = Callable[[S1m], CURRY8[S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, T]]
CURRY10: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[[S9m], Callable[[S10m], T]],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]
CURRY11: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[[S9m], Callable[[S10m], Callable[[S11m], T]]],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
]
CURRY12: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m], Callable[[S11m], Callable[[S12m], T]]
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
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m],
                                        Callable[
                                            [S11m],
                                            Callable[[S12m], Callable[[S13m], T]],
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
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m],
                                        Callable[
                                            [S11m],
                                            Callable[
                                                [S12m],
                                                Callable[[S13m], Callable[[S14m], T]],
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
CURRY15: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m],
                                        Callable[
                                            [S11m],
                                            Callable[
                                                [S12m],
                                                Callable[
                                                    [S13m],
                                                    Callable[
                                                        [S14m], Callable[[S15m], T]
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
]
CURRY16: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m],
                                        Callable[
                                            [S11m],
                                            Callable[
                                                [S12m],
                                                Callable[
                                                    [S13m],
                                                    Callable[
                                                        [S14m],
                                                        Callable[
                                                            [S15m], Callable[[S16m], T]
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
]
CURRY17: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m],
                                        Callable[
                                            [S11m],
                                            Callable[
                                                [S12m],
                                                Callable[
                                                    [S13m],
                                                    Callable[
                                                        [S14m],
                                                        Callable[
                                                            [S15m],
                                                            Callable[
                                                                [S16m],
                                                                Callable[[S17m], T],
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
]
CURRY18: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m],
                                        Callable[
                                            [S11m],
                                            Callable[
                                                [S12m],
                                                Callable[
                                                    [S13m],
                                                    Callable[
                                                        [S14m],
                                                        Callable[
                                                            [S15m],
                                                            Callable[
                                                                [S16m],
                                                                Callable[
                                                                    [S17m],
                                                                    Callable[[S18m], T],
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
]
CURRY19: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m],
                                        Callable[
                                            [S11m],
                                            Callable[
                                                [S12m],
                                                Callable[
                                                    [S13m],
                                                    Callable[
                                                        [S14m],
                                                        Callable[
                                                            [S15m],
                                                            Callable[
                                                                [S16m],
                                                                Callable[
                                                                    [S17m],
                                                                    Callable[
                                                                        [S18m],
                                                                        Callable[
                                                                            [S19m], T
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
]
CURRY20: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m],
                                        Callable[
                                            [S11m],
                                            Callable[
                                                [S12m],
                                                Callable[
                                                    [S13m],
                                                    Callable[
                                                        [S14m],
                                                        Callable[
                                                            [S15m],
                                                            Callable[
                                                                [S16m],
                                                                Callable[
                                                                    [S17m],
                                                                    Callable[
                                                                        [S18m],
                                                                        Callable[
                                                                            [S19m],
                                                                            Callable[
                                                                                [S20m],
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
]
CURRY21: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m],
                                        Callable[
                                            [S11m],
                                            Callable[
                                                [S12m],
                                                Callable[
                                                    [S13m],
                                                    Callable[
                                                        [S14m],
                                                        Callable[
                                                            [S15m],
                                                            Callable[
                                                                [S16m],
                                                                Callable[
                                                                    [S17m],
                                                                    Callable[
                                                                        [S18m],
                                                                        Callable[
                                                                            [S19m],
                                                                            Callable[
                                                                                [S20m],
                                                                                Callable[
                                                                                    [
                                                                                        S21m
                                                                                    ],
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
]
CURRY22: TypeAlias = Callable[
    [S1m],
    Callable[
        [S2m],
        Callable[
            [S3m],
            Callable[
                [S4m],
                Callable[
                    [S5m],
                    Callable[
                        [S6m],
                        Callable[
                            [S7m],
                            Callable[
                                [S8m],
                                Callable[
                                    [S9m],
                                    Callable[
                                        [S10m],
                                        Callable[
                                            [S11m],
                                            Callable[
                                                [S12m],
                                                Callable[
                                                    [S13m],
                                                    Callable[
                                                        [S14m],
                                                        Callable[
                                                            [S15m],
                                                            Callable[
                                                                [S16m],
                                                                Callable[
                                                                    [S17m],
                                                                    Callable[
                                                                        [S18m],
                                                                        Callable[
                                                                            [S19m],
                                                                            Callable[
                                                                                [S20m],
                                                                                Callable[
                                                                                    [
                                                                                        S21m
                                                                                    ],
                                                                                    Callable[
                                                                                        [
                                                                                            S22m
                                                                                        ],
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
]


@overload
def curry(function: Callable[[S1m, S2m], T], /) -> CURRY2[S1m, S2m, T]:
    ...


@overload
def curry(function: Callable[[S1m, S2m, S3m], T], /) -> CURRY3[S1m, S2m, S3m, T]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m], T], /
) -> CURRY4[S1m, S2m, S3m, S4m, T]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m], T], /
) -> CURRY5[S1m, S2m, S3m, S4m, S5m, T]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m], T], /
) -> CURRY6[S1m, S2m, S3m, S4m, S5m, S6m, T]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m], T], /
) -> CURRY7[S1m, S2m, S3m, S4m, S5m, S6m, S7m, T]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m], T], /
) -> CURRY8[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, T]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m], T], /
) -> CURRY9[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, T]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m], T],
    /,
) -> CURRY10[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, T]:
    ...


@overload
def curry(
    function: Callable[[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m], T],
    /,
) -> CURRY11[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, T]:
    ...


@overload
def curry(
    function: Callable[
        [S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m], T
    ],
    /,
) -> CURRY12[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, T]:
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
) -> CURRY13[S1m, S2m, S3m, S4m, S5m, S6m, S7m, S8m, S9m, S10m, S11m, S12m, S13m, T]:
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
        T,
    ],
    /,
) -> CURRY14[
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
    T,
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
        T,
    ],
    /,
) -> CURRY15[
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
    T,
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
        T,
    ],
    /,
) -> CURRY16[
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
    T,
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
        T,
    ],
    /,
) -> CURRY17[
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
    T,
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
        T,
    ],
    /,
) -> CURRY18[
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
    T,
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
        T,
    ],
    /,
) -> CURRY19[
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
    T,
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
        T,
    ],
    /,
) -> CURRY20[
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
    T,
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
        T,
    ],
    /,
) -> CURRY21[
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
    T,
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
        T,
    ],
    /,
) -> CURRY22[
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
    22  # Limit number of Type variables that can be parsed by the signature.
)


def curry(function: Callable[P, T], /):
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
