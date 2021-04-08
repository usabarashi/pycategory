def test_void():
    from category import Void

    assert Void is type(Void[int]())
    assert False is bool(Void[int]())
    try:
        Void[int]().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    try:
        Void[int]().get_or_else()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is Void[int]().get_or_else(default=lambda: None)
    assert True is Void[int]().is_empty()
    assert False is Void[int]().not_empty()


def test_void_map():
    from category import Void

    assert Void is type(Void[int]().map(functor=lambda some: None))
    assert False is bool(Void[int]().map(functor=lambda some: None))
    try:
        Void[int]().map(functor=lambda some: None).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    try:
        Void[int]().map(functor=lambda some: None).get_or_else()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is Void[int]().map(functor=lambda some: None).get_or_else(
        default=lambda: None
    )
    assert True is Void[int]().map(functor=lambda some: None).is_empty()
    assert False is Void[int]().map(functor=lambda some: None).not_empty()


def test_void_flatmap():
    from category import Some, Void

    assert Void is type(Void[int]().flatmap(functor=lambda some: Some[int](value=0)))
    assert False is bool(Void[int]().flatmap(functor=lambda some: Some[int](value=0)))
    try:
        Void[int]().flatmap(functor=lambda some: Some[int](value=0)).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    try:
        Void[int]().flatmap(functor=lambda some: Some[int](value=0)).get_or_else()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is Void[int]().flatmap(
        functor=lambda some: Some[int](value=0)
    ).get_or_else(default=lambda: None)
    assert (
        True is Void[int]().flatmap(functor=lambda some: Some[int](value=0)).is_empty()
    )
    assert (
        False
        is Void[int]().flatmap(functor=lambda some: Some[int](value=0)).not_empty()
    )


def test_some():
    from category import Some

    assert Some is type(Some[int](value=0))
    assert True is bool(Some[int](value=0))
    assert 0 == Some[int](value=0).get()
    assert 0 == Some[int](value=0).get_or_else()
    assert 0 == Some[int](value=0).get_or_else(default=lambda: None)
    assert False is Some[int](value=0).is_empty()
    assert True is Some[int](value=0).not_empty()


def test_some_map():
    from category import Some

    assert Some is type(Some[int](value=0).map(functor=lambda some: some + 1))
    assert True is bool(Some[int](value=0).map(functor=lambda some: some + 1))
    assert 1 == Some[int](value=0).map(functor=lambda some: some + 1).get()
    assert 1 == Some[int](value=0).map(functor=lambda some: some + 1).get_or_else()
    assert 1 == Some[int](value=0).map(functor=lambda some: some + 1).get_or_else(
        default=lambda: None
    )
    assert False is Some[int](value=0).map(functor=lambda some: some + 1).is_empty()
    assert (
        True is Some[int](value=0).map(functor=lambda integer: integer + 1).not_empty()
    )


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
    assert (
        1
        == Some[int](value=0)
        .flatmap(functor=lambda some: Some[int](value=some + 1))
        .get_or_else()
    )
    assert 1 == Some[int](value=0).flatmap(
        functor=lambda some: Some[int](value=some + 1)
    ).get_or_else(default=lambda: None)
    assert (
        False
        is Some[int](value=0)
        .flatmap(functor=lambda some: Some[int](value=some + 1))
        .is_empty()
    )
    assert (
        True
        is Some[int](value=0)
        .flatmap(functor=lambda some: Some[int](value=some + 1))
        .not_empty()
    )


def test_option_fold():
    from category import Some, Void

    try:
        assert (
            None
            is Void[int]()
            .fold(void=lambda: Void[int](), some=lambda some: Some(value=some + 1))
            .get()
        )
        assert False
    except Exception as error:
        assert ValueError is type(error)
    try:
        assert (
            None
            is Void[int]()
            .fold(void=lambda: Void[int](), some=lambda some: Some[int](value=some + 1))
            .get_or_else()
        )
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is Void[int]().fold(
        void=lambda: Void[int](), some=lambda some: Some[int](value=some + 1)
    ).get_or_else(default=lambda: None)
    assert (
        1
        == Some[int](value=0)
        .fold(void=lambda: Void[int](), some=lambda some: Some[int](value=some + 1))
        .get_or_else()
    )
    assert 1 == Some[int](value=0).fold(
        void=lambda: Void[int](), some=lambda some: Some[int](value=some + 1)
    ).get_or_else(default=lambda: None)


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


def test_convert():
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
    assert Void is type(Some[int](value=1).convert(to_void))
    assert Some is type(Some[int](value=1).convert(to_some))
