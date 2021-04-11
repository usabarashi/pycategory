def test_option_do():
    from category import Option, OptionDo, Some, Void

    @Option.do
    def void_context() -> OptionDo[int]:
        one = yield from Some[int](value=1)()
        two = 2
        three = yield from Void[int]()()
        return one + two + three

    assert Void is type(void_context())
    assert False is bool(void_context())
    assert True is void_context().is_empty()
    assert False is void_context().not_empty()
    assert None is void_context().fold(void=lambda: None, some=lambda some: None)

    @Option.do
    def some_context() -> OptionDo[int]:
        one = yield from Some[int](value=1)()
        two = 2
        three = yield from Some[int](value=3)()
        return one + two + three

    assert Some(value=6) == some_context()
    assert 6 == some_context().get()
    assert True is bool(some_context())
    assert False is some_context().is_empty()
    assert True is some_context().not_empty()
    assert None is some_context().fold(void=lambda: None, some=lambda some: None)


def test_void():
    from category import Void

    assert Void is type(Void[int]())
    assert False is bool(Void[int]())


def test_void_map():
    from category import Void

    void = Void[int]()
    mapped_void = void.map(functor=lambda some: 0)
    assert void is mapped_void
    assert Void is type(mapped_void)
    assert False is bool(mapped_void)


def test_void_flatmap():
    from category import Some, Void

    void = Void[int]()
    flatmapped_void = void.flatmap(functor=lambda some: Some[int](value=0))
    assert void is flatmapped_void
    assert Void is type(flatmapped_void)
    assert False is bool(flatmapped_void)


def test_void_fold():
    from category import Void

    assert False is Void[int]().fold(void=lambda: False, some=lambda some: True)


def test_void_is_empty():
    from category import Void

    assert True is Void[int]().is_empty()


def test_void_not_empty():
    from category import Void

    assert False is Void[int]().not_empty()


def test_void_get():
    from category import Void

    try:
        Void[int]().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)


def test_void_get_or_else():
    from category import Void

    assert False is Void[int]().get_or_else(default=lambda: False)


def test_void_method():
    from category import Option, Some, Void

    def to_void(option: Option[int]) -> Void[int]:
        if isinstance(option.pattern, Void):
            return option.pattern
        else:
            return Void[int]()

    def to_some(option: Option[int]) -> Some[int]:
        if isinstance(option.pattern, Void):
            return Some[int](value=0)
        else:
            return option.pattern

    assert Void is type(Void[int]().method(to_void))
    assert Some is type(Void[int]().method(to_some))


def test_some():
    from category import Some

    assert Some is type(Some[int](value=0))
    assert True is bool(Some[int](value=0))


def test_some_map():
    from category import Some

    some = Some[int](value=0)
    mapped_some = some.map(functor=lambda some: some + 1)
    assert some is not mapped_some
    assert Some is type(mapped_some)
    assert True is bool(mapped_some)
    assert 1 == mapped_some.get()


def test_some_flatmap():
    from category import Some

    some = Some[int](value=0)
    flatmapped_some = some.flatmap(functor=lambda some: Some[int](value=some + 1))
    assert some is not flatmapped_some
    assert Some is type(flatmapped_some)
    assert True is bool(flatmapped_some)
    assert 1 == flatmapped_some.get()


def test_some_fold():
    from category import Some

    assert True is Some[int](value=0).fold(void=lambda: False, some=lambda some: True)


def test_some_is_empty():
    from category import Some

    assert False is Some[int](value=0).is_empty()


def test_some_not_empty():
    from category import Some

    assert True is Some[int](value=0).not_empty()


def test_some_get():
    from category import Some

    assert 0 == Some[int](value=0).get()


def test_some_get_or_else():
    from category import Some

    assert 0 == Some[int](value=0).get_or_else(default=lambda: 1)


def test_some_method():
    from category import Option, Some, Void

    def to_void(option: Option[int]) -> Void[int]:
        if isinstance(option.pattern, Void):
            return option.pattern
        else:
            return Void[int]()

    def to_some(option: Option[int]) -> Some[int]:
        if isinstance(option.pattern, Void):
            return Some[int](value=0)
        else:
            return option.pattern

    assert Void is type(Some[int](value=1).method(to_void))
    assert Some is type(Some[int](value=1).method(to_some))
