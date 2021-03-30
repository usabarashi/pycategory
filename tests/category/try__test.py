def test_failure():
    from category import Failure

    assert Failure is type(Failure[int](value=Exception()))
    try:
        Failure[int](value=Exception()).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is Failure[int](value=Exception()).get_or_else(default=lambda: None)
    assert True is Failure[int](value=Exception()).is_failure()
    assert False is Failure[int](value=Exception()).is_success()


def test_failure_map():
    from category import Failure

    assert Failure is type(
        Failure[int](value=Exception()).map(functor=lambda success: None)
    )


def test_failure_flatmap():
    from category import Failure, Success

    assert Failure is type(
        Failure[int](value=Exception()).flatmap(
            functor=lambda success: Failure[None](value=Exception())
        )
    )
    assert Failure is type(
        Failure[int](value=Exception()).flatmap(
            functor=lambda success: Success[None](value=None)
        )
    )


def test_success():
    from category import Success

    assert Success is type(Success[int](value=0))
    assert 0 == Success[int](value=0).get()
    assert 0 == Success[int](value=0).get_or_else(default=lambda: None)
    assert False is Success[int](value=0).is_failure()
    assert True is Success[int](value=0).is_success()


def test_success_map():
    from category import Success

    assert Success is type(Success[int](value=0).map(functor=lambda success: None))


def test_success_flatmap():
    from category import Failure, Success

    assert Failure is type(
        Success[int](value=0).flatmap(
            functor=lambda success: Failure[None](value=Exception())
        )
    )
    assert Success is type(
        Success[int](value=0).flatmap(functor=lambda success: Success[None](value=None))
    )


def test_try_fold():
    from category import Failure, Success

    assert None is Failure[int](value=Exception()).fold(
        failure=lambda failure: None, success=lambda success: None
    )
    assert None is Success[int](value=0).fold(
        failure=lambda failure: None, success=lambda success: None
    )


def test_try_hold():
    from category import Failure, Success, Try

    @Try.hold
    def multi_context(value: int) -> int:
        if not value:
            raise Exception("error")
        return value

    assert Failure is type(multi_context(value=0))
    try:
        multi_context(value=0).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is multi_context(value=0).get_or_else(default=lambda: None)

    assert Success is type(multi_context(value=1))
    assert 1 == multi_context(value=1).get()
    assert 1 == multi_context(value=1).get_or_else(default=lambda: None)


def test_try_do():
    from category import Failure, Success, Try, TryDo

    @Try.do
    def failure_context() -> TryDo[int]:
        one = yield from Success(value=1)()
        two = 2
        three = yield from Failure[int](value=Exception())()
        return one + two + three

    assert Failure is type(failure_context())
    try:
        failure_context().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)

    @Try.do
    def failure_convert_context() -> TryDo[int]:
        one = yield from Success(value=1)()
        two = 2
        three = yield from Failure[int](value=Exception())(
            convert=lambda exception: Failure[int](value=ValueError())
        )
        return one + two + three

    assert Failure is type(failure_convert_context())
    try:
        failure_convert_context().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert ValueError is type(failure_convert_context().value)

    @Try.do
    def success_context() -> TryDo[int]:
        one = yield from Success(value=1)()
        two = 2
        three = yield from Success(value=3)()
        return one + two + three

    assert Success(value=6) == success_context()
    assert 6 == success_context().get()
    assert 6 == success_context().get_or_else(default=lambda: None)

    @Try.do
    def success_convert_context() -> TryDo[int]:
        one = yield from Success(value=1)()
        two = 2
        three = yield from Success(value=3)(convert=lambda success: Success(value=3))
        return one + two + three

    try:
        success_convert_context()
        assert False
    except BaseException as error:
        GeneratorExit is type(error)

    @Try.hold
    def multi_context(value: int) -> int:
        if not value:
            raise Exception("error")
        return value

    @Try.do
    def mix_failure_context() -> TryDo[int]:
        success: int = yield from multi_context(value=1)()
        _ = yield from multi_context(valeu=0)()
        return success

    assert Failure is type(mix_failure_context())
    try:
        type(mix_failure_context().get())
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is mix_failure_context().get_or_else(default=lambda: None)

    @Try.do
    def mix_success_context() -> TryDo[int]:
        one: int = yield from multi_context(value=1)()
        two = 2
        three: int = yield from multi_context(value=3)()
        return one + two + three

    assert Success(value=6) == mix_success_context()
    assert 6 == mix_success_context().get()
    assert 6 == mix_success_context().get_or_else(default=lambda: None)
