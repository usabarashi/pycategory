def test_apply():
    from pycategory import Extractor

    class Unit(Extractor):
        ...

    assert Unit is type(Unit.apply())

    class Tuple1(Extractor):

        __match_args__ = ("value",)

        def __init__(self, value: int):
            self.value = value

    assert Tuple1 is type(Tuple1.apply(42))

    class TupleN(Extractor):

        __match_args__ = ("int_", "str_", "bool_")

        def __init__(self, int_: int, str_: str, bool_: bool):
            self.int_ = int_
            self.str_ = str_
            self.bool_ = bool_

    assert TupleN is type(TupleN.apply(42, "42", True))


def test_unapply():
    from pycategory import Extractor

    class Unit(Extractor):
        ...

    assert () == Unit.apply().unapply()

    class Tuple1(Extractor):

        __match_args__ = ("value",)

        def __init__(self, value: int):
            self.value = value

    assert (42,) == Tuple1.apply(42).unapply()

    class TupleN(Extractor):

        __match_args__ = ("int_", "str_", "bool_")

        def __init__(self, int_: int, str_: str, bool_: bool):
            self.int_ = int_
            self.str_ = str_
            self.bool_ = bool_

    assert (42, "42", True) == TupleN.apply(42, "42", True).unapply()


def test_structural_pattern_match():
    from pycategory import Extractor

    class Unit(Extractor):
        ...

    match Unit.apply():
        case Unit():
            ...
        case _:
            assert False

    class Tuple1(Extractor):

        __match_args__ = ("value",)

        def __init__(self, value: int):
            self.value = value

    match Tuple1.apply(42):
        case Tuple1(value=42):
            ...
        case _:
            assert False

    class TupleN(Extractor):

        __match_args__ = ("int_", "str_", "bool_")

        def __init__(self, int_: int, str_: str, bool_: bool):
            self.int_ = int_
            self.str_ = str_
            self.bool_ = bool_

    match TupleN.apply(42, "42", True):
        case TupleN(int_=42, str_="42", bool_=True):
            ...
        case _:
            assert False
