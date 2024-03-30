"""Implicit"""
from __future__ import annotations

import inspect
from typing import Any, Callable, Type

_IMPLICIT = "__implicit__"
_IMPLICIT_FUNCTION = "__implicit_function__"


class ImplicitError(ValueError):
    pass


class Implicit[**P, T, *U]:
    """Function wrapper to apply implicit parameters"""

    def __init__(self, func: Callable[P, T], *implicit_types: *U):
        if len(implicit_types) == 0:
            raise ImplicitError("Expected at least one implicit type.")
        if not all(isinstance(t, type) for t in implicit_types):
            raise ImplicitError("Expected all implicit types to be types.", implicit_types)
        if len(implicit_types) != len(set(implicit_types)):
            raise ImplicitError("Duplicate implicit types found.", implicit_types)

        self._func = func
        self._implicit_types: tuple[Type[Any]] = implicit_types  # type: ignore

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        """Apply implicit parameters and execute the function

        Cannot apply implicit parameters to the same function object in parallel.
        """
        if (current_frame := inspect.currentframe()) is None:
            raise RuntimeError("An unexpected error occurred")
        if (callers_frame := current_frame.f_back) is None:
            raise RuntimeError("An unexpected error occurred")

        current_implicit: dict[Type[Any], Any] = {}
        for implicit_type in self._implicit_types:
            # Local scope case
            if (callers_local := callers_frame.f_locals.get(_IMPLICIT)) is not None:
                if implicit_type in callers_local:
                    current_implicit[implicit_type] = callers_local[implicit_type]
                    continue
            # Global scope case
            if (callers_global := callers_frame.f_globals.get(_IMPLICIT)) is not None:
                if implicit_type in callers_global:
                    current_implicit[implicit_type] = callers_global[implicit_type]
                    continue
            # The Case of Function Object
            if (call_resource_frame := callers_frame.f_back) is None:
                raise ImplicitError(f"Expected {implicit_type} to be given")
            if (callers_func := call_resource_frame.f_locals.get(_IMPLICIT_FUNCTION)) is None:
                raise ImplicitError(f"Expected {implicit_type} to be given")
            if (implicit_parameter := getattr(callers_func, _IMPLICIT, None)) is None:
                raise ImplicitError(f"Expected {implicit_type} to be given")
            if implicit_type in implicit_parameter:
                return implicit_parameter[implicit_type]

            raise ImplicitError(f"Expected {implicit_type} to be given")

        try:
            # The variable names __implicit_function__ and __implicit__ are constants
            __implicit_function__ = self._func
            __implicit_function__.__implicit__ = current_implicit  # type: ignore
            return __implicit_function__(*args, **kwargs)
        finally:
            if hasattr(self._func, _IMPLICIT):
                delattr(self._func, _IMPLICIT)

    @staticmethod
    def given(value: Any) -> None:
        """Add implicit parameter to the caller's stack frame."""
        frame = inspect.currentframe()
        try:
            if frame is None:
                raise RuntimeError("An unexpected error occurred")
            if (callers_frame := frame.f_back) is None:
                raise RuntimeError("An unexpected error occurred")

            if _IMPLICIT not in callers_frame.f_locals:
                callers_frame.f_locals[_IMPLICIT] = {}
            if type(value) in callers_frame.f_locals[_IMPLICIT]:
                raise ImplicitError(f"Duplicate implicit parameter of type {type(value).__name__}.")

            callers_frame.f_locals[_IMPLICIT][type(value)] = value
        finally:
            del frame

    @staticmethod
    def use[I](implicit_type: Type[I]) -> I:
        """Get implicit parameters with the following priority

        1. local scope
        2. global scope
        3. attributes of the calling function
        """
        frame = inspect.currentframe()
        try:
            if (current_frame := inspect.currentframe()) is None:
                raise RuntimeError("An unexpected error occurred")
            if (callers_frame := current_frame.f_back) is None:
                raise RuntimeError("An unexpected error occurred")

            # Local scope case
            if (implicit_parameters := callers_frame.f_locals.get(_IMPLICIT)) is not None:
                if implicit_type in implicit_parameters:
                    return implicit_parameters[implicit_type]

            # Global scope case
            if (implicit_parameter := callers_frame.f_globals.get(_IMPLICIT)) is not None:
                if implicit_type in implicit_parameter:
                    return implicit_parameter[implicit_type]

            # The Case of Function Object
            if (call_resource_frame := callers_frame.f_back) is None:
                raise ImplicitError(f"Expected {implicit_type} to be given")
            if (callers_func := call_resource_frame.f_locals.get(_IMPLICIT_FUNCTION)) is None:
                raise ImplicitError(f"Expected {implicit_type} to be given")
            if (implicit_parameter := getattr(callers_func, _IMPLICIT, None)) is None:
                raise ImplicitError(f"Expected {implicit_type} to be given")
            if implicit_type in implicit_parameter:
                return implicit_parameter[implicit_type]

            raise ImplicitError(f"Expected {implicit_type} to be given")
        finally:
            del frame

    @staticmethod
    def usage(*implicit_types: *U) -> Callable[[Callable[P, T]], Implicit[P, T, *U]]:
        """Defines implicit parameters to be applied to the function"""
        if len(implicit_types) == 0:
            raise ImplicitError("Expected at least one implicit type.")
        if not all(isinstance(t, type) for t in implicit_types):
            raise ImplicitError("Expected all implicit types to be types.", implicit_types)
        if len(implicit_types) != len(set(implicit_types)):
            raise ImplicitError("Duplicate implicit types found.", implicit_types)

        def constructor(func: Callable[P, T]) -> Implicit[P, T, *U]:
            return Implicit(func, *implicit_types)

        return constructor
