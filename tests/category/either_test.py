def test_either_do():
    from category import EitherDo, Left, Monad, Right, Some, Success

    @Monad.do
    def safe_context() -> EitherDo[IndexError | KeyError, int]:
        _ = yield from Right[IndexError, bool](True)
        one = yield from Right[IndexError, int](1)
        two = 2
        three = yield from Right[KeyError, int](3)
        _ = yield from Right[IndexError, bool](False)
        _ = yield from Right[KeyError, bool](False)
        return one + two + three

    assert 6 == safe_context().get()

    @Monad.do
    def outside_context() -> EitherDo[IndexError | KeyError, int]:
        _ = yield from Right[IndexError, bool](True)
        one = yield from Right[IndexError, int](1)
        two = 2
        three = yield from Right[KeyError, int](3)
        _ = yield from Right[IndexError, bool](False)
        _ = yield from Right[KeyError, bool](False)
        _ = yield from Some[int](42)  # Outside
        _ = yield from Success[int](42)  # Outside
        _ = yield from Right[ValueError, int](42)  # Outside
        _ = yield from Right[TypeError, int](42)  # Outside
        return str(one + two + three)  # Outside

    try:
        outside_context().get()
        assert False
    except Exception as error:
        assert TypeError is type(error)

    @Monad.do
    def left_context() -> EitherDo[Exception, int]:
        one = yield from Right[Exception, int](1)
        two = 2
        three = yield from Left[Exception, int](Exception())
        return one + two + three

    assert Exception is type(left_context().left().get())
    assert True is left_context().is_left()
    assert False is left_context().is_right()
    assert type(Left[Exception, int](Exception()).left().get()) is type(
        left_context().left().get()
    )
    assert None is left_context().fold(left=lambda left: None, right=lambda right: None)

    @Monad.do
    def right_context() -> EitherDo[None, int]:
        one = yield from Right[None, int](1)
        two = 2
        three = yield from Right[None, int](3)
        return one + two + three

    assert 6 == right_context().right().get()
    assert False is right_context().is_left()
    assert True is right_context().is_right()
    assert Right is type(right_context())
    assert None is right_context().fold(
        left=lambda left: None, right=lambda right: None
    )
    assert 6 == right_context().get()


def test_left():
    from category import Left

    assert Left is type(Left[int, None](42))
    assert Left is type(eval(f"{Left[int, None](42)}"))


def test_left_map():
    from category import Left, LeftProjection, RightProjection

    left = Left[int, None](0)
    mapped_left = left.map(lambda right: right)
    assert left is mapped_left
    assert Left is type(mapped_left)
    assert LeftProjection is type(mapped_left.left())
    assert 0 == mapped_left.left().get()
    assert 0 == mapped_left.left().get_or_else(lambda: 1)
    assert RightProjection is type(mapped_left.right())
    try:
        mapped_left.right().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is mapped_left.right().get_or_else(lambda: None)


def test_left_flat_map():
    from category import Left, LeftProjection, RightProjection

    left = Left[int, None](0)
    flat_mapped_left = left.flat_map(lambda right: Left[int, None](0))
    assert left is flat_mapped_left
    assert Left is type(flat_mapped_left)
    assert LeftProjection is type(flat_mapped_left.left())
    assert 0 == flat_mapped_left.left().get()
    assert 0 == left.flat_map(lambda right: Left[int, None](1)).left().get_or_else(
        lambda: 1
    )
    assert RightProjection is type(flat_mapped_left.right())
    try:
        flat_mapped_left.right().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is flat_mapped_left.right().get_or_else(lambda: None)


def test_left_to_option():
    from category import Left, Void

    assert Void() is Left[None, int](None).to_option


def test_left_to_try():
    from category import Failure, Left, SubtypeConstraints

    assert Failure is type(
        Left[TypeError, int](TypeError()).to_try(
            SubtypeConstraints(TypeError, Exception)
        )
    )
    try:
        Left[bool, int](False).to_try(SubtypeConstraints(bool, Exception))
        assert False
    except TypeError:
        assert True


def test_left_fold():
    from category import Left

    assert None is Left[None, int](None).fold(
        left=lambda left: None, right=lambda right: None
    )


def test_left_leftprojecton():
    from category import Left, LeftProjection

    assert LeftProjection is type(eval(f"{Left[int, None](42).left()}"))
    assert LeftProjection is type(eval(f"{Left[int, None](42).left()}"))


def test_left_leftprojection_get():
    from category import Left, Right

    assert 0 == Left[int, None](0).left().get()
    assert 0 == Left[int, None](0).left().get_or_else(lambda: 0)
    try:
        Right[int, None](None).left().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert 0 == Right[int, None](None).left().get_or_else(lambda: 0)


def test_left_rightprojecton():
    from category import Left, RightProjection

    assert RightProjection is type(Left[int, None](0).right())


def test_left_rightprojecton_get():
    from category import Left

    try:
        Left[int, None](0).right().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is Left[int, None](0).right().get_or_else(lambda: None)


def test_left_is_left():
    from category import Left

    assert True is Left[Exception, int](Exception()).is_left()


def test_left_is_right():
    from category import Left

    assert False is Left[Exception, int](Exception()).is_right()


def test_left_get():
    from category import Left

    try:
        Left[Exception, int](Exception()).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)


def test_left_get_or_else():
    from category import Left

    assert False is Left[Exception, int](Exception()).get_or_else(lambda: False)


def test_left_method():
    from category import Either, Left, Right

    def to_left(self: Either[Exception, int]) -> Left[Exception, int]:
        match self.pattern:
            case Left():
                return self.pattern
            case Right():
                return Left[Exception, int](Exception())

    def to_right(self: Either[Exception, int]) -> Right[Exception, int]:
        match self.pattern:
            case Left():
                return Right[Exception, int](1)
            case Right():
                return self.pattern

    assert Left is type(Left[Exception, int](Exception()).method(to_left))
    assert Right is type(Left[Exception, int](Exception()).method(to_right))


def test_right():
    from category import Right

    assert Right is type(Right[None, int](42))
    assert Right is type(eval(f"{Right[None, int](42)}"))


def test_right_map():
    from category import LeftProjection, Right, RightProjection

    right = Right[None, int](0)
    mapped_right = right.map(lambda right: right)
    assert right is not mapped_right
    assert Right is type(mapped_right)
    assert RightProjection is type(mapped_right.right())
    assert 0 == mapped_right.right().get()
    assert 0 == mapped_right.right().get_or_else(lambda: 0)
    assert LeftProjection is type(mapped_right.left())
    try:
        mapped_right.left().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is mapped_right.left().get_or_else(lambda: None)


def test_right_flat_map():
    from category import LeftProjection, Right, RightProjection

    right = Right[None, int](0)
    flat_mapped_right = right.flat_map(lambda right: Right[None, int](right + 1))
    assert right is not flat_mapped_right
    assert Right is type(flat_mapped_right)
    assert RightProjection is type(flat_mapped_right.right())
    assert 1 == flat_mapped_right.right().get()
    assert LeftProjection is type(flat_mapped_right.left())
    try:
        flat_mapped_right.left().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is flat_mapped_right.left().get_or_else(lambda: None)


def test_right_to_option():
    from category import Right, Some

    assert Some is type(Right[None, int](42).to_option)
    assert 42 == Right[None, int](42).to_option.get_or_else(lambda: 0)


def test_right_to_try():
    from category import Right, SubtypeConstraints, Success

    assert Success is type(
        Right[TypeError, int](42).to_try(SubtypeConstraints(TypeError, Exception))
    )
    assert 42 == Right[TypeError, int](42).to_try(
        SubtypeConstraints(TypeError, Exception)
    ).get_or_else(lambda: 0)


def test_right_fold():
    from category import Left, Right

    assert None is Left[None, int](None).fold(
        left=lambda left: None, right=lambda right: None
    )
    assert None is Right[None, int](0).fold(
        left=lambda left: None, right=lambda right: None
    )


def test_right_rightprojecton():
    from category import Right, RightProjection

    assert RightProjection is type(Right[None, int](42).right())
    assert RightProjection is type(eval(f"{Right[None, int](42).right()}"))


def test_right_rightprojection_get():
    from category import Right

    assert 0 == Right[None, int](0).right().get()
    assert 0 == Right[None, int](0).right().get_or_else(lambda: 0)


def test_right_leftprojecton():
    from category import LeftProjection, Right

    assert LeftProjection is type(Right[None, int](0).left())


def test_right_leftprojecton_get():
    from category import Right

    try:
        Right[None, int](0).left().get()
    except ValueError:
        assert True
    except Exception:
        assert False
    assert None is Right[None, int](0).left().get_or_else(lambda: None)


def test_right_is_left():
    from category import Right

    assert False is Right[Exception, int](1).is_left()


def test_right_is_right():
    from category import Right

    assert True is Right[Exception, int](1).is_right()


def test_right_get():
    from category import Right

    assert 1 == Right[Exception, int](1).get()


def test_right_get_or_else():
    from category import Right

    assert 1 == Right[Exception, int](1).get_or_else(lambda: False)


def test_right_method():
    from category import Either, Left, Right

    def to_left(either: Either[Exception, int]) -> Left[Exception, int]:
        match either.pattern:
            case Left():
                return either.pattern
            case _:
                return Left[Exception, int](Exception())

    def to_right(either: Either[Exception, int]) -> Right[Exception, int]:
        match either.pattern:
            case Left():
                return Right[Exception, int](1)
            case _:
                return either.pattern

    assert Left is type(Right[Exception, int](1).method(to_left))
    assert Right is type(Right[Exception, int](1).method(to_right))


def test_dataclass():
    from dataclasses import asdict, dataclass
    from typing import cast

    from category import Left, Right

    @dataclass(frozen=True)
    class AsDict:
        left: Left[None, int]
        right: Right[None, int]

    dict_data = asdict(AsDict(left=Left[None, int](None), right=Right[None, int](42)))
    assert Left is type(dict_data.get("left", None))
    assert None is cast(Left[None, int], dict_data.get("left", None)).left().get()
    assert Right is type(dict_data.get("right", None))
    assert 42 == cast(Right[None, int], dict_data.get("right", None)).get()


def test_pattern_match():
    from typing import cast

    from category import Either, Left, Right

    match cast(Either[None, int], Left[None, int](None)):
        case Left(None):
            assert True
        case _:
            assert False

    match cast(Either[None, int], Right[None, int](42)):
        case Right(42):
            assert True
        case _:
            assert False

    match cast(
        Either[IndexError | KeyError, int],
        Left[IndexError | KeyError, int](KeyError()),
    ):
        case Left(error) if isinstance(error, IndexError):
            assert False
        case Left(error) if isinstance(error, KeyError):
            assert True
        case Right():
            assert False
        case _:
            assert False

    match cast(Either[None, int], Left[None, int](None)), cast(
        Either[None, int], Left[None, int](None)
    ):
        case Left(x), Left(y) if x is y:
            assert True
        case _:
            assert False

    match cast(Either[None, int], Right[None, int](41)), cast(
        Either[None, int], Right[None, int](42)
    ):
        case Right(x), Right(y) if x < y:
            assert True
        case _:
            assert False
