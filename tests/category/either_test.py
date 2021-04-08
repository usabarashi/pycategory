def test_left():
    from category import Left

    assert Left is type(Left[int, None](value=0))
    assert False is bool(Left[int, None](value=0))
    assert True is Left[int, None](value=0).is_left()
    assert False is Left[int, None](value=0).is_right()


def test_left_leftprojecton():
    from category import Left, LeftProjection

    assert LeftProjection is type(Left[int, None](value=0).left())
    assert False is bool(Left[int, None](value=0).left())


def test_left_leftprojection_get():
    from category import Left, Right

    assert 0 == Left[int, None](value=0).left().get()
    assert 0 == Left[int, None](value=0).left().get_or_else(default=lambda: 0)
    try:
        Right[int, None](value=None).left().get()
        assert False
    except Exception as error:
        ValueError is type(error)
    assert 0 == Right[int, None](value=None).left().get_or_else(default=lambda: 0)


def test_left_rightprojecton():
    from category import Left, RightProjection

    assert RightProjection is type(Left[int, None](value=0).right())
    assert False is bool(Left[int, None](value=0).right())


def test_left_rightprojecton_get():
    from category import Left

    try:
        Left[int, None](value=0).right().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is Left[int, None](value=0).right().get_or_else(default=lambda: None)


def test_left_map():
    from category import Left, LeftProjection, RightProjection

    assert Left is type(Left[int, None](0).map(functor=lambda right: right))
    assert LeftProjection is type(
        Left[int, None](0).map(functor=lambda right: right).left()
    )
    assert 0 == Left[int, None](0).map(functor=lambda right: right).left().get()
    assert 0 == Left[int, None](0).map(functor=lambda right: right).left().get_or_else(
        default=lambda: 0
    )
    assert RightProjection is type(
        Left[int, None](value=0).map(functor=lambda right: right).right()
    )
    try:
        Left[int, None](value=0).map(functor=lambda right: right).right().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    None is Left[int, None](value=0).map(
        functor=lambda right: right
    ).right().get_or_else(default=lambda: None)


def test_left_faltmap():
    from category import Left, LeftProjection, RightProjection

    assert Left is type(
        Left[int, None](value=0).flatmap(functor=lambda right: Left[int, None](value=0))
    )
    assert LeftProjection is type(
        Left[int, None](value=0)
        .flatmap(functor=lambda right: Left[int, None](value=0))
        .left()
    )
    assert (
        0
        == Left[int, None](value=0)
        .flatmap(functor=lambda right: Left[int, None](value=1))
        .left()
        .get()
    )
    assert 0 == Left[int, None](value=0).flatmap(
        functor=lambda right: Left[int, None](value=1)
    ).left().get_or_else(default=lambda: 0)
    assert RightProjection is type(
        Left[int, None](value=0)
        .flatmap(functor=lambda right: Left[int, None](value=1))
        .right()
    )
    try:
        Left[int, None](value=0).flatmap(
            functor=lambda right: Left[int, None](value=1)
        ).right().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is Left[int, None](value=0).flatmap(
        functor=lambda none: Left[int, None](value=1)
    ).right().get_or_else(default=lambda: None)


def test_right():
    from category import Right

    assert Right is type(Right[None, int](value=0))
    assert True is bool(Right[None, int](value=0))
    assert False is Right[None, int](value=0).is_left()
    assert True is Right[None, int](value=0).is_right()


def test_right_rightprojecton():
    from category import Right, RightProjection

    assert RightProjection is type(Right[None, int](value=0).right())
    assert True is bool(Right[None, int](value=0).right())


def test_right_rightprojection_get():
    from category import Right

    assert 0 == Right[None, int](value=0).right().get()
    assert 0 == Right[None, int](value=0).right().get_or_else(default=lambda: 0)


def test_right_leftprojecton():
    from category import LeftProjection, Right

    assert LeftProjection is type(Right[None, int](value=0).left())
    assert True is bool(Right[None, int](value=0).left())


def test_right_leftprojecton_get():
    from category import Right

    try:
        Right[None, int](value=0).left().get()
    except ValueError:
        assert True
    except Exception:
        assert False
    assert None is Right[None, int](value=0).left().get_or_else(default=lambda: None)


def test_right_map():
    from category import LeftProjection, Right, RightProjection

    assert Right is type(Right[None, int](value=0).map(functor=lambda right: right))
    assert RightProjection is type(
        Right[None, int](value=0).map(functor=lambda right: right).right()
    )
    assert 0 == Right[None, int](value=0).map(functor=lambda right: right).right().get()
    assert 0 == Right[None, int](value=0).map(
        functor=lambda right: right
    ).right().get_or_else(default=lambda: 0)
    assert LeftProjection is type(
        Right[None, int](value=0).map(functor=lambda right: right).left()
    )
    try:
        Right[None, int](value=0).map(functor=lambda right: right).left().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is Right[None, int](value=0).map(
        functor=lambda right: right
    ).left().get_or_else(default=lambda: None)


def test_right_flatmap():
    from category import LeftProjection, Right, RightProjection

    assert Right is type(
        Right[None, int](value=0).flatmap(
            functor=lambda right: Right[None, int](value=right + 1)
        )
    )
    assert RightProjection is type(
        Right[None, int](value=0)
        .map(functor=lambda right: Right[None, int](value=right + 1))
        .right()
    )
    assert (
        1
        == Right[None, int](value=0)
        .flatmap(functor=lambda right: Right[None, int](value=right + 1))
        .right()
        .get()
    )
    1 == Right[None, int](value=0).flatmap(
        functor=lambda right: Right[None, int](value=right + 1)
    ).right().get()
    assert LeftProjection is type(
        Right[None, int](value=0)
        .flatmap(functor=lambda right: Right[None, int](value=right + 1))
        .left()
    )
    try:
        Right[None, int](value=0).flatmap(
            functor=lambda right: Right[None, int](value=right + 1)
        ).left().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is Right[None, int](value=0).map(
        functor=lambda right: Right[None, int](value=right + 1)
    ).left().get_or_else(default=lambda: None)


def test_fold():
    from category import Left, Right

    assert None is Left[None, int](value=None).fold(
        left=lambda left: None, right=lambda right: None
    )
    assert None is Right[None, int](value=0).fold(
        left=lambda left: None, right=lambda right: None
    )


def test_either_do():
    from category import Either, EitherDo, Left, Right

    @Either.do
    def left_context() -> EitherDo[Exception, int]:
        one = yield from Right[Exception, int](value=1)()
        two = 2
        three = yield from Left[Exception, int](value=Exception())()
        return one + two + three

    assert Exception is type(left_context().left().get())
    assert False is bool(left_context())
    assert True is left_context().is_left()
    assert False is left_context().is_right()
    assert type(Left[Exception, int](value=Exception()).left().get()) is type(
        left_context().left().get()
    )
    assert None is left_context().fold(left=lambda left: None, right=lambda right: None)

    @Either.do
    def left_convert_context() -> EitherDo[Exception, int]:
        one = yield from Right[Exception, int](value=1)()
        two = 2
        three = yield from Left[Exception, int](value=Exception())(
            convert=lambda left: Left[Exception, int](value=ValueError())
        )
        return one + two + three

    assert ValueError is type(left_convert_context().left().get())
    assert False is bool(left_convert_context())
    assert True is left_convert_context().is_left()
    assert False is left_convert_context().is_right()
    assert type(Left[Exception, int](value=ValueError()).left().get()) is type(
        left_convert_context().left().get()
    )
    assert None is left_convert_context().fold(
        left=lambda left: None, right=lambda right: None
    )

    @Either.do
    def right_context() -> EitherDo[None, int]:
        one = yield from Right[None, int](1)()
        two = 2
        three = yield from Right[None, int](3)()
        return one + two + three

    assert 6 == right_context().right().get()
    assert True is bool(right_context())
    assert False is right_context().is_left()
    assert True is right_context().is_right()
    assert Right[None, int](value=6) == right_context()
    assert None is right_context().fold(
        left=lambda left: None, right=lambda right: None
    )

    @Either.do
    def right_convert_context() -> EitherDo[None, int]:
        one = yield from Right[None, int](value=1)()
        two = 2
        three = yield from Right[None, int](value=3)(
            convert=lambda right: Right[None, int](value=3)
        )
        return one + two + three

    try:
        right_convert_context().right().get()
        assert False
    except BaseException as error:
        GeneratorExit is type(error)


def test_convert():
    from category import Either, Left, Right

    def to_left(either: Either[Exception, int]) -> Left[Exception, int]:
        if isinstance(either.pattern, Left):
            return either.pattern
        else:
            return Left[Exception, int](value=Exception())

    def to_right(either: Either[Exception, int]) -> Right[Exception, int]:
        if isinstance(either.pattern, Left):
            return Right[Exception, int](value=1)
        else:
            return either.pattern

    assert Left is type(Left[Exception, int](value=Exception()).convert(to_left))
    assert Right is type(Left[Exception, int](value=Exception()).convert(to_right))
    assert Left is type(Right[Exception, int](value=1).convert(to_left))
    assert Right is type(Right[Exception, int](value=1).convert(to_right))
