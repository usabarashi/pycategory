import inspect
from copy import deepcopy
from typing import Any, Callable, Optional, ParamSpec

P = ParamSpec("P")

MASK = "****"


def masking(
    *, arguments: dict[Any, Any], unmask: Optional[tuple[Any, ...]]
) -> dict[Any, Any]:
    return {
        key: MASK if (unmask is None) or (key not in unmask) else value
        for key, value in arguments.items()
    }


def arguments(
    function: Callable[P, Any], /, *args: P.args, **kwargs: P.kwargs
) -> dict[str, Any]:
    """Derive function arguments

    If there is no TypeHint in the function signature, {} is returned.
    """
    arguments = deepcopy(function.__annotations__)
    if "return" in arguments:
        del arguments["return"]
    if len(arguments) == 0:
        return arguments
    # Apply default arguments
    if function.__defaults__ is not None:
        for index, key in enumerate(reversed(arguments)):
            if len(function.__defaults__) <= index:
                break
            else:
                arguments[key] = function.__defaults__[index]
    # Apply positional parameters
    for index, key in enumerate(arguments):
        if len(args) <= index:
            break
        else:
            arguments[key] = args[index]
    # Applying named parameters
    for key, value in kwargs.items():
        arguments[key] = value
    return arguments


class Frame:
    DEPTH: int = 1

    def __init__(
        self, /, depth: Optional[int] = None, unmask: Optional[tuple[str, ...]] = None
    ):
        target_depth = self.DEPTH if depth is None else depth
        self.filename: str = inspect.stack()[target_depth].filename
        self.line: int = inspect.stack()[target_depth].frame.f_lineno
        self.function: str = inspect.stack()[target_depth].function
        self.variables: dict[str, Any] = masking(
            arguments=inspect.getargvalues(inspect.stack()[target_depth].frame).locals,
            unmask=unmask,
        )
        self.stack: list[inspect.FrameInfo] = inspect.stack()
