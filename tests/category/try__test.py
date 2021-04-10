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
        one = yield from Success[int](value=1)()
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
    def success_context() -> TryDo[int]:
        one = yield from Success[int](value=1)()
        two = 2
        three = yield from Success[int](value=3)()
        return one + two + three

    assert Success(value=6) == success_context()
    assert 6 == success_context().get()
    assert 6 == success_context().get_or_else(default=lambda: None)

    @Try.hold
    def multi_context(value: int) -> int:
        if not value:
            raise Exception("error")
        return value

    @Try.do
    def mix_failure_context() -> TryDo[int]:
        success = yield from multi_context(value=1)()
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
        one = yield from multi_context(value=1)()
        two = 2
        three = yield from multi_context(value=3)()
        return one + two + three

    assert Success(value=6) == mix_success_context()
    assert 6 == mix_success_context().get()
    assert 6 == mix_success_context().get_or_else(default=lambda: None)


def test_failure():
    from category import Failure

    assert Failure is type(Failure[int](value=Exception()))
    assert False is bool(Failure[int](value=Exception()))


def test_failure_map():
    from category import Failure

    failure = Failure[int](value=Exception())
    mapped_failure = failure.map(functor=lambda success: None)
    failure is not mapped_failure
    assert Failure is type(mapped_failure)


def test_failure_flatmap():
    from category import Failure, Success

    failure = Failure[int](value=Exception())
    flatmapped_failure = failure.flatmap(
        functor=lambda success: Success[bool](value=True)
    )
    assert failure is not flatmapped_failure
    assert Failure is type(flatmapped_failure)


def test_failure_fold():
    from category import Failure

    assert False is Failure[int](value=Exception()).fold(
        failure=lambda failure: False, success=lambda success: True
    )


def test_failure_is_failure():
    from category import Failure

    assert True is Failure[int](value=Exception()).is_failure()


def test_failure_is_success():
    from category import Failure

    assert False is Failure[int](value=Exception()).is_success()


def test_failure_get():
    from category import Failure

    try:
        Failure[int](value=Exception()).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)


def test_failure_get_or_else():
    from category import Failure

    assert False is Failure[int](value=Exception()).get_or_else(default=lambda: False)


def test_failure_convert():
    from category import Failure, Success, Try

    def to_failure(try_: Try[int]) -> Failure[int]:
        if isinstance(try_.pattern, Failure):
            return try_.pattern
        else:
            return Failure[int](value=Exception())

    def to_success(try_: Try[int]) -> Success[int]:
        if isinstance(try_.pattern, Failure):
            return Success[int](value=1)
        else:
            return try_.pattern

    assert Failure is type(Failure[int](value=Exception()).method(to_failure))
    assert Success is type(Failure[int](value=Exception()).method(to_success))


def test_success():
    from category import Success

    assert Success is type(Success[int](value=0))
    assert True is bool(Success[int](value=0))


def test_success_map():
    from category import Success

    success = Success[int](value=0)
    mapped_success = success.map(functor=lambda success: None)
    assert success is not mapped_success
    assert Success is type(mapped_success)
    assert None is mapped_success.get()


def test_success_flatmap():
    from category import Failure, Success

    success = Success[int](value=0)
    flatmapped_failure = success.flatmap(
        functor=lambda success: Failure[None](value=Exception())
    )
    assert success is not flatmapped_failure
    assert Failure is type(flatmapped_failure)
    assert Success is type(
        Success[int](value=0).flatmap(functor=lambda success: Success[None](value=None))
    )


def test_success_fold():
    from category import Success

    assert None is Success[int](value=0).fold(
        failure=lambda failure: None, success=lambda success: None
    )


def test_success_is_failure():
    from category import Success

    assert False is Success[int](value=0).is_failure()


def test_success_is_success():
    from category import Success

    assert True is Success[int](value=0).is_success()


def test_success_get():
    from category import Success

    assert 1 == Success[int](value=1).get()


def test_success_get_or_else():
    from category import Success

    assert 1 == Success[int](value=1).get_or_else(default=lambda: Exception())


def test_success_convert():
    from category import Failure, Success, Try

    def to_failure(try_: Try[int]) -> Failure[int]:
        if isinstance(try_.pattern, Failure):
            return try_.pattern
        else:
            return Failure[int](value=Exception())

    def to_success(try_: Try[int]) -> Success[int]:
        if isinstance(try_.pattern, Failure):
            return Success[int](value=1)
        else:
            return try_.pattern

    assert Failure is type(Success[int](value=1).method(to_failure))
    assert Success is type(Success[int](value=1).method(to_success))
