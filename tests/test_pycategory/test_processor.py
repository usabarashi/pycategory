def test_masking():
    from pycategory import processor

    half_masked_arguments = processor.masking(
        arguments={"mask": 42, "unmask": 42}, unmask=("unmask",)
    )
    assert processor.MASK == half_masked_arguments.get("mask", None)
    assert 42 == half_masked_arguments.get("unmask", None)

    masked_arguments = processor.masking(arguments={"mask": 42, "unmask": 42}, unmask=None)
    assert processor.MASK == masked_arguments.get("mask", None)
    assert processor.MASK == masked_arguments.get("unmask", None)


def test_apply_defaults():
    import inspect
    from copy import deepcopy
    from typing import Optional

    from pycategory import processor

    def position_defaults_arguments(arg1: int, arg2: Optional[int] = None, /): ...

    arguments = inspect.signature(position_defaults_arguments).parameters.copy()
    position_defaults_applied_arguments = processor.apply_defaults(
        arguments=arguments, function=position_defaults_arguments
    )
    assert id(arguments) != id(position_defaults_applied_arguments)
    assert_arguments = deepcopy(arguments)
    assert_arguments |= {"arg2": None}
    assert assert_arguments == position_defaults_applied_arguments

    def position_or_keyword_default_arguments(arg1: int, arg2: Optional[int] = None): ...

    arguments = inspect.signature(position_or_keyword_default_arguments).parameters.copy()
    position_or_keyword_defaults_applied_arguments = processor.apply_defaults(
        arguments=arguments, function=position_defaults_arguments
    )
    assert_arguments = deepcopy(arguments)
    assert_arguments |= {"arg2": None}
    assert assert_arguments == position_or_keyword_defaults_applied_arguments

    def keyword_defaults_arguments(*, arg1: int, arg2: Optional[int] = None): ...

    arguments = inspect.signature(keyword_defaults_arguments).parameters.copy()
    keyword_defaults_applied_arguments = processor.apply_defaults(
        arguments=arguments, function=position_defaults_arguments
    )
    assert_arguments = deepcopy(arguments)
    assert_arguments |= {"arg2": None}
    assert assert_arguments == keyword_defaults_applied_arguments


def test_apply_parameter():
    import inspect
    from typing import Optional

    from pycategory import processor

    def position_only_parameter(arg1: int, arg2: Optional[int] = None, /): ...

    arguments = inspect.signature(position_only_parameter).parameters.copy()
    applied_position_only_arguments = processor.apply_parameters(arguments, *(1, 2))
    assert id(arguments) != id(applied_position_only_arguments)
    assert {"arg1": 1, "arg2": 2} == applied_position_only_arguments

    def position_or_keyword_default_parameter(arg1: int, arg2: Optional[int] = None): ...

    arguments = inspect.signature(position_or_keyword_default_parameter).parameters.copy()
    applied_position_or_keyword_arguments = processor.apply_parameters(
        arguments, *(1,), **{"arg2": 2}
    )
    assert {"arg1": 1, "arg2": 2} == applied_position_or_keyword_arguments

    def keyword_only_parameter(*, arg1: int, arg2: Optional[int] = None): ...

    arguments = inspect.signature(keyword_only_parameter).parameters.copy()
    applied_keyword_only_arguments = processor.apply_parameters(arguments, **{"arg1": 1, "arg2": 2})
    assert {"arg1": 1, "arg2": 2} == applied_keyword_only_arguments


def test_arguments():
    from typing import Optional

    from pycategory import processor

    def position_only_no_default(position: int, /) -> None: ...

    assert {"position": 42} == processor.arguments(position_only_no_default, *(42,), **{})

    def position_only_has_default(position: Optional[int] = None, /) -> None: ...

    assert {"position": None} == processor.arguments(position_only_has_default, *(), **{})
    assert {"position": 42} == processor.arguments(position_only_has_default, *(42,), **{})

    def position_or_keyword_no_default(position_or_keyword: int) -> None: ...

    assert {"position_or_keyword": 42} == processor.arguments(
        position_or_keyword_no_default, *(42,), **{}
    )
    assert {"position_or_keyword": 42} == processor.arguments(
        position_or_keyword_no_default, *(), **{"position_or_keyword": 42}
    )

    def position_or_keyword_has_default(
        position_or_keyword: Optional[int] = None,
    ) -> None: ...

    assert {"position_or_keyword": None} == processor.arguments(
        position_or_keyword_has_default, *(), **{}
    )
    assert {"position_or_keyword": 42} == processor.arguments(
        position_or_keyword_has_default, *(42,), **{}
    )
    assert {"position_or_keyword": 42} == processor.arguments(
        position_or_keyword_has_default, *(), **{"position_or_keyword": 42}
    )

    def keyword_only_no_default(*, keyword: int) -> None: ...

    assert {"keyword": 42} == processor.arguments(keyword_only_no_default, *(), **{"keyword": 42})

    def keyword_only_has_default(keyword: Optional[int] = None, /) -> None: ...

    assert {"keyword": None} == processor.arguments(keyword_only_has_default, *(), **{})
    assert {"keyword": 42} == processor.arguments(keyword_only_has_default, *(), **{"keyword": 42})

    def complex_no_default(
        position1: int,
        position2: int,
        /,
        position_or_keyword_1: int,
        position_or_keyword_2: int,
        *,
        keyword1: int,
        keyword2: int,
    ) -> None: ...

    assert {
        "position1": 0,
        "position2": 1,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": 3,
        "keyword1": 4,
        "keyword2": 5,
    } == processor.arguments(
        complex_no_default,
        *(0, 1),
        **{
            "position_or_keyword_1": 2,
            "position_or_keyword_2": 3,
            "keyword1": 4,
            "keyword2": 5,
        },
    )
    assert {
        "position1": 0,
        "position2": 1,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": 3,
        "keyword1": 4,
        "keyword2": 5,
    } == processor.arguments(
        complex_no_default,
        *(0, 1, 2),
        **{
            "position_or_keyword_2": 3,
            "keyword1": 4,
            "keyword2": 5,
        },
    )
    assert {
        "position1": 0,
        "position2": 1,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": 3,
        "keyword1": 4,
        "keyword2": 5,
    } == processor.arguments(
        complex_no_default,
        *(0, 1, 2, 3),
        **{
            "keyword1": 4,
            "keyword2": 5,
        },
    )

    def complex_position_has_default(
        position1: int,
        position2: Optional[int] = None,
        /,
        position_or_keyword_1: Optional[int] = None,
        position_or_keyword_2: Optional[int] = None,
        *,
        keyword1: Optional[int] = None,
        keyword2: Optional[int] = None,
    ) -> None: ...

    assert {
        "position1": 0,
        "position2": 1,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": 3,
        "keyword1": 4,
        "keyword2": 5,
    } == processor.arguments(
        complex_position_has_default,
        *(0, 1),
        **{
            "position_or_keyword_1": 2,
            "position_or_keyword_2": 3,
            "keyword1": 4,
            "keyword2": 5,
        },
    )

    assert {
        "position1": 0,
        "position2": None,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": 3,
        "keyword1": 4,
        "keyword2": 5,
    } == processor.arguments(
        complex_position_has_default,
        *(0,),
        **{
            "position_or_keyword_1": 2,
            "position_or_keyword_2": 3,
            "keyword1": 4,
            "keyword2": 5,
        },
    )

    assert {
        "position1": 0,
        "position2": None,
        "position_or_keyword_1": None,
        "position_or_keyword_2": 3,
        "keyword1": 4,
        "keyword2": 5,
    } == processor.arguments(
        complex_position_has_default,
        *(0,),
        **{
            "position_or_keyword_2": 3,
            "keyword1": 4,
            "keyword2": 5,
        },
    )

    assert {
        "position1": 0,
        "position2": None,
        "position_or_keyword_1": None,
        "position_or_keyword_2": None,
        "keyword1": 4,
        "keyword2": 5,
    } == processor.arguments(
        complex_position_has_default,
        *(0,),
        **{
            "keyword1": 4,
            "keyword2": 5,
        },
    )

    assert {
        "position1": 0,
        "position2": None,
        "position_or_keyword_1": None,
        "position_or_keyword_2": None,
        "keyword1": None,
        "keyword2": 5,
    } == processor.arguments(
        complex_position_has_default,
        *(0,),
        **{
            "keyword2": 5,
        },
    )

    assert {
        "position1": 0,
        "position2": None,
        "position_or_keyword_1": None,
        "position_or_keyword_2": None,
        "keyword1": None,
        "keyword2": None,
    } == processor.arguments(
        complex_position_has_default,
        *(0,),
        **{},
    )

    def complex_position_or_keyword_has_default(
        position1: int,
        position2: int,
        /,
        position_or_keyword_1: int,
        position_or_keyword_2: Optional[int] = None,
        *,
        keyword1: Optional[int] = None,
        keyword2: Optional[int] = None,
    ) -> None: ...

    assert {
        "position1": 0,
        "position2": 1,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": 3,
        "keyword1": 4,
        "keyword2": 5,
    } == processor.arguments(
        complex_position_or_keyword_has_default,
        *(0, 1),
        **{
            "position_or_keyword_1": 2,
            "position_or_keyword_2": 3,
            "keyword1": 4,
            "keyword2": 5,
        },
    )

    assert {
        "position1": 0,
        "position2": 1,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": None,
        "keyword1": 4,
        "keyword2": 5,
    } == processor.arguments(
        complex_position_or_keyword_has_default,
        *(0, 1),
        **{
            "position_or_keyword_1": 2,
            "keyword1": 4,
            "keyword2": 5,
        },
    )

    assert {
        "position1": 0,
        "position2": 1,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": None,
        "keyword1": None,
        "keyword2": 5,
    } == processor.arguments(
        complex_position_or_keyword_has_default,
        *(0, 1),
        **{
            "position_or_keyword_1": 2,
            "keyword2": 5,
        },
    )

    assert {
        "position1": 0,
        "position2": 1,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": None,
        "keyword1": None,
        "keyword2": None,
    } == processor.arguments(
        complex_position_or_keyword_has_default,
        *(0, 1),
        **{
            "position_or_keyword_1": 2,
        },
    )

    def complex_keyword_has_default(
        position1: int,
        position2: int,
        /,
        position_or_keyword_1: int,
        position_or_keyword_2: int,
        *,
        keyword1: int,
        keyword2: Optional[int] = None,
    ) -> None: ...

    assert {
        "position1": 0,
        "position2": 1,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": 3,
        "keyword1": 4,
        "keyword2": 5,
    } == processor.arguments(
        complex_keyword_has_default,
        *(0, 1),
        **{
            "position_or_keyword_1": 2,
            "position_or_keyword_2": 3,
            "keyword1": 4,
            "keyword2": 5,
        },
    )
    assert {
        "position1": 0,
        "position2": 1,
        "position_or_keyword_1": 2,
        "position_or_keyword_2": 3,
        "keyword1": 4,
        "keyword2": None,
    } == processor.arguments(
        complex_keyword_has_default,
        *(0, 1),
        **{
            "position_or_keyword_1": 2,
            "position_or_keyword_2": 3,
            "keyword1": 4,
        },
    )


def test_is_private():
    from pycategory import processor

    assert False is processor.is_private_attribute("public")
    assert True is processor.is_private_attribute("_private")


def test_parse():
    import inspect
    from typing import Any, Callable

    from pycategory import processor

    class Sample:
        def __init__(
            self,
            int_: int,
            str_: str,
            bool_: bool,
            list_: list[Any],
            tuple_: tuple[Any, ...],
            set_: set[Any],
            dict_: dict[Any, Any],
            function_: Callable[..., Any],
        ):
            self.function_ = function_
            self.int_ = int_
            self.str_ = str_
            self.bool_ = bool_
            self.list_ = list_
            self.tuple_ = tuple_
            self.set_ = set_
            self.dict_ = dict_

    def argument_function(value: int) -> int:
        return value

    sample = Sample(
        int_=42,
        str_="42",
        bool_=False,
        list_=[
            42,
            "42",
            False,
            [42, "42", [42, "42"], (42, "42"), {42, "42"}, {42: 42, "42": "42"}],
        ],
        tuple_=(
            42,
            "42",
            False,
            [42, "42", [42, "42"], (42, "42"), {42, "42"}, {42: 42, "42": "42"}],
        ),
        set_={42, "42", False, (42, "42", (42, "42"))},
        dict_={
            42: 42,
            "42": "42",
            False: False,
            (42, "42", (42, "42")): [
                42,
                "42",
                [42, "42"],
                (42, "42"),
                {42, "42"},
                {42: 42, "42": "42"},
            ],
        },
        function_=argument_function,
    )
    parsed_sample = processor.parse(sample)
    assert parsed_sample is not sample
    assert {
        "int_": 42,
        "str_": "42",
        "bool_": False,
        "list_": [
            42,
            "42",
            False,
            [42, "42", [42, "42"], (42, "42"), {42, "42"}, {42: 42, "42": "42"}],
        ],
        "tuple_": (
            42,
            "42",
            False,
            [42, "42", [42, "42"], (42, "42"), {42, "42"}, {42: 42, "42": "42"}],
        ),
        "set_": {42, "42", False, (42, "42", (42, "42"))},
        "dict_": {
            42: 42,
            "42": "42",
            False: False,
            (42, "42", (42, "42")): [
                42,
                "42",
                [42, "42"],
                (42, "42"),
                {42, "42"},
                {42: 42, "42": "42"},
            ],
        },
        "function_": inspect.signature(argument_function),
    } == parsed_sample


def test_frame():
    from pycategory import Either, EitherDo, Frame, Left, Right, processor

    def function(arg1: int, arg2: int, arg3: int) -> Frame:
        variable1 = 42  # type: ignore # Frame parameter
        variable2 = 42  # type: ignore # Frame parameter
        variable3 = 42  # type: ignore # Frame parameter
        return Frame(unmask=("arg1", "variable1"))

    frame = function(arg1=42, arg2=42, arg3=42)
    assert 42 == frame.variables.get("arg1", None)
    assert processor.MASK == frame.variables.get("arg2", None)
    assert processor.MASK == frame.variables.get("arg3", None)
    assert 42 == frame.variables.get("variable1", None)
    assert processor.MASK == frame.variables.get("variable2", None)
    assert processor.MASK == frame.variables.get("variable3", None)

    class Error(Frame): ...

    @Either.do
    def context(*, mask: int, unmask: int) -> EitherDo[Error, int]:
        one = yield from Left[Error, int](Error(unmask=("unmask",)))
        two = 2
        three = yield from Right[Error, int](3)
        return one + two + three

    result = context(mask=42, unmask=42)
    assert Left is type(result)
    assert Error is type(result.left().get())
    assert "****" == result.left().get().variables.get("mask", None)
    assert 42 == result.left().get().variables.get("unmask", None)


def test_execute_debugger():
    from pycategory import processor

    assert None is processor.execute_debugger(debugger=None, arguments={"value": 42})
    assert None is processor.execute_debugger(debugger=lambda arguments: None, arguments={})
    assert isinstance(
        processor.execute_debugger(
            debugger=lambda arguments: arguments["John Doe."], arguments={"value": 42}
        ),
        Exception,
    )
    assert 42 == processor.execute_debugger(
        debugger=lambda arguments: arguments.get("value"), arguments={"value": 42}
    )
