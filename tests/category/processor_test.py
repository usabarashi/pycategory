def test_masking():
    from category import processor

    half_masked_arguments = processor.masking(
        arguments={"mask": 42, "unmask": 42}, unmask=("unmask",)
    )
    assert processor.MASK == half_masked_arguments.get("mask", None)
    assert 42 == half_masked_arguments.get("unmask", None)

    masked_arguments = processor.masking(
        arguments={"mask": 42, "unmask": 42}, unmask=None
    )
    assert processor.MASK == masked_arguments.get("mask", None)
    assert processor.MASK == masked_arguments.get("unmask", None)


def test_arguments():
    from typing import Any, Optional

    from category import processor

    def annotations_arguments(
        position1: int,
        position2: int,
        name1: str,
        name2: Optional[list[str]] = None,
        name3: Optional[dict[str, Any]] = None,
    ) -> None:
        ...

    args = (0, 1, "1")
    kwargs = {"name2": ["2"], "name3": {3: 3}}

    arguments = processor.arguments(annotations_arguments, *args, **kwargs)
    assert {
        "position1": 0,
        "position2": 1,
        "name1": "1",
        "name2": ["2"],
        "name3": {3: 3},
    } == arguments

    def no_return_annotations(
        position1: int,
        position2: int,
        name1: str,
        name2: Optional[list[str]] = None,
        name3: Optional[dict[str, Any]] = None,
    ):
        ...

    arguments = processor.arguments(no_return_annotations, *args, **kwargs)
    assert {
        "position1": 0,
        "position2": 1,
        "name1": "1",
        "name2": ["2"],
        "name3": {3: 3},
    } == arguments

    def no_default_annotations(
        position1: int,
        position2: int,
        name1: str,
        name2: Optional[list[str]],
        name3: Optional[dict[str, Any]],
    ) -> None:
        ...

    arguments = processor.arguments(no_default_annotations, *args, **kwargs)
    assert {
        "position1": 0,
        "position2": 1,
        "name1": "1",
        "name2": ["2"],
        "name3": {3: 3},
    } == arguments

    def plane_arguments(
        position1,
        position2,
        name1,
        name2=None,
        name3=None,
    ) -> None:
        ...

    arguments = processor.arguments(plane_arguments, *args, **kwargs)

    assert 0 == len(arguments)


def test_is_private():
    from category import processor

    assert False is processor.is_private_attribute("public")
    assert True is processor.is_private_attribute("_private")


def test_parse():
    from typing import Any

    from category import processor

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
        ):
            self.int_ = int_
            self.str_ = str_
            self.bool_ = bool_
            self.list_ = list_
            self.tuple_ = tuple_
            self.set_ = set_
            self.dict_ = dict_

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
    } == parsed_sample


def test_frame():
    from category import Either, EitherDo, Frame, Left, Right, processor

    def function(arg1: int, arg2: int, arg3: int) -> Frame:
        variable1 = 42
        variable2 = 42
        variable3 = 42
        return Frame(unmask=("arg1", "variable1"))

    frame = function(arg1=42, arg2=42, arg3=42)
    assert 42 == frame.variables.get("arg1", None)
    assert processor.MASK == frame.variables.get("arg2", None)
    assert processor.MASK == frame.variables.get("arg3", None)
    assert 42 == frame.variables.get("variable1", None)
    assert processor.MASK == frame.variables.get("variable2", None)
    assert processor.MASK == frame.variables.get("variable3", None)

    class Error(Frame):
        ...

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
