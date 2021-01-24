from typing import Any, Generator

from category import Either, Left, Right


def test_either():
    assert 0 == Left[int, Any](0).value
    assert 0 == Right[Any, int](0).value
    assert False is bool(Left[int, Any](0))
    assert True is bool(Right[Any, int](0))
    assert True is Left[int, Any](0).is_left()
    assert False is Left[int, Any](0).is_right()
    assert False is Right[Any, int](0).is_left()
    assert True is Right[Any, int](0).is_right()
    assert Left(0) == Left[int, Any](0)()
    assert 0 == Right[Any, int](0)()


def test_either_do():
    @Either.do
    def left_context() -> Generator[Either[None, int], Any, int]:
        one = yield Right[None, int](1)()
        two = 2
        three = yield Left[None, int](None)()
        return one + two + three

    assert None is left_context().value
    assert False is bool(left_context())
    assert True is left_context().is_left()
    assert False is left_context().is_right()
    assert Left[None, int](None) == left_context()
    assert Left[None, int](None) == left_context().map(lambda value: value * 2)
    assert Left[int, int](0) == left_context().fold(
        left=lambda value: 0, right=lambda value: value * 2
    )

    @Either.do
    def right_context() -> Generator[Either[None, int], Any, int]:
        one = yield Right[None, int](1)()
        two = 2
        three = yield Right[None, int](3)()
        return one + two + three

    assert 6 == right_context().value
    assert True is bool(right_context())
    assert False is right_context().is_left()
    assert True is right_context().is_right()
    assert Right[None, int](6) == right_context()
    assert Right[None, int](12) == right_context().map(lambda value: value * 2)
    assert Right[None, int](12) == right_context().fold(
        left=lambda value: 0, right=lambda value: value * 2
    )
