def test_failure():
    from category import Failure, FailureError

    assert Failure is type(Failure[int](value=Exception()))
    try:
        Failure[int](value=Exception()).get()
    except FailureError as error:
        assert FailureError is type(error)
    assert None is Failure[int](value=Exception()).get(
        if_failure_then=lambda error: None
    )
    assert True is Failure[int](value=Exception()).is_failure()
    assert False is Failure[int](value=Exception()).is_success()


def test_failure_map():
    from category import Failure, FailureError

    assert Failure is type(
        Failure[int](value=Exception()).map(functor=lambda e: TypeError())
    )
    try:
        Failure[int](value=Exception()).map(functor=lambda e: TypeError()).get()
    except FailureError as error:
        assert FailureError is type(error)
    assert None is Failure[int](value=Exception()).map(
        functor=lambda e: TypeError()
    ).get(if_failure_then=lambda error: None)
    assert (
        True
        is Failure[int](value=Exception())
        .map(functor=lambda e: TypeError())
        .is_failure()
    )
    assert (
        False
        is Failure[int](value=Exception())
        .map(functor=lambda e: TypeError())
        .is_success()
    )


def test_failure_flatmap():
    from category import Failure, FailureError

    assert Failure is type(
        Failure[int](value=Exception()).flatmap(
            functor=lambda e: Failure[int](value=TypeError())
        )
    )
    try:
        Failure[int](value=Exception()).flatmap(
            functor=lambda e: Failure[int](value=TypeError())
        ).get()
    except FailureError as error:
        assert FailureError is type(error)
    assert None is Failure[int](value=Exception()).flatmap(
        functor=lambda e: Failure[int](value=TypeError())
    ).get(if_failure_then=lambda error: None)
    assert (
        True
        is Failure[int](value=Exception())
        .flatmap(functor=lambda e: Failure[int](value=TypeError()))
        .is_failure()
    )
    assert (
        False
        is Failure[int](value=Exception())
        .flatmap(functor=lambda e: Failure[int](value=TypeError()))
        .is_success()
    )


def test_success():
    from category import Success

    assert Success is type(Success[int](value=0))
    assert 0 == Success[int](value=0).get()
    assert 0 == Success[int](value=0).get(if_failure_then=lambda error: None)
    assert False is Success[int](value=0).is_failure()
    assert True is Success[int](value=0).is_success()


def test_success_map():
    from category import Success

    assert Success is type(
        Success[int](value=0).map(functor=lambda integer: integer + 1)
    )
    assert 1 == Success[int](value=0).map(functor=lambda integer: integer + 1).get()
    assert 1 == Success[int](value=0).map(functor=lambda integer: integer + 1).get(
        if_failure_then=lambda error: None
    )
    assert (
        False
        is Success[int](value=0).map(functor=lambda integer: integer + 1).is_failure()
    )
    assert (
        True
        is Success[int](value=0).map(functor=lambda integer: integer + 1).is_success()
    )


def test_success_flatmap():
    from category import Success

    assert Success is type(
        Success[int](value=0).flatmap(
            functor=lambda integer: Success[int](value=integer + 1)
        )
    )
    assert (
        1
        == Success[int](value=0)
        .flatmap(functor=lambda integer: Success[int](value=integer + 1))
        .get()
    )
    assert 1 == Success[int](value=0).flatmap(
        functor=lambda integer: Success[int](value=integer + 1)
    ).get(if_failure_then=lambda error: None)
    assert (
        False
        is Success[int](value=0)
        .flatmap(functor=lambda integer: Success[int](value=integer + 1))
        .is_failure()
    )
    assert (
        True
        is Success[int](value=0)
        .flatmap(functor=lambda integer: Success[int](value=integer + 1))
        .is_success()
    )


def test_try_fold():
    from category import Failure, FailureError, Success

    try:
        assert (
            1
            == Failure[int](value=Exception())
            .fold(failure=lambda error: error, success=lambda integer: integer + 1)
            .get()
        )
    except FailureError as error:
        assert FailureError is type(error)
    assert None is Failure[int](value=Exception()).fold(
        failure=lambda error: error, success=lambda integer: integer + 1
    ).get(if_failure_then=lambda error: None)
    assert (
        1
        == Success[int](value=0)
        .fold(failure=lambda error: error, success=lambda integer: integer + 1)
        .get()
    )


def test_try_hold():
    from category import Failure, FailureError, Success, Try

    @Try.hold
    def multi_context(value: int) -> int:
        if not value:
            raise Exception("error")
        return value

    assert Failure is type(multi_context(0))
    try:
        type(multi_context(0).get())
    except FailureError as error:
        assert FailureError is type(error)
    assert None is multi_context(0).get(if_failure_then=lambda error: None)
    assert Success is type(multi_context(1))
    assert 1 == multi_context(1).get()
    assert 1 == multi_context(1).get(if_failure_then=lambda error: None)
    assert False is bool(multi_context(0))
    assert True is bool(multi_context(1))
    assert True is multi_context(0).is_failure()
    assert False is multi_context(0).is_success()
    assert False is multi_context(1).is_failure()
    assert True is multi_context(1).is_success()


def test_try_do():
    from category import Failure, Success, Try, TryDo

    @Try.do
    def failure_context() -> TryDo[int]:
        one = yield from Success(1)()
        two = 2
        three = yield from Failure(ValueError())()
        return one + two + three

    assert Failure is type(failure_context())
    assert ValueError is type(failure_context().value)
    assert False is bool(failure_context())
    assert False is failure_context().is_success()
    assert True is failure_context().is_failure()
    assert Failure is type(
        failure_context().fold(
            failure=lambda value: EOFError(), success=lambda value: value * 2
        )
    )

    @Try.do
    def success_context() -> TryDo[int]:
        one = yield from Success(1)()
        two = 2
        three = yield from Success(3)()
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
    def mix_failure_context() -> TryDo[int]:
        success = yield from multi_context(1)()
        _ = yield from multi_context(0)()
        return success

    assert Failure is type(mix_failure_context())
    assert Exception is type(mix_failure_context().value)

    @Try.do
    def mix_success_context() -> TryDo[int]:
        one = yield from multi_context(1)()
        two = 2
        three = yield from multi_context(3)()
        return one + two + three

    assert Success(6) == mix_success_context()
    assert 6 == mix_success_context().value
