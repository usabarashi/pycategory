from typing import Any, Generator

from category import Either, Failure, Left, Right, Success, Try


def test_try():
    assert isinstance(Failure(Exception()).value, Exception)
    assert isinstance(Failure(ValueError()).value, Exception)
    assert 0 == Success(0).value
    assert True is bool(Success(0))
    assert False is bool(Failure(Exception()))
    assert True is Success(0).is_success()
    assert False is Success(0).is_failure()
    assert False is Failure(Exception()).is_success()
    assert True is Failure(Exception()).is_failure()

    assert 0 == Success(0)()
    assert isinstance(Failure(Exception())(), Failure)
    assert isinstance(Failure(Exception())().value, Exception)


def test_try_hold():
    @Try.hold
    def multi_context(value: int) -> int:
        if not value:
            raise Exception("error")
        return value

    assert isinstance(multi_context(0), Failure)
    assert isinstance(multi_context(0).value, Exception)
    assert isinstance(multi_context(1), Success)
    assert 1 == multi_context(1).value
    assert False is bool(multi_context(0))
    assert True is bool(multi_context(1))
    assert True is multi_context(0).is_failure()
    assert False is multi_context(0).is_success()
    assert False is multi_context(1).is_failure()
    assert True is multi_context(1).is_success()


def test_try_do():
    @Try.do
    def failure_context() -> Generator[Try[int], Any, int]:
        one = yield Success(1)()
        two = 2
        three = yield Failure(ValueError())()
        return one + two + three

    assert isinstance(failure_context(), Failure)
    assert isinstance(failure_context().value, Exception)
    assert False is bool(failure_context())
    assert False is failure_context().is_success()
    assert True is failure_context().is_failure()
    assert isinstance(
        failure_context().fold(
            failure=lambda value: EOFError(), success=lambda value: value * 2
        ),
        Failure,
    )

    @Try.do
    def success_context() -> Generator[Try[int], Any, int]:
        one = yield Success(1)()
        two = 2
        three = yield Success(3)()
        return one + two + three

    assert Success(6) == success_context()
    assert 6 == success_context().value
    assert True is bool(success_context())
    assert True is success_context().is_success()
    assert False is success_context().is_failure()
    assert Success[int](12) == success_context().fold(
        failure=lambda value: ValueError(), success=lambda value: value * 2
    )

    @Try.hold
    def multi_context(value: int) -> int:
        if not value:
            raise Exception("error")
        return value

    @Try.do
    def mix_failure_context() -> Generator[Try[int], Any, int]:
        success = yield multi_context(1)()
        _ = yield multi_context(0)()
        return success

    assert isinstance(mix_failure_context(), Failure)
    assert isinstance(mix_failure_context().value, Exception)

    @Try.do
    def mix_success_context() -> Generator[Try[int], Any, int]:
        one = yield multi_context(1)()
        two = 2
        three = yield multi_context(3)()
        return one + two + three

    assert Success(6) == mix_success_context()
    assert 6 == mix_success_context().value


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
    assert Right[None, int](12) == right_context().fold(
        left=lambda value: 0, right=lambda value: value * 2
    )
