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
    assert 6 == right_context().get()


def test_left():
    from category import Left

    assert Left is type(Left[int, None](value=0))
    assert False is bool(Left[int, None](value=0))


def test_left_map():
    from category import Left, LeftProjection, RightProjection

    left = Left[int, None](0)
    mapped_left = left.map(functor=lambda right: right)
    assert left is not mapped_left
    assert Left is type(mapped_left)
    assert LeftProjection is type(mapped_left.left())
    assert 0 == mapped_left.left().get()
    assert 0 == mapped_left.left().get_or_else(default=lambda: 0)
    assert RightProjection is type(mapped_left.right())
    try:
        mapped_left.right().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    None is mapped_left.right().get_or_else(default=lambda: None)


def test_left_faltmap():
    from category import Left, LeftProjection, RightProjection

    left = Left[int, None](value=0)
    flatmapped_left = left.flatmap(functor=lambda right: Left[int, None](value=0))
    assert left is not flatmapped_left
    assert Left is type(flatmapped_left)
    assert LeftProjection is type(flatmapped_left.left())
    assert 0 == flatmapped_left.left().get()
    assert 0 == left.flatmap(
        functor=lambda right: Left[int, None](value=1)
    ).left().get_or_else(default=lambda: 0)
    assert RightProjection is type(flatmapped_left.right())
    try:
        flatmapped_left.right().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is flatmapped_left.right().get_or_else(default=lambda: None)


def test_left_fold():
    from category import Left

    assert None is Left[None, int](value=None).fold(
        left=lambda left: None, right=lambda right: None
    )


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


def test_left_is_left():
    from category import Left

    assert True is Left[Exception, int](value=Exception()).is_left()


def test_left_is_right():
    from category import Left

    assert False is Left[Exception, int](value=Exception()).is_right()


def test_left_get():
    from category import Left

    try:
        Left[Exception, int](value=Exception()).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)


def test_left_get_or_else():
    from category import Left

    assert False is Left[Exception, int](value=Exception()).get_or_else(
        default=lambda: False
    )


def test_left_method():
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

    assert Left is type(Left[Exception, int](value=Exception()).method(to_left))
    assert Right is type(Left[Exception, int](value=Exception()).method(to_right))


def test_right():
    from category import Right

    assert Right is type(Right[None, int](value=0))
    assert True is bool(Right[None, int](value=0))


def test_right_map():
    from category import LeftProjection, Right, RightProjection

    right = Right[None, int](value=0)
    mapped_right = right.map(functor=lambda right: right)
    assert right is not mapped_right
    assert Right is type(mapped_right)
    assert RightProjection is type(mapped_right.right())
    assert 0 == mapped_right.right().get()
    assert 0 == mapped_right.right().get_or_else(default=lambda: 0)
    assert LeftProjection is type(mapped_right.left())
    try:
        mapped_right.left().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is mapped_right.left().get_or_else(default=lambda: None)


def test_right_flatmap():
    from category import LeftProjection, Right, RightProjection

    right = Right[None, int](value=0)
    flatmapped_right = right.flatmap(
        functor=lambda right: Right[None, int](value=right + 1)
    )
    assert right is not flatmapped_right
    assert Right is type(flatmapped_right)
    assert RightProjection is type(flatmapped_right.right())
    assert 1 == flatmapped_right.right().get()
    assert LeftProjection is type(flatmapped_right.left())
    try:
        flatmapped_right.left().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is flatmapped_right.left().get_or_else(default=lambda: None)


def test_right_fold():
    from category import Left, Right

    assert None is Left[None, int](value=None).fold(
        left=lambda left: None, right=lambda right: None
    )
    assert None is Right[None, int](value=0).fold(
        left=lambda left: None, right=lambda right: None
    )


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


def test_right_is_left():
    from category import Right

    assert False is Right[Exception, int](value=1).is_left()


def test_right_is_right():
    from category import Right

    assert True is Right[Exception, int](value=1).is_right()


def test_right_get():
    from category import Right

    assert 1 == Right[Exception, int](value=1).get()


def test_right_get_or_else():
    from category import Right

    assert 1 == Right[Exception, int](value=1).get_or_else(default=lambda: False)


def test_right_method():
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

    assert Left is type(Right[Exception, int](value=1).method(to_left))
    assert Right is type(Right[Exception, int](value=1).method(to_right))
