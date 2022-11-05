from category import Future

SLEEP_TIME = 1


def process_multi_context(value: int, /) -> int:
    import time

    time.sleep(SLEEP_TIME)
    if 0 < value:
        return value
    else:
        raise ValueError(value)


@Future.hold
def thread_multi_context(value: int, /) -> int:
    import time

    time.sleep(SLEEP_TIME)
    if 0 < value:
        return value
    else:
        raise ValueError(value)


def test_future():
    from category import Future

    assert Future is type(Future[int].successful(1))
    assert True is bool(Future[int].successful(1))
    assert False is bool(Future[int]())


def test_map():
    from typing import cast

    from category import (
        Failure,
        Future,
        ProcessPoolExecutionContext,
        Success,
        ThreadPoolExecutionContext,
    )

    pc = ProcessPoolExecutionContext(max_workers=5)
    tc = ThreadPoolExecutionContext(max_workers=5)

    # Failure finished case
    failure_future = Future[int].failed(Exception("Failure"))
    failure_mapped_future = failure_future.map(lambda success: success + 1)(pc)
    assert failure_future is not failure_mapped_future
    assert Future is type(failure_mapped_future)
    try:
        failure_mapped_future.result()
        assert False
    except Exception as error:
        assert Exception is type(error)
    assert Failure is type(failure_mapped_future.value)
    assert Exception is type(cast(Failure[int], failure_mapped_future.value).exception)

    # Failure process running case
    failure_process = Future.hold(process_multi_context)(0)(pc)
    failure_mapped_process = failure_process.map(lambda success: success + 1)(pc)
    assert failure_process is not failure_mapped_process
    assert Future is type(failure_mapped_process)
    try:
        failure_mapped_process.result()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert Failure is type(failure_mapped_process.value)
    assert ValueError is type(
        cast(Failure[int], failure_mapped_process.value).exception
    )

    # Failure thread running case
    failure_thread = thread_multi_context(0)(tc)
    failure_mapped_thread = failure_thread.map(lambda success: success + 1)(tc)
    assert failure_thread is not failure_mapped_thread
    assert Future is type(failure_mapped_thread)
    try:
        failure_mapped_thread.result()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert Failure is type(failure_mapped_thread.value)
    assert ValueError is type(cast(Failure[int], failure_mapped_thread.value).exception)

    # Success finished case
    success_future = Future.successful(42)
    success_mapped_future = success_future.map(lambda success: success + 1)(pc)
    assert success_future is not success_mapped_future
    assert Future is type(success_mapped_future)
    assert 43 == success_mapped_future.result()
    assert Success is type(success_mapped_future.value)
    assert 43 == success_mapped_future.value.get()

    # Success process running case
    success_process = Future.hold(process_multi_context)(42)(pc)
    success_mapped_process = success_future.map(lambda success: success + 1)(pc)
    assert success_process is not success_mapped_process
    assert Future is type(success_mapped_process)
    assert 43 == success_mapped_process.result()
    assert Success is type(success_mapped_process.value)
    assert 43 == success_mapped_process.value.get()

    # Success thread running case
    success_thread = thread_multi_context(42)(tc)
    success_mapped_thread = success_future.map(lambda success: success + 1)(tc)
    assert success_thread is not success_mapped_thread
    assert Future is type(success_mapped_thread)
    assert 43 == success_mapped_thread.result()
    assert Success is type(success_mapped_thread.value)
    assert 43 == success_mapped_thread.value.get()


def test_flat_map():
    from typing import cast

    from category import (
        Failure,
        Future,
        ProcessPoolExecutionContext,
        Success,
        ThreadPoolExecutionContext,
    )

    pc = ProcessPoolExecutionContext(max_workers=5)
    tc = ThreadPoolExecutionContext(max_workers=5)

    # Failure finished case
    failure_future = Future[int].failed(Exception())
    failure_flat_mapped_future = failure_future.flat_map(
        lambda success: Future[int].successful(success + 1)
    )(pc)
    assert failure_future is not failure_flat_mapped_future
    assert Future is type(failure_flat_mapped_future)
    try:
        failure_flat_mapped_future.result()
        assert False
    except Exception as error:
        assert Exception is type(error)
    assert Failure is type(failure_flat_mapped_future.value)
    assert Exception is type(
        cast(Failure[int], failure_flat_mapped_future.value).exception
    )

    # Failure process running case
    failure_process = Future.hold(process_multi_context)(0)(pc)
    failure_flat_mapped_process = failure_process.flat_map(
        lambda success: Future[int].successful(success + 1)
    )(pc)
    assert failure_process is not failure_flat_mapped_process
    assert Future is type(failure_flat_mapped_process)
    try:
        failure_flat_mapped_process.result()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert Failure is type(failure_flat_mapped_process.value)
    assert ValueError is type(
        cast(Failure[int], failure_flat_mapped_process.value).exception
    )

    # Failure thread running case
    failure_thread = Future.hold(process_multi_context)(0)(tc)
    failure_flat_mapped_thread = failure_thread.flat_map(
        lambda success: Future[int].successful(success + 1)
    )(tc)
    assert failure_thread is not failure_flat_mapped_thread
    assert Future is type(failure_flat_mapped_thread)
    try:
        failure_flat_mapped_thread.result()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert Failure is type(failure_flat_mapped_thread.value)
    assert ValueError is type(
        cast(Failure[int], failure_flat_mapped_thread.value).exception
    )

    # Success finished case
    success_future = Future[int].successful(42)
    success_flat_mapped_future = success_future.flat_map(
        lambda success: Future[int].successful(success + 1)
    )(pc)
    assert success_future is not success_flat_mapped_future
    assert Future is type(success_flat_mapped_future)
    assert 43 == success_flat_mapped_future.result()
    assert Success is type(success_flat_mapped_future.value)
    assert 43 == success_flat_mapped_future.value.get()

    # Success process running case
    success_process = Future[int].hold(process_multi_context)(42)(pc)
    success_flat_mapped_process = success_process.flat_map(
        lambda success: Future[int].successful(success + 1)
    )(pc)
    assert success_process is not success_flat_mapped_process
    assert Future is type(success_flat_mapped_process)
    assert 43 == success_flat_mapped_process.result()
    assert Success is type(success_flat_mapped_process.value)
    assert 43 == success_flat_mapped_process.value.get()

    # Success thread running case
    success_thread = thread_multi_context(42)(tc)
    success_flat_mapped_thread = success_thread.flat_map(
        lambda success: Future[int].successful(success + 1)
    )(tc)
    assert success_thread is not success_flat_mapped_thread
    assert Future is type(success_flat_mapped_thread)
    assert 43 == success_flat_mapped_thread.result()
    assert Success is type(success_flat_mapped_thread.value)
    assert 43 == success_flat_mapped_thread.value.get()


def test_recover():
    from category import (
        Failure,
        Future,
        ProcessPoolExecutionContext,
        Success,
        ThreadPoolExecutionContext,
    )

    pe = ProcessPoolExecutionContext(max_workers=5)
    te = ThreadPoolExecutionContext(max_workers=5)

    failure_process = Future.hold(process_multi_context)(0)(pe)
    failure_recover_process = failure_process.recover(lambda exception: 42)(pe)
    assert failure_process is not failure_recover_process
    assert Success is type(failure_recover_process.value)
    assert 42 == failure_recover_process.result()

    failure_unrecover_process = failure_process.recover(lambda exception: None)(pe)
    assert failure_process is not failure_unrecover_process
    assert Failure is type(failure_unrecover_process.value)

    failure_thread = thread_multi_context(0)(te)
    failure_recover_thread = failure_thread.recover(lambda exception: 42)(te)
    assert failure_thread is not failure_recover_thread
    assert Success is type(failure_recover_thread.value)
    assert 42 == failure_recover_thread.result()

    failure_unrecover_thread = failure_thread.recover(lambda exception: None)(te)
    assert failure_thread is not failure_unrecover_thread
    assert Failure is type(failure_unrecover_thread.value)


def test_recover_with():
    from category import (
        Failure,
        Future,
        ProcessPoolExecutionContext,
        Success,
        ThreadPoolExecutionContext,
    )

    pe = ProcessPoolExecutionContext(max_workers=5)
    te = ThreadPoolExecutionContext(max_workers=5)

    failure_process = Future.hold(process_multi_context)(0)(pe)
    failure_recover_process = failure_process.recover_with(
        lambda exception: Future[int].successful(42)
    )(pe)
    assert failure_process is not failure_recover_process
    assert Success is type(failure_recover_process.value)
    assert 42 == failure_recover_process.result()

    failure_unrecover_process = failure_process.recover_with(lambda exception: None)(pe)
    assert failure_process is not failure_unrecover_process
    assert Failure is type(failure_unrecover_process.value)

    failure_thread = thread_multi_context(0)(te)
    failure_recover_thread = failure_thread.recover_with(
        lambda exception: Future[int].successful(42)
    )(te)
    assert failure_thread is not failure_recover_thread
    assert Success is type(failure_recover_thread.value)
    assert 42 == failure_recover_thread.result()

    failure_unrecover_thread = failure_thread.recover_with(lambda exception: None)(te)
    assert failure_thread is not failure_unrecover_thread
    assert Failure is type(failure_unrecover_thread.value)


def test_from_try():
    from category import Failure, Future, Success

    failure_future = Future[int].from_try(Failure[int](Exception("Error")))
    assert Failure is type(failure_future.value)

    success_future = Future[int].from_try(Success[int](42))
    assert Success is type(success_future.value)
    assert 42 == success_future.result()


def test_try_complete():
    import time
    from typing import cast

    from category import (
        Failure,
        Future,
        ProcessPoolExecutionContext,
        Success,
        ThreadPoolExecutionContext,
    )

    pc = ProcessPoolExecutionContext(max_workers=5)
    tc = ThreadPoolExecutionContext(max_workers=5)

    # Failure case
    failure_future = Future[int].failed(Exception())
    assert False is failure_future.try_complete(Success(1))
    try:
        failure_future.result()
        assert False
    except Exception as error:
        assert Exception is type(error)
    assert Failure is type(failure_future.value)
    assert Exception is type(cast(Failure[int], failure_future.value).exception)

    # Failure process case
    failure_process = Future[int].hold(process_multi_context)(0)(pc)
    time.sleep(SLEEP_TIME + 1)
    assert False is failure_process.try_complete(Success(1))
    try:
        failure_process.result()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert Failure is type(failure_process.value)
    assert ValueError is type(cast(Failure[int], failure_process.value).exception)

    # Failure thread case
    failure_thread = thread_multi_context(0)(tc)
    time.sleep(SLEEP_TIME + 1)
    assert False is failure_thread.try_complete(Success(1))
    try:
        failure_thread.result()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert Failure is type(failure_thread.value)
    assert ValueError is type(cast(Failure[int], failure_thread.value).exception)

    # Success case
    success_future = Future[int].successful(42)
    assert False is success_future.try_complete(Success(2))
    assert 42 == success_future.result()
    assert Success is type(success_future.value)
    assert 42 == success_future.value.get()

    # Success process case
    success_process = Future[int].hold(process_multi_context)(42)(pc)
    assert True is success_process.try_complete(Success(0))
    time.sleep(SLEEP_TIME + 1)
    assert 0 == success_process.result()
    assert Success is type(success_process.value)
    assert 0 == success_process.value.get()

    # Success thread case
    success_thread = thread_multi_context(42)(tc)
    assert True is success_thread.try_complete(Success(0))
    time.sleep(SLEEP_TIME + 1)
    assert 0 == success_thread.result()
    assert Success is type(success_thread.value)
    assert 0 == success_thread.value.get()


def test_on_complete():
    import time

    from category import (
        Failure,
        Future,
        ProcessPoolExecutionContext,
        Success,
        ThreadPoolExecutionContext,
        Try,
    )

    def on_complete(try_: Try[int], /) -> str:
        match try_.pattern:
            case Failure():
                return "Failure"
            case Success():
                return "Success"

    pe = ProcessPoolExecutionContext(max_workers=5)
    te = ThreadPoolExecutionContext(max_workers=5)

    # Process case
    success_process = Future.successful(42)
    success_process.on_complete(on_complete)(pe)
    time.sleep(SLEEP_TIME)
    assert 42 == success_process.result()

    failure_process = Future[int].failed(Exception("Failure"))
    failure_process.on_complete(on_complete)(pe)
    time.sleep(SLEEP_TIME)
    try:
        failure_process.result()
        assert False
    except Exception as exception:
        assert Exception is type(exception)

    # thread case
    success_thread = Future.successful(42)
    success_thread.on_complete(on_complete)(te)
    time.sleep(SLEEP_TIME)
    assert 42 == success_thread.result()

    failure_thread = Future[int].failed(Exception("Failure"))
    failure_thread.on_complete(on_complete)(te)
    time.sleep(SLEEP_TIME)
    try:
        failure_thread.result()
        assert False
    except Exception as exception:
        assert Exception is type(exception)


def test_successful():
    from category import Future, Success

    success_future = Future[int].successful(42)
    assert Future is type(success_future)
    assert 42 == success_future.result()
    assert Success is type(success_future.value)
    assert 42 == success_future.value.get()


def test_failed():
    from category import Failure, Future

    failure_future = Future[int].failed(Exception("Error"))
    assert Future is type(failure_future)
    try:
        failure_future.result()
        assert False
    except Exception:
        assert True
    assert Failure is type(failure_future.value)
    try:
        failure_future.value.get()
        assert False
    except Exception:
        assert True


def test_hold():
    from typing import cast

    from category import (
        Failure,
        Future,
        ProcessPoolExecutionContext,
        Success,
        ThreadPoolExecutionContext,
    )

    pe = ProcessPoolExecutionContext(max_workers=5)
    te = ThreadPoolExecutionContext(max_workers=5)

    assert "thread_multi_context" == thread_multi_context.__name__

    # Failure case
    failure_future = thread_multi_context(0)(te)
    assert Future is type(failure_future)
    assert Failure is type(failure_future.value)
    assert ValueError is type(cast(Failure[int], failure_future.value).exception)
    failure_future = Future.hold(process_multi_context)(0)(pe)
    assert Future is type(failure_future)
    assert Failure is type(failure_future.value)
    assert ValueError is type(cast(Failure[int], failure_future.value).exception)

    # Success case
    success_future = thread_multi_context(42)(te)
    assert Future is type(success_future)
    assert 42 == success_future.result()
    assert Success is type(success_future.value)
    assert 42 == success_future.value.get()
    success_future = Future.hold(process_multi_context)(42)(pe)
    assert Future is type(success_future)
    assert 42 == success_future.result()
    assert Success is type(success_future.value)
    assert 42 == success_future.value.get()


def test_do():
    from typing import cast

    from category import (
        Failure,
        Future,
        FutureDo,
        ProcessPoolExecutionContext,
        Success,
        ThreadPoolExecutionContext,
    )

    pe = ProcessPoolExecutionContext(max_workers=5)
    te = ThreadPoolExecutionContext(max_workers=5)

    @Future.do
    def safe_context() -> FutureDo[int]:
        _ = yield from Future[bool].successful(True)
        one = yield from Future[int].hold(process_multi_context)(1)(pe)
        two = 2
        three = yield from thread_multi_context(0)(te)
        return one + two + three

    # Failure case
    @Future.do
    def failure_context() -> FutureDo[int]:
        one = yield from Future[int].hold(process_multi_context)(1)(pe)
        two = 2
        three = yield from thread_multi_context(0)(te)
        return one + two + three

    failure_result = failure_context()(pe)
    assert Future is type(failure_result)
    try:
        failure_result.result()
        assert False
    except Exception:
        assert True
    assert Failure is type(failure_result.value)
    assert ValueError is type(cast(Failure[int], failure_result.value).exception)

    # Success case
    @Future.do
    def success_context() -> FutureDo[int]:
        one = yield from Future[int].hold(process_multi_context)(1)(pe)
        two = 2
        three = yield from thread_multi_context(3)(te)
        return one + two + three

    success_result = success_context()(te)
    assert Future is type(success_result)
    assert 6 == success_result.result()
    assert Success is type(success_result.value)
    assert 6 == success_result.value.get()


def test_method():
    from category import Failure, Future, Success

    def to_failure(self: Future[int], /) -> Future[int]:
        try:
            self.result()
            return Future[int].failed(Exception())
        except Exception as error:
            return Future[int].failed(error)

    def to_success(self: Future[int], /) -> Future[int]:
        try:
            result = self.result()
            return Future[int].successful(result)
        except Exception:
            return Future[int].successful(42)

    failure = Future[int].failed(Exception())
    success = Future[int].successful(42)
    assert Future is type(failure.method(to_failure))
    assert Failure is type(failure.method(to_failure).value)
    assert Future is type(failure.method(to_success))
    assert Success is type(failure.method(to_success).value)
    assert Future is type(success.method(to_failure))
    assert Failure is type(success.method(to_failure).value)
    assert Future is type(success.method(to_success))
    assert Success is type(success.method(to_success).value)
