def test_left():
    from category.either import Left

    assert Left is type(Left[int, None](0))


def test_left_leftprojecton():
    from category.either import Left, LeftProjection

    assert Left is type(Left[int, None](0))
    assert LeftProjection is type(Left[int, None](0).left())


def test_left_leftprojection_get():
    from category.either import Left

    assert 0 == Left[int, None](0).left().get()
    assert 0 == Left[int, None](0).left().get(else_then=lambda: Exception())


def test_left_rightprojecton():
    from category.either import Left, RightProjection

    assert RightProjection is type(Left[int, None](0).right())


def test_left_rightprojecton_get():
    from category.either import Left

    try:
        Left[int, None](0).right().get()
    except Exception as error:
        assert ValueError is type(error)
    assert Exception is type(
        Left[int, None](0).right().get(else_then=lambda: Exception())
    )


def test_left_map():
    from category.either import Left, LeftProjection, RightProjection

    assert Left is type(Left[int, None](0).map(functor=lambda none: none))
    assert LeftProjection is type(
        Left[int, None](0).map(functor=lambda none: none).left()
    )
    assert 0 == Left[int, None](0).map(functor=lambda none: none).left().get()
    assert 0 == Left[int, None](0).map(functor=lambda none: none).left().get(
        else_then=lambda: Exception()
    )
    assert RightProjection is type(
        Left[int, None](0).map(functor=lambda none: none).right()
    )
    try:
        Left[int, None](0).map(functor=lambda none: none).right().get()
    except Exception as error:
        assert ValueError is type(error)
    assert Exception is type(
        Left[int, None](0)
        .map(functor=lambda none: none)
        .right()
        .get(else_then=lambda: Exception())
    )


def test_left_faltmap():
    from category.either import Left, LeftProjection, RightProjection

    assert Left is type(
        Left[int, None](0).flatmap(functor=lambda none: Left[int, None](value=1))
    )
    assert LeftProjection is type(
        Left[int, None](0).flatmap(functor=lambda none: Left[int, None](value=1)).left()
    )
    assert (
        0
        == Left[int, None](0)
        .flatmap(functor=lambda none: Left[int, None](value=1))
        .left()
        .get()
    )
    assert 0 == Left[int, None](0).flatmap(
        functor=lambda none: Left[int, None](value=1)
    ).left().get(else_then=lambda: Exception())
    assert RightProjection is type(
        Left[int, None](0)
        .flatmap(functor=lambda none: Left[int, None](value=1))
        .right()
    )
    try:
        Left[int, None](0).flatmap(
            functor=lambda none: Left[int, None](value=1)
        ).right().get()
    except Exception as error:
        assert ValueError is type(error)
    assert Exception is type(
        Left[int, None](0)
        .flatmap(functor=lambda none: Left[int, None](value=1))
        .right()
        .get(else_then=lambda: Exception())
    )


def test_right():
    from category.either import Right

    assert Right is type(Right[None, int](0))


def test_right_rightprojecton():
    from category.either import Right, RightProjection

    assert Right is type(Right[None, int](0))
    assert RightProjection is type(Right[None, int](0).right())


def test_right_rightprojection_get():
    from category.either import Right

    assert 0 == Right[None, int](0).right().get()
    assert 0 == Right[None, int](0).right().get(else_then=lambda: Exception())


def test_right_leftprojecton():
    from category.either import LeftProjection, Right

    assert LeftProjection is type(Right[None, int](0).left())


def test_right_leftprojecton_get():
    from category.either import Right

    try:
        Right[None, int](0).left().get()
    except Exception as error:
        assert ValueError is type(error)
    assert Exception is type(
        Right[None, int](0).left().get(else_then=lambda: Exception())
    )


def test_right_map():
    from category.either import LeftProjection, Right, RightProjection

    assert Right is type(Right[None, int](0).map(functor=lambda none: none))
    assert RightProjection is type(
        Right[None, int](0).map(functor=lambda none: none).right()
    )
    assert 0 == Right[None, int](0).map(functor=lambda none: none).right().get()
    assert 0 == Right[None, int](0).map(functor=lambda none: none).right().get(
        else_then=lambda: Exception()
    )
    assert LeftProjection is type(
        Right[None, int](0).map(functor=lambda none: none).left()
    )
    try:
        Right[None, int](0).map(functor=lambda none: none).left().get()
    except Exception as error:
        assert ValueError is type(error)
    assert Exception is type(
        Right[None, int](0)
        .map(functor=lambda none: none)
        .left()
        .get(else_then=lambda: Exception())
    )


def test_right_flatmap():
    from category.either import LeftProjection, Right, RightProjection

    assert Right is type(
        Right[None, int](0).flatmap(
            functor=lambda integer: Right[None, int](value=integer + 1)
        )
    )
    assert RightProjection is type(
        Right[None, int](0)
        .map(functor=lambda integer: Right[None, int](value=integer + 1))
        .right()
    )
    assert (
        1
        == Right[None, int](0)
        .flatmap(functor=lambda integer: Right[None, int](value=integer + 1))
        .right()
        .get()
    )
    assert 1 == Right[None, int](0).flatmap(
        functor=lambda integer: Right[None, int](value=integer + 1)
    ).right().get(else_then=lambda: Exception())
    assert LeftProjection is type(
        Right[None, int](0)
        .flatmap(functor=lambda integer: Right[None, int](value=integer + 1))
        .left()
    )
    try:
        Right[None, int](0).flatmap(
            functor=lambda integer: Right[None, int](value=integer + 1)
        ).left().get()
    except Exception as error:
        assert ValueError is type(error)
    assert Exception is type(
        Right[None, int](0)
        .map(functor=lambda integer: Right[None, int](value=integer + 1))
        .left()
        .get(else_then=lambda: Exception())
    )


def test_either_do():
    from typing import Any, Generator

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
    assert (
        Left[int, int](0).value
        == left_context()
        .fold(left=lambda value: 0, right=lambda value: value * 2)
        .value
    )

    @Either.do
    def right_context() -> Generator[Any, Any, int]:
        one = yield from Right[None, int](1)()
        two = 2
        three = yield from Right[None, int](3)()
        return one + two + three

    assert 6 == right_context().right().get()
    assert True is bool(right_context())
    assert False is right_context().is_left()
    assert True is right_context().is_right()
    assert Right[None, int](6) == right_context()
    assert Right[None, int](12) == right_context().fold(
        left=lambda value: 0, right=lambda value: value * 2
    )
