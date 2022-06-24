def test_option_do():
    from category import VOID, OptionDo, Some, Void, do

    @do
    def void_context() -> OptionDo[int]:
        one = yield from Some[int](1)
        two = 2
        three = yield from VOID
        return one + two + three

    assert Void is type(void_context())
    assert False is bool(void_context())
    assert True is void_context().is_empty()
    assert False is void_context().not_empty()
    assert None is void_context().fold(void=lambda: None, some=lambda some: None)

    @do
    def some_context() -> OptionDo[int]:
        one = yield from Some[int](1)
        two = 2
        three = yield from Some[int](3)
        return one + two + three

    assert Some is type(some_context())
    assert 6 == some_context().get()
    assert True is bool(some_context())
    assert False is some_context().is_empty()
    assert True is some_context().not_empty()
    assert None is some_context().fold(void=lambda: None, some=lambda some: None)


def test_void():
    from category import VOID, Void

    assert Void is type(VOID)
    assert False is bool(VOID)


def test_void_map():
    from category import VOID, Void

    void = VOID
    mapped_void = void.map(lambda some: 42)
    assert void is mapped_void
    assert Void is type(mapped_void)
    assert False is bool(mapped_void)


def test_void_flatmap():
    from category import Some, Void

    void = Void[int]()
    flatmapped_void = void.flatmap(lambda some: Some[int](42))
    assert void is flatmapped_void
    assert Void is type(flatmapped_void)
    assert False is bool(flatmapped_void)


def test_void_fold():
    from category import VOID

    assert False is VOID.fold(void=lambda: False, some=lambda some: True)


def test_void_is_empty():
    from category import VOID

    assert True is VOID.is_empty()


def test_void_not_empty():
    from category import VOID

    assert False is VOID.not_empty()


def test_void_get():
    from category import VOID

    try:
        VOID.get()
        assert False
    except Exception as error:
        assert ValueError is type(error)


def test_void_get_or_else():
    from category import VOID

    assert False is VOID.get_or_else(lambda: False)


def test_void_method():
    from category import VOID, Option, Some, Void

    def to_void(self: Option[int], /) -> Void[int]:
        if isinstance(self.pattern, Void):
            return self.pattern
        else:
            return VOID

    def to_some(self: Option[int], /) -> Some[int]:
        if isinstance(self.pattern, Void):
            return Some[int](42)
        else:
            return self.pattern

    assert Void is type(VOID.method(to_void))
    assert Some is type(VOID.method(to_some))


def test_some():
    from category import Some

    assert Some is type(Some[int](42))
    assert True is bool(Some[int](42))


def test_some_map():
    from category import Some

    some = Some[int](42)
    mapped_some = some.map(lambda some: some + 1)
    assert some is not mapped_some
    assert Some is type(mapped_some)
    assert True is bool(mapped_some)
    assert 43 == mapped_some.get()


def test_some_flatmap():
    from category import Some

    some = Some[int](42)
    flatmapped_some = some.flatmap(lambda some: Some[int](some + 1))
    assert some is not flatmapped_some
    assert Some is type(flatmapped_some)
    assert True is bool(flatmapped_some)
    assert 43 == flatmapped_some.get()


def test_some_fold():
    from category import Some

    assert True is Some[int](42).fold(void=lambda: False, some=lambda some: True)


def test_some_is_empty():
    from category import Some

    assert False is Some[int](42).is_empty()


def test_some_not_empty():
    from category import Some

    assert True is Some[int](42).not_empty()


def test_some_get():
    from category import Some

    assert 42 == Some[int](42).get()


def test_some_get_or_else():
    from category import Some

    assert 42 == Some[int](42).get_or_else(lambda: 8)


def test_some_method():
    from category import VOID, Option, Some, Void

    def to_void(self: Option[int], /) -> Void[int]:
        if isinstance(self.pattern, Void):
            return self.pattern
        else:
            return VOID

    def to_some(self: Option[int], /) -> Some[int]:
        if isinstance(self.pattern, Void):
            return Some[int](42)
        else:
            return self.pattern

    assert Void is type(Some[int](42).method(to_void))
    assert Some is type(Some[int](42).method(to_some))


def test_dataclass():
    from dataclasses import asdict, dataclass

    from category import VOID, Some, Void

    @dataclass(frozen=True)
    class AsDict:
        void: Void[int]
        some: Some[int]

    dict_data = asdict(AsDict(void=VOID, some=Some(42)))
    assert VOID is dict_data.get("void", None)
    assert Some is type(dict_data.get("some", None))
    assert 42 == dict_data.get("some", None).get()


def test_pattern_match():
    from typing import cast

    from category import VOID, Option, Some, Void

    match cast(Option[int], VOID):
        case Void():
            assert True
        case _:
            assert False

    match cast(Option[int], Some(42)):
        case Some(42):
            assert True
        case _:
            assert False

    match cast(Option[int], VOID), cast(Option[int], VOID):
        case Void() as a, Void() as b if a is b:
            assert True
        case _:
            assert False

    match cast(Option[int], Some(41)), cast(Option[int], Some(42)), cast(
        Option[int], Some(43)
    ):
        case Some(x), Some(y), Some(z) if x < y < z:
            assert True
        case _:
            assert False
