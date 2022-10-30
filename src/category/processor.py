import inspect
from copy import deepcopy
from typing import Any, Callable, NamedTuple, Optional, ParamSpec, TypeAlias, cast

P = ParamSpec("P")
Arguments: TypeAlias = dict[str, Any]

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
) -> Arguments:
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


def is_private_attribute(attribute: str) -> bool:
    return attribute.startswith("_")


def parse(object_: Any) -> Any:
    """Recursively decompose object structure"""

    def recursive(parse_object: Any, /) -> Any:
        # Class case
        if hasattr(parse_object, "__dict__"):
            return {
                recursive(key): MASK if is_private_attribute(key) else recursive(value)
                for key, value in dict(
                    cast(dict[str, Any], parse_object.__dict__)
                ).items()
            }
        elif isinstance(parse_object, list):
            return [recursive(item) for item in cast(list[Any], parse_object)]
        elif isinstance(parse_object, tuple):
            return tuple(
                recursive(item) for item in cast(tuple[Any, ...], parse_object)
            )
        elif isinstance(parse_object, set):
            return {recursive(item) for item in cast(set[Any], parse_object)}
        elif isinstance(parse_object, dict):
            return {
                recursive(key): recursive(value)
                for key, value in cast(dict[Any, Any], parse_object.items())
            }
        else:
            return parse_object

    return recursive(object_)


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


class RuntimeErrorReport(NamedTuple):
    arguments: Arguments
    debug: Optional[Exception | Any]


def execute_debugger(
    debugger: Optional[Callable[[Arguments], Any]],
    arguments: Arguments,
) -> Optional[Exception | Any]:
    if (debugger is None) or (arguments == {}):
        return None
    try:
        return debugger(arguments)
    except Exception as exception:
        return exception
