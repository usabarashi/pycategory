import inspect
from copy import deepcopy
from typing import Any, Callable, NamedTuple, Optional, ParamSpec, TypeAlias, cast

P = ParamSpec("P")
Arguments: TypeAlias = dict[str, Any]

MASK = "****"


def masking(*, arguments: dict[Any, Any], unmask: Optional[tuple[Any, ...]]) -> dict[Any, Any]:
    return {
        key: MASK if (unmask is None) or (key not in unmask) else value
        for key, value in arguments.items()
    }


def apply_defaults(*, arguments: Arguments, function: Callable[..., Any]) -> Arguments:
    """Apply default arguments to arguments.

    - function.__defaults__: position or keyword defaults arguments.
    - function.__kwdefaults__: keyword only default arguments.
    """
    default_list = (
        [] if function.__defaults__ is None else [(None, value) for value in function.__defaults__]
    )
    keyword_only_default_list = (
        []
        if cast(Optional[dict[str, Any]], function.__kwdefaults__) is None
        else [(key, value) for key, value in function.__kwdefaults__.items()]
    )
    update_arguments = deepcopy(arguments)
    for argument_key, (default_key, default_value) in zip(
        reversed(update_arguments),
        reversed(default_list + keyword_only_default_list),
    ):
        match default_key:
            case None:
                # Apply position only default arguments
                # Apply position or keyword default arguments
                update_arguments[argument_key] = default_value
            case str():
                # Apply keyword only default arguments
                update_arguments[default_key] = default_value
    return update_arguments


def apply_parameters(arguments: Arguments, /, *args: ..., **kwargs: ...) -> Arguments:
    """Apply parameters to arguments."""
    update_arguments = deepcopy(arguments)
    position_parameters = [(None, value) for value in args]
    keyword_parameters = [(key, value) for key, value in cast(dict[str, Any], kwargs.items())]
    for argument_key, (parameter_key, parameter_value) in zip(
        update_arguments, position_parameters + keyword_parameters
    ):
        match parameter_key:
            case None:
                # Apply position parameters
                update_arguments[argument_key] = parameter_value
            case str():
                # Applying keyword parameters
                update_arguments[parameter_key] = parameter_value
    return update_arguments


def arguments(function: Callable[P, Any], /, *args: P.args, **kwargs: P.kwargs) -> Arguments:
    """Derive function arguments."""
    arguments = deepcopy(inspect.signature(function).parameters.copy())
    if len(arguments) == 0:
        return arguments

    default_applied_arguments = apply_defaults(arguments=arguments, function=function)
    parameter_applied_arguments = apply_parameters(default_applied_arguments, *args, **kwargs)

    return parameter_applied_arguments


def is_private_attribute(attribute: str) -> bool:
    return attribute.startswith("_")


def parse(object_: Any) -> Any:
    """Recursively decompose object structure."""

    def recursive(parse_object: Any, /) -> Any:
        match parse_object:
            case _ if callable(parse_object):
                return inspect.signature(parse_object)
            case _ if hasattr(parse_object, "__dict__"):
                return {
                    recursive(key): MASK if is_private_attribute(key) else recursive(value)
                    for key, value in dict(cast(dict[str, Any], parse_object.__dict__)).items()
                }
            case list():
                return [recursive(item) for item in cast(list[Any], parse_object)]
            case tuple():
                return tuple(recursive(item) for item in cast(tuple[Any, ...], parse_object))
            case set():
                return {recursive(item) for item in cast(set[Any], parse_object)}
            case dict():
                return {
                    recursive(key): recursive(value)
                    for key, value in cast(dict[Any, Any], parse_object.items())
                }
            case _:
                return parse_object

    return recursive(object_)


class Frame:
    DEPTH: int = 1

    def __init__(self, /, depth: Optional[int] = None, unmask: Optional[tuple[str, ...]] = None):
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
