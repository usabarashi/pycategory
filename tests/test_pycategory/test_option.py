def test_functor_law():
    from pycategory import VOID, Some, functor

    assert functor.identity_law(VOID)
    assert functor.identity_law(Some[int](42))
    assert functor.composite_law(F=VOID, f=lambda v: [v], g=lambda v: (v,))
    assert functor.composite_law(F=Some[int](42), f=lambda v: [v], g=lambda v: (v,))


def test_option_do():
    from pycategory import VOID, Option, OptionDo, Right, Some, Void

    @Option.do
    def safe_context() -> OptionDo[int]:  # type: ignore # Not access
        _ = yield from Some[bool](True)
        one = yield from Some[int](1)
        two = 2
        three = yield from Some[int](3)
        return one + two + three

    @Option.do
    def outside_context() -> OptionDo[int]:  # type: ignore # Not access
        _ = yield from Some[bool](True)
        one = yield from Some[int](1)
        two = 2
        three = yield from Some[int](3)
        _ = yield from Right[Exception, int](42)  # type: ignore # Error case
        return str(one + two + three)  # type: ignore # Error case

    @Option.do
    def void_context() -> OptionDo[int]:
        one = yield from Some[int](1)
        two = 2
        three = yield from VOID
        return one + two + three

    assert Void is type(void_context())
    assert True is void_context().is_empty()
    assert False is void_context().not_empty()
    assert None is void_context().fold(void=lambda: None, some=lambda some: None)

    @Option.do
    def some_context() -> OptionDo[int]:
        one = yield from Some[int](1)
        two = 2
        three = yield from Some[int](3)
        return one + two + three

    assert Some is type(some_context())
    assert 6 == some_context().get()
    assert False is some_context().is_empty()
    assert True is some_context().not_empty()
    assert None is some_context().fold(void=lambda: None, some=lambda some: None)


def test_void():
    from pycategory import VOID, Void

    assert Void is type(VOID)
    assert Void is type(eval(f"{repr(VOID)}"))


def test_void_map():
    from pycategory import VOID, Void

    void = VOID
    mapped_void = void.map(lambda some: 42)
    assert void is mapped_void
    assert Void is type(mapped_void)


def test_void_flat_map():
    from pycategory import Some, Void

    void = Void[int]()
    flat_mapped_void = void.flat_map(lambda some: Some[int](42))
    assert void is flat_mapped_void
    assert Void is type(flat_mapped_void)


def test_void_fold():
    from pycategory import VOID

    assert False is VOID.fold(void=lambda: False, some=lambda some: True)


def test_void_is_empty():
    from pycategory import VOID

    assert True is VOID.is_empty()


def test_void_not_empty():
    from pycategory import VOID

    assert False is VOID.not_empty()


def test_void_get():
    from pycategory import VOID

    try:
        VOID.get()
        assert False
    except Exception as error:
        assert ValueError is type(error)


def test_void_get_or_else():
    from pycategory import VOID

    assert False is VOID.get_or_else(lambda: False)


def test_some():
    from pycategory import Some

    assert Some is type(Some[int](42))
    assert Some is type(eval(f"{repr(Some[int](42))}"))


def test_some_map():
    from pycategory import Some

    some = Some[int](42)
    mapped_some = some.map(lambda some: some + 1)
    assert some is not mapped_some
    assert Some is type(mapped_some)
    assert 43 == mapped_some.get()


def test_some_flat_map():
    from pycategory import Some

    some = Some[int](42)
    flat_mapped_some = some.flat_map(lambda some: Some[int](some + 1))
    assert some is not flat_mapped_some
    assert Some is type(flat_mapped_some)
    assert 43 == flat_mapped_some.get()


def test_some_fold():
    from pycategory import Some

    assert True is Some[int](42).fold(void=lambda: False, some=lambda some: True)


def test_some_is_empty():
    from pycategory import Some

    assert False is Some[int](42).is_empty()


def test_some_not_empty():
    from pycategory import Some

    assert True is Some[int](42).not_empty()


def test_some_get():
    from pycategory import Some

    assert 42 == Some[int](42).get()


def test_some_get_or_else():
    from pycategory import Some

    assert 42 == Some[int](42).get_or_else(lambda: 8)


def test_dataclass():
    from dataclasses import asdict, dataclass
    from typing import cast

    from pycategory import VOID, Some, Void

    @dataclass(frozen=True)
    class AsDict:
        void: Void[int]
        some: Some[int]

    dict_data = asdict(AsDict(void=VOID, some=Some(42)))
    assert VOID is dict_data.get("void", None)
    assert Some is type(dict_data.get("some", None))
    assert 42 == cast(Some[int], dict_data.get("some", None)).get()


def test_pattern_match():
    from typing import cast

    from pycategory import VOID, Option, Some, Void

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

    match cast(Option[int], Some(41)), cast(Option[int], Some(42)), cast(Option[int], Some(43)):
        case Some(value=x), Some(value=y), Some(value=z) if x < y < z:
            assert True
        case _:
            assert False

    match cast(Option[Option[int]], Some(Some(42))):
        case Some(value=Some(value=x)) if x == 42:
            assert True
        case _:
            assert False


def test_json_encode():
    import json
    from dataclasses import asdict, dataclass
    from typing import Any, cast

    from pycategory import VOID, Some, Void

    class OptionEncoder(json.JSONEncoder):
        def default(self, o: Any) -> Any:
            def recur(obj: Any) -> Any:
                match obj:
                    case Void():
                        return None
                    case Some(primitive) if not hasattr(primitive, "__dict__"):  # type: ignore
                        return primitive  # type: ignore
                    case Some(value) if isinstance(value, Some):  # type: ignore
                        return recur(value)
                    case _:
                        return json.JSONEncoder.default(self, o)

            return recur(o)

    @dataclass(frozen=True)
    class Entity:
        void: Void[int]
        some: Some[Some[Some[int]]]

    dict_entity = asdict(Entity(void=VOID, some=Some(Some(Some(42)))))
    assert VOID is dict_entity.get("void")
    assert Some is type(dict_entity.get("some"))
    assert 42 == cast(Some[Some[Some[int]]], dict_entity.get("some")).get().get().get()

    json_entity = json.dumps(dict_entity, cls=OptionEncoder)
    assert 0 <= json_entity.find('"void": null')
    assert 0 <= json_entity.find('"some": 42')

    re_dict_entity = cast(dict[str, Any], json.loads(json_entity))
    assert None is re_dict_entity.get("void")
    assert 42 == re_dict_entity.get("some")
