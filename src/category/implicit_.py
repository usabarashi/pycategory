from __future__ import annotations

import inspect
from collections.abc import Callable, Generator
from typing import Any, Generic, Optional, ParamSpec, Type, TypeVar, TypeVarTuple

T1 = TypeVar("T1")
T2 = TypeVar("T2")
Fm = TypeVar("Fm", bound=Callable, contravariant=True)
Sm = TypeVar("Sm", contravariant=True)
Ss = TypeVarTuple("Ss")
Tp = TypeVar("Tp", covariant=True)
P = ParamSpec("P")


PARAMETER_PREFIX = "_implicit_"
ONE_STEP_CALL_BACK: int = 1


class CannotFindImplicitParameter(Exception):
    """

    Cannot find an implicit parameter.
    You may need to provide the _implicit_PARAMEMETER: TYPE variable in the caller.
    """

    ...


def all_implicit_parameters(depth: int = 1) -> Generator[Any, None, None]:
    variables = inspect.getargvalues(
        inspect.stack()[depth + ONE_STEP_CALL_BACK].frame
    ).locals
    return (
        value for key, value in variables.items() if key.startswith(PARAMETER_PREFIX)
    )


def parameter(type_: Type[Sm], /, *, depth: int = 1) -> Optional[Sm]:
    """

    Look of the specified type Look for implicit parameters.
    """
    if type_ is None:
        return None
    try:
        return next(
            filter(
                lambda value: isinstance(value, type_),
                all_implicit_parameters(depth + ONE_STEP_CALL_BACK),
            )
        )
    except StopIteration:
        return None


def find_parameter(
    *, param: Optional[Tp], target: Type[Tp], depth: int = 1
) -> Optional[Tp]:
    """

    Find implicit parameters for optional variables.
    """
    if target is None:
        return None
    elif isinstance(param, target):
        return param
    elif (found_param := parameter(target, depth=depth + ONE_STEP_CALL_BACK)) is None:
        return None
    else:
        return found_param


class Implicit(Generic[Fm, *Ss]):
    def __init__(self, func: Fm, /):
        if not callable(func):
            raise TypeError
        self._func = func

    @property
    def __call__(self) -> Fm:
        # Binding to implicit parameters in the current stack
        for count, parameter in enumerate(all_implicit_parameters()):
            exec(f"{PARAMETER_PREFIX}{count} = {parameter};")
        return self._func


class implicit(Generic[*Ss]):
    @staticmethod
    def hold(func: Callable[P, Tp]) -> Implicit[Callable[P, Tp], *Ss]:
        return Implicit[Callable[P, Tp], *Ss](func)


class explicit(Generic[*Ss]):
    @staticmethod
    def hold(func: Callable[P, Tp]) -> Callable[P, Callable[[*Ss], Tp]]:
        def _hold_function_parameters(
            *args: P.args, **kwargs: P.kwargs
        ) -> Callable[[*Ss], Tp]:
            def _hold_explicit_parameters(*explicit_args: *Ss) -> Tp:
                # Binding to implicit parameters in the current stack
                for count in range(len(explicit_args)):
                    exec(f"{PARAMETER_PREFIX}{count} = explicit_args[{count}];")
                return func(*args, **kwargs)

            return _hold_explicit_parameters

        return _hold_function_parameters
