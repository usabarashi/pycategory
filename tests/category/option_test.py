def test_option_do():
    from category import VOID, Option, OptionDo, Some, Void

    @Option.do
    def void_context() -> OptionDo[int]:
        one = yield from Some[int](1)()
        two = 2
        three = yield from VOID()
        return one + two + three

    assert Void is type(void_context())
    assert False is bool(void_context())
    assert True is void_context().is_empty()
    assert False is void_context().not_empty()
    assert None is void_context().fold(void=lambda: None, some=lambda some: None)

    @Option.do
    def some_context() -> OptionDo[int]:
        one = yield from Some[int](1)()
        two = 2
        three = yield from Some[int](3)()
        return one + two + three

    assert Some(6) == some_context()
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
    mapped_void = void.map(lambda some: 0)
    assert void is mapped_void
    assert Void is type(mapped_void)
    assert False is bool(mapped_void)


def test_void_flatmap():
    from category import Some, Void

    void = Void[int]()
    flatmapped_void = void.flatmap(lambda some: Some[int](0))
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
            return Some[int](0)
        else:
            return self.pattern

    assert Void is type(VOID.method(to_void))
    assert Some is type(VOID.method(to_some))


def test_some():
    from category import Some

    assert Some is type(Some[int](0))
    assert True is bool(Some[int](0))


def test_some_map():
    from category import Some

    some = Some[int](0)
    mapped_some = some.map(lambda some: some + 1)
    assert some is not mapped_some
    assert Some is type(mapped_some)
    assert True is bool(mapped_some)
    assert 1 == mapped_some.get()


def test_some_flatmap():
    from category import Some

    some = Some[int](0)
    flatmapped_some = some.flatmap(lambda some: Some[int](some + 1))
    assert some is not flatmapped_some
    assert Some is type(flatmapped_some)
    assert True is bool(flatmapped_some)
    assert 1 == flatmapped_some.get()


def test_some_fold():
    from category import Some

    assert True is Some[int](0).fold(void=lambda: False, some=lambda some: True)


def test_some_is_empty():
    from category import Some

    assert False is Some[int](0).is_empty()


def test_some_not_empty():
    from category import Some

    assert True is Some[int](0).not_empty()


def test_some_get():
    from category import Some

    assert 0 == Some[int](0).get()


def test_some_get_or_else():
    from category import Some

    assert 0 == Some[int](0).get_or_else(lambda: 1)


def test_some_method():
    from category import VOID, Option, Some, Void

    def to_void(self: Option[int], /) -> Void[int]:
        if isinstance(self.pattern, Void):
            return self.pattern
        else:
            return VOID

    def to_some(self: Option[int], /) -> Some[int]:
        if isinstance(self.pattern, Void):
            return Some[int](0)
        else:
            return self.pattern

    assert Void is type(Some[int](1).method(to_void))
    assert Some is type(Some[int](1).method(to_some))
