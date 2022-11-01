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
    """Derive function arguments"""
    arguments = deepcopy(inspect.signature(function).parameters.copy())
    if len(arguments) == 0:
        return arguments

    position_or_keyword_defaults = (
        []
        if function.__defaults__ is None
        else [(None, value) for value in function.__defaults__]
    )
    keyword_defaults = (
        []
        if function.__kwdefaults__ is None
        else [(key, value) for key, value in function.__kwdefaults__.items()]
    )
    for key, (default_key, default_value) in zip(
        reversed(arguments),
        reversed(position_or_keyword_defaults + keyword_defaults),
    ):
        match default_key:
            case None:
                # Apply position or keyword default arguments
                arguments[key] = default_value
            case str():
                # Apply keyword default arguments
                arguments[default_key] = default_value

    position_parameters = [(None, value) for value in cast(tuple[Any, ...], args)]
    keyword_parameters = [
        (key, value) for key, value in cast(dict[str, Any], kwargs.items())
    ]
    for key, (parameter_key, parameter_value) in zip(
        arguments, position_parameters + keyword_parameters
    ):
        match parameter_key:
            case None:
                # Apply position parameters
                arguments[key] = parameter_value
            case str():
                # Applying keyword parameters
                arguments[parameter_key] = parameter_value

    return arguments


def is_private_attribute(attribute: str) -> bool:
    return attribute.startswith("_")


def parse(object_: Any) -> Any:
    """Recursively decompose object structure"""

    def recursive(parse_object: Any, /) -> Any:
        match parse_object:
            case class_object if hasattr(class_object, "__dict__"):
                return {
                    recursive(key): MASK
                    if is_private_attribute(key)
                    else recursive(value)
                    for key, value in dict(
                        cast(dict[str, Any], class_object.__dict__)
                    ).items()
                }
            case list() as list_object:
                return [recursive(item) for item in cast(list[Any], list_object)]
            case tuple() as tuple_object:
                return tuple(
                    recursive(item) for item in cast(tuple[Any, ...], tuple_object)
                )
            case set() as set_object:
                return {recursive(item) for item in cast(set[Any], set_object)}
            case dict() as dict_object:
                return {
                    recursive(key): recursive(value)
                    for key, value in cast(dict[Any, Any], dict_object.items())
                }
            case _:
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
