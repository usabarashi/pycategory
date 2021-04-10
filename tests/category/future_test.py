def test_future():
    from category import Future

    assert Future is type(Future[int].successful(value=1))
    assert True is bool(Future[int].successful(value=1))
    assert False is bool(Future[int]())


def test_map():
    from category import Failure, Future, Success
    from category import ThreadPoolExecutionContext as ec

    # Failure case
    failure_future = Future[int]()
    failure_future.set_exception(exception=Exception())
    failure_mapped_future = failure_future.map(functor=lambda success: success + 1)(ec)
    assert failure_future is not failure_mapped_future
    assert Future is type(failure_mapped_future)
    try:
        failure_mapped_future.result()
        assert False
    except Exception as error:
        assert Exception is type(error)
    assert Failure is type(failure_mapped_future.value)
    assert Exception is type(failure_mapped_future.value.value)

    # Success case
    success_future = Future.successful(value=1)
    success_mapped_future = success_future.map(functor=lambda success: success + 1)(ec)
    assert success_future is not success_mapped_future
    assert Future is type(success_mapped_future)
    assert 2 == success_mapped_future.result()
    assert Success is type(success_mapped_future.value)
    assert 2 == success_mapped_future.value.get()


def test_flatmap():
    from category import Failure, Future, Success
    from category import ThreadPoolExecutionContext as ec

    # Failure case
    failure_future = Future[int]()
    failure_future.set_exception(exception=Exception())
    failure_flatmapped_future = failure_future.flatmap(
        functor=lambda success: Future[int].successful(value=success + 1)
    )(ec)
    assert failure_future is not failure_flatmapped_future
    assert Future is type(failure_flatmapped_future)
    try:
        failure_flatmapped_future.result()
        assert False
    except Exception as error:
        assert Exception is type(error)
    assert Failure is type(failure_flatmapped_future.value)
    assert Exception is type(failure_flatmapped_future.value.value)

    # Success case
    success_future = Future[int].successful(value=1)
    success_flatmapped_future = success_future.flatmap(
        functor=lambda success: Future[int].successful(value=success + 1)
    )(ec)
    assert success_future is not success_flatmapped_future
    assert Future is type(success_flatmapped_future)
    assert 2 == success_flatmapped_future.result()
    assert Success is type(success_flatmapped_future.value)
    assert 2 == success_flatmapped_future.value.get()


def test_try_complete():
    from category import Failure, Future, Success

    # Failure case
    failure_future = Future[int]()
    failure_future.set_exception(exception=Exception())
    assert False is failure_future.try_complete(result=Success(value=1))
    try:
        failure_future.result()
        assert False
    except Exception as error:
        assert Exception is type(error)
    assert Failure is type(failure_future.value)
    assert Exception is type(failure_future.value.value)

    # Success case
    success_future = Future[int].successful(value=1)
    assert False is success_future.try_complete(result=Success(value=2))
    assert 1 == success_future.result()
    assert Success is type(success_future.value)
    assert 1 == success_future.value.get()


def test_on_complete():
    from typing import Union

    from category import Failure, Future
    from category import ThreadPoolExecutionContext as ec
    from category import Try

    def functor(try_: Try[int]) -> Union[Exception, int]:
        if isinstance(try_, Failure):
            return try_.value
        else:
            return try_.get_or_else(lambda: 0) + 1

    true_future = Future.successful(value=1)
    true_future.on_complete(functor=functor)(ec)
    assert 2 == true_future.result()


def test_successful():
    from category import Future, Success

    success_future = Future[bool].successful(value=True)
    assert Future is type(success_future)
    assert True is success_future.result()
    assert Success(value=True) == success_future.value
    assert True is success_future.value.get()


def test_hold():
    from category import Failure, Future, Success
    from category import ThreadPoolExecutionContext as ec

    @Future.hold
    def multi_context(value: int) -> int:
        if 0 < value:
            return value
        else:
            raise Exception(value)

    # Failure case
    failure_future = multi_context(value=0)(ec)
    assert Future is type(failure_future)
    assert Failure is type(failure_future.value)
    assert Exception is type(failure_future.value.value)

    # Success case
    success_future = multi_context(value=1)(ec)
    assert Future is type(success_future)
    assert 1 == success_future.result()
    assert Success is type(success_future.value)
    assert 1 == success_future.value.get()


def test_do():
    from category import Failure, Future, FutureDo, Success
    from category import ThreadPoolExecutionContext as ec

    @Future.hold
    def multi_context(value: int) -> int:
        if 0 < value:
            return value
        else:
            raise Exception(value)

    # Failure case
    @Future.do
    def failure_context() -> FutureDo[int]:
        one = yield from multi_context(value=1)(ec)()
        two = 2
        three = yield from multi_context(value=0)(ec)()
        return one + two + three

    assert Future is type(failure_context())
    try:
        failure_context().result()
        assert False
    except Exception:
        assert True
    assert Failure is type(failure_context().value)
    assert Exception is type(failure_context().value.value)

    # Success case
    @Future.do
    def success_context() -> FutureDo[int]:
        one = yield from multi_context(value=1)(ec)()
        two = 2
        three = yield from multi_context(value=3)(ec)()
        return one + two + three

    assert Future is type(success_context())
    assert 6 == success_context().result()
    assert Success is type(success_context().value)
    assert 6 == success_context().value.get()


def test_method():
    from category import Failure, Future, Success

    def to_failure(future: Future[int]) -> Future[int]:
        try:
            future.result()
            failure = Future[int]()
            failure.set_exception(exception=Exception())
            return failure
        except Exception as error:
            failure = Future[int]()
            failure.set_exception(exception=error)
            return failure

    def to_success(future: Future[int]) -> Future[int]:
        try:
            value = future.result()
            return Future[int].successful(value=value)
        except Exception:
            return Future[int].successful(value=1)

    failure = Future[int]()
    failure.set_exception(exception=Exception())
    success = Future[int].successful(value=1)
    assert Future is type(failure.method(to_failure))
    assert Failure is type(failure.method(to_failure).value)
    assert Future is type(failure.method(to_success))
    assert Success is type(failure.method(to_success).value)
    assert Future is type(success.method(to_failure))
    assert Failure is type(success.method(to_failure).value)
    assert Future is type(success.method(to_success))
    assert Success is type(success.method(to_success).value)
