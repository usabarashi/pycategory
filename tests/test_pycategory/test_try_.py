def test_functor_law():
    from pycategory import Failure, Success, functor

    assert functor.identity_law(Failure[int](Exception()))
    assert functor.identity_law(Success[int](42))
    assert functor.composite_law(F=Failure[int](Exception()), f=lambda v: [v], g=lambda v: (v,))
    assert functor.composite_law(F=Success[int](42), f=lambda v: [v], g=lambda v: (v,))


def test_try_hold():
    from typing import cast

    from pycategory import Failure, Success, Try, processor

    @Try.hold
    def multi_context(value: int, /) -> int:
        if not value:
            raise Exception("error")
        return value

    assert "multi_context" == multi_context.__name__

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

    class Class_:
        def __init__(self, public_value: int, private_value: int):
            self.public_value = public_value
            self._private_value = private_value

    @Try.hold(
        unmask=("unmask", "class_"),
        debugger=lambda arguments: arguments.get("mask"),
    )
    def unmask_context(mask: int, unmask: str, class_: Class_) -> str:
        if not mask:
            raise Exception("error")
        return unmask

    result = unmask_context(0, unmask="John Doe.", class_=Class_(public_value=42, private_value=42))
    assert Failure is type(result)
    failure = cast(Failure[str], result)
    assert processor.RuntimeErrorReport is type(failure.exception.args[-1])
    runtime_error_report = cast(processor.RuntimeErrorReport, failure.exception.args[-1])
    assert {
        "mask": processor.MASK,
        "unmask": "John Doe.",
        "class_": {"public_value": 42, "_private_value": processor.MASK},
    } == runtime_error_report.arguments
    assert 0 == runtime_error_report.debug


def test_try_do():
    from pycategory import Failure, Right, Success, Try, TryDo

    @Try.do
    def safe_context() -> TryDo[int]:  # type: ignore # Not access
        _ = yield from Success[bool](True)
        one = yield from Success[int](1)
        two = 2
        three = yield from Success[int](3)
        return one + two + three

    @Try.do
    def outside_context() -> TryDo[int]:  # type: ignore # Not access
        _ = yield from Success[bool](True)
        one = yield from Success[int](1)
        two = 2
        three = yield from Success[int](3)
        three = yield from Right[Exception, int](42)  # type: ignore # Error case
        return str(one + two + three)  # type: ignore # Error case

    @Try.do
    def failure_context() -> TryDo[int]:
        one = yield from Success[int](1)
        two = 2
        three = yield from Failure[int](Exception())
        return one + two + three

    assert Failure is type(failure_context())
    try:
        failure_context().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)

    @Try.do
    def success_context() -> TryDo[int]:
        one = yield from Success[int](1)
        two = 2
        three = yield from Success[int](3)
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
        success = yield from multi_context(1)
        _ = yield from multi_context(0)
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
        one = yield from multi_context(1)
        two = 2
        three = yield from multi_context(3)
        return one + two + three

    assert Success is type(mix_success_context())
    assert 6 == mix_success_context().get()
    assert 6 == mix_success_context().get_or_else(lambda: None)


def test_failure():
    from pycategory import Failure

    assert Failure is type(Failure[int](Exception()))
    assert Failure is type(eval(f"{repr(Failure[int](Exception()))}"))


def test_failure_map():
    from pycategory import Failure

    failure = Failure[int](Exception())
    mapped_failure = failure.map(lambda success: None)
    assert failure is mapped_failure
    assert Failure is type(mapped_failure)


def test_failure_flat_map():
    from pycategory import Failure, Success

    failure = Failure[int](Exception())
    flat_mapped_failure = failure.flat_map(lambda success: Success[bool](True))
    assert failure is flat_mapped_failure
    assert Failure is type(flat_mapped_failure)


def test_failure_recover():
    from pycategory import Failure, Success

    failure = Failure[int](Exception())
    recover_failure = failure.recover(lambda exception: 42)
    assert failure is not recover_failure
    assert Success is type(recover_failure)
    assert 42 == recover_failure.get()


def test_failure_recover_with():
    from pycategory import Failure, Success

    failure = Failure[int](Exception())
    recover_with_failure = failure.recover_with(lambda exception: Success[int](42))
    assert failure is not recover_with_failure
    assert Success is type(recover_with_failure)
    assert 42 == recover_with_failure.get()


def test_failure_to_either():
    from pycategory import Failure, Left

    assert Left is type(Failure[int](Exception()).to_either)
    assert None is Failure[int](Exception()).to_either.get_or_else(lambda: None)


def test_failure_to_option():
    from pycategory import Failure, Void

    assert Void is type(Failure[int](Exception()).to_option)


def test_failure_fold():
    from pycategory import Failure

    assert False is Failure[int](Exception()).fold(
        failure=lambda failure: False, success=lambda success: True
    )


def test_failure_is_failure():
    from pycategory import Failure

    assert True is Failure[int](Exception()).is_failure()


def test_failure_is_success():
    from pycategory import Failure

    assert False is Failure[int](Exception()).is_success()


def test_failure_get():
    from pycategory import Failure

    try:
        Failure[int](Exception()).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)


def test_failure_get_or_else():
    from pycategory import Failure

    assert False is Failure[int](Exception()).get_or_else(lambda: False)


def test_success():
    from pycategory import Success

    assert Success is type(Success[int](42))
    assert Success is type(eval(f"{repr(Success[int](42))}"))


def test_success_map():
    from pycategory import Success

    success = Success[int](0)
    mapped_success = success.map(lambda success: None)
    assert success is not mapped_success
    assert Success is type(mapped_success)
    assert None is mapped_success.get()


def test_success_flat_map():
    from pycategory import Failure, Success

    success = Success[int](0)
    flat_mapped_failure = success.flat_map(lambda success: Failure[None](Exception()))
    assert success is not flat_mapped_failure
    assert Failure is type(flat_mapped_failure)
    assert Success is type(Success[int](0).flat_map(lambda success: Success[None](None)))


def test_success_recover():
    from pycategory import Success

    success = Success[int](42)
    recover_success = success.recover(lambda success: None)
    assert success is recover_success
    assert Success is type(recover_success)
    assert 42 == recover_success.get()


def test_success_recover_with():
    from pycategory import Failure, Success

    success = Success[int](42)
    recover_with_failure = success.recover_with(lambda success: Failure[None](Exception()))
    assert success is recover_with_failure
    assert Success is type(recover_with_failure)
    assert 42 == recover_with_failure.get()


def test_success_to_either():
    from pycategory import Right, Success

    assert Right is type(Success[int](42).to_either)
    assert 42 == Success[int](42).to_either.get_or_else(lambda: None)


def test_success_to_option():
    from pycategory import Some, Success

    assert Some is type(Success[int](42).to_option)
    assert 42 == Success[int](42).to_option.get_or_else(lambda: None)


def test_success_fold():
    from pycategory import Success

    assert None is Success[int](0).fold(failure=lambda failure: None, success=lambda success: None)


def test_success_is_failure():
    from pycategory import Success

    assert False is Success[int](0).is_failure()


def test_success_is_success():
    from pycategory import Success

    assert True is Success[int](0).is_success()


def test_success_get():
    from pycategory import Success

    assert 1 == Success[int](1).get()


def test_success_get_or_else():
    from pycategory import Success

    assert 1 == Success[int](1).get_or_else(lambda: Exception())


def test_dataclass():
    from dataclasses import asdict, dataclass
    from typing import cast

    from pycategory import Failure, Success

    @dataclass(frozen=True)
    class AsDict:
        failure: Failure[int]
        success: Success[int]

    dict_data = asdict(AsDict(failure=Failure[int](Exception(42)), success=Success[int](42)))
    assert Failure is type(dict_data.get("failure", None))
    assert Exception is type(cast(Failure[int], dict_data.get("failure", None)).exception)
    assert Success is type(dict_data.get("success", None))
    assert 42 == cast(Success[int], dict_data.get("success", None)).get()


def test_pattern_match():
    from typing import cast

    from pycategory import Failure, Success, Try

    match cast(Try[int], Failure[int](Exception(42))):
        case Failure():
            assert True
        case _:
            assert False

    match cast(Try[int], Success(42)):
        case Success(42):
            assert True
        case _:
            assert False
