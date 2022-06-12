def test_try_hold():
    from category import Failure, Success, Try

    @Try.hold
    def multi_context(value: int, /) -> int:
        if not value:
            raise Exception("error")
        return value

    assert Failure is type(multi_context(0))
    try:
        multi_context(0).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is multi_context(0).get_or_else(lambda: None)

    assert Success is type(multi_context(1))
    assert 1 == multi_context(1).get()
    assert 1 == multi_context(1).get_or_else(lambda: None)


def test_try_do():
    from category import Failure, Success, Try, TryDo

    @Try.do
    def failure_context() -> TryDo[int]:
        one = yield from Success[int](1)()
        two = 2
        three = yield from Failure[int](Exception())()
        return one + two + three

    assert Failure is type(failure_context())
    try:
        failure_context().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)

    @Try.do
    def success_context() -> TryDo[int]:
        one = yield from Success[int](1)()
        two = 2
        three = yield from Success[int](3)()
        return one + two + three

    assert Success is type(success_context())
    assert 6 == success_context().get()
    assert 6 == success_context().get_or_else(lambda: None)

    @Try.hold
    def multi_context(value: int, /) -> int:
        if not value:
            raise Exception("error")
        return value

    @Try.do
    def mix_failure_context() -> TryDo[int]:
        success = yield from multi_context(1)()
        _ = yield from multi_context(0)()
        return success

    assert Failure is type(mix_failure_context())
    try:
        type(mix_failure_context().get())
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert None is mix_failure_context().get_or_else(lambda: None)

    @Try.do
    def mix_success_context() -> TryDo[int]:
        one = yield from multi_context(1)()
        two = 2
        three = yield from multi_context(3)()
        return one + two + three

    assert Success is type(mix_success_context())
    assert 6 == mix_success_context().get()
    assert 6 == mix_success_context().get_or_else(lambda: None)


def test_failure():
    from category import Failure

    assert Failure is type(Failure[int](Exception()))
    assert False is bool(Failure[int](Exception()))


def test_failure_map():
    from category import Failure

    failure = Failure[int](Exception())
    mapped_failure = failure.map(lambda success: None)
    failure is not mapped_failure
    assert Failure is type(mapped_failure)


def test_failure_flatmap():
    from category import Failure, Success

    failure = Failure[int](Exception())
    flatmapped_failure = failure.flatmap(lambda success: Success[bool](True))
    assert failure is not flatmapped_failure
    assert Failure is type(flatmapped_failure)


def test_failure_fold():
    from category import Failure

    assert False is Failure[int](Exception()).fold(
        failure=lambda failure: False, success=lambda success: True
    )


def test_failure_is_failure():
    from category import Failure

    assert True is Failure[int](Exception()).is_failure()


def test_failure_is_success():
    from category import Failure

    assert False is Failure[int](Exception()).is_success()


def test_failure_get():
    from category import Failure

    try:
        Failure[int](Exception()).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)


def test_failure_get_or_else():
    from category import Failure

    assert False is Failure[int](Exception()).get_or_else(lambda: False)


def test_failure_method():
    from category import Failure, Success, Try

    def to_failure(self: Try[int], /) -> Failure[int]:
        if isinstance(self.pattern, Failure):
            return self.pattern
        else:
            return Failure[int](Exception())

    def to_success(self: Try[int], /) -> Success[int]:
        if isinstance(self.pattern, Failure):
            return Success[int](1)
        else:
            return self.pattern

    assert Failure is type(Failure[int](Exception()).method(to_failure))
    assert Success is type(Failure[int](Exception()).method(to_success))


def test_success():
    from category import Success

    assert Success is type(Success[int](0))
    assert True is bool(Success[int](0))


def test_success_map():
    from category import Success

    success = Success[int](0)
    mapped_success = success.map(lambda success: None)
    assert success is not mapped_success
    assert Success is type(mapped_success)
    assert None is mapped_success.get()


def test_success_flatmap():
    from category import Failure, Success

    success = Success[int](0)
    flatmapped_failure = success.flatmap(lambda success: Failure[None](Exception()))
    assert success is not flatmapped_failure
    assert Failure is type(flatmapped_failure)
    assert Success is type(Success[int](0).flatmap(lambda success: Success[None](None)))


def test_success_fold():
    from category import Success

    assert None is Success[int](0).fold(
        failure=lambda failure: None, success=lambda success: None
    )


def test_success_is_failure():
    from category import Success

    assert False is Success[int](0).is_failure()


def test_success_is_success():
    from category import Success

    assert True is Success[int](0).is_success()


def test_success_get():
    from category import Success

    assert 1 == Success[int](1).get()


def test_success_get_or_else():
    from category import Success

    assert 1 == Success[int](1).get_or_else(lambda: Exception())


def test_success_method():
    from category import Failure, Success, Try

    def to_failure(self: Try[int], /) -> Failure[int]:
        if isinstance(self.pattern, Failure):
            return self.pattern
        else:
            return Failure[int](Exception())

    def to_success(self: Try[int], /) -> Success[int]:
        if isinstance(self.pattern, Failure):
            return Success[int](1)
        else:
            return self.pattern

    assert Failure is type(Success[int](1).method(to_failure))
    assert Success is type(Success[int](1).method(to_success))


def test_dataclass():
    from dataclasses import asdict, dataclass

    from category import Failure, Success

    @dataclass(frozen=True)
    class AsDict:
        failure: Failure[int]
        success: Success[int]

    dict_data = asdict(
        AsDict(failure=Failure[int](Exception(42)), success=Success[int](42))
    )
    assert Failure is type(dict_data.get("failure", None))
    assert Exception is type(dict_data.get("failure", None)._exception)
    assert Success is type(dict_data.get("success", None))
    assert 42 == dict_data.get("success", None).get()


def test_pattern_match():
    from category import Failure, Success

    match Failure[int](Exception(42)):
        case Failure():
            assert True
        case _:
            assert False

    match Success[int](42):
        case Success() as success if success.get() == 42:
            assert True
        case _:
            assert False
