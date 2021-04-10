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

    assert Void is type(Void[int]().map(functor=lambda some: None))
    assert False is bool(Void[int]().map(functor=lambda some: 0))


def test_void_flatmap():
    from category import Some, Void

    assert Void is type(Void[int]().flatmap(functor=lambda some: Some[int](value=0)))
    assert False is bool(Void[int]().flatmap(functor=lambda some: Some[int](value=0)))


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


def test_void_convert():
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

    assert Void is type(Void[int]().convert(to_void))
    assert Some is type(Void[int]().convert(to_some))


def test_some():
    from category import Some

    assert Some is type(Some[int](value=0))
    assert True is bool(Some[int](value=0))


def test_some_map():
    from category import Some

    assert Some is type(Some[int](value=0).map(functor=lambda some: some + 1))
    assert True is bool(Some[int](value=0).map(functor=lambda some: some + 1))
    assert 1 == Some[int](value=0).map(functor=lambda some: some + 1).get()


def test_some_flatmap():
    from category import Some

    assert Some is type(
        Some[int](value=0).flatmap(functor=lambda some: Some[int](value=some + 1))
    )
    assert True is bool(
        Some[int](value=0).flatmap(functor=lambda some: Some[int](value=some + 1))
    )
    assert (
        1
        == Some[int](value=0)
        .flatmap(functor=lambda some: Some[int](value=some + 1))
        .get()
    )


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


def test_some_convert():
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

    assert Void is type(Some[int](value=1).convert(to_void))
    assert Some is type(Some[int](value=1).convert(to_some))
