def test_map():

    from category import Failure, Future, Success
    from category import ThreadPoolExecutionContext as ec

    # Failure case
    failure_future = Future[int]()
    failure_future.set_exception(exception=Exception())
    failure_mapped_future = failure_future.map(functor=lambda success: success + 1)(
        ec=ec
    )
    assert failure_future is not failure_mapped_future
    assert Future is type(failure_mapped_future)
    try:
        failure_mapped_future.result()
        assert False
    except Exception:
        assert True
    assert Failure is type(failure_mapped_future.value)
    assert Exception is type(failure_mapped_future.value.value)

    # Success case
    success_future = Future.successful(1)
    success_mapped_future = success_future.map(functor=lambda success: success + 1)(
        ec=ec
    )
    assert success_future is not success_mapped_future
    assert Future is type(success_mapped_future)
    assert 2 == success_mapped_future.result()
    assert Success is type(success_mapped_future.value)
    assert 2 == success_mapped_future.value.value


def test_flatmap():
    from category import Failure, Future, Success
    from category import ThreadPoolExecutionContext as ec

    # Failure case
    failure_future = Future[int]()
    failure_future.set_exception(exception=Exception())
    failure_flatmapped_future = failure_future.flatmap(
        functor=lambda success: Future[int].successful(value=success + 1)
    )(ec=ec)
    assert failure_future is not failure_flatmapped_future
    assert Future is type(failure_flatmapped_future)
    try:
        failure_flatmapped_future.result()
        assert False
    except Exception:
        assert True
    assert Failure is type(failure_flatmapped_future.value)
    assert Exception is type(failure_flatmapped_future.value.value)

    # Success case
    success_future = Future[int].successful(1)
    success_flatmapped_future = success_future.flatmap(
        functor=lambda success: Future[int].successful(value=success + 1)
    )(ec=ec)
    assert success_future is not success_flatmapped_future
    assert Future is type(success_flatmapped_future)
    assert 2 == success_flatmapped_future.result()
    assert Success is type(success_flatmapped_future.value)
    assert 2 == success_flatmapped_future.value.value


def test_try_complete():
    from category import Failure, Future, Success

    # Failure case
    failure_future = Future[int]()
    failure_future.set_exception(exception=Exception())
    assert False is failure_future.try_complete(result=Success(value=1))
    try:
        failure_future.result()
        assert False
    except Exception:
        assert True
    assert Failure is type(failure_future.value)
    assert Exception is type(failure_future.value.value)

    # Success case
    success_future = Future[int].successful(value=1)
    assert False is success_future.try_complete(result=Success(value=2))
    assert 1 == success_future.result()
    assert Success is type(success_future.value)
    assert 1 == success_future.value.value


def test_on_complete():
    from typing import Union

    from category import Failure, Future
    from category import ThreadPoolExecutionContext as ec
    from category import TryST

    def functor(try_: TryST[int]) -> Union[Exception, int]:
        if isinstance(try_, Failure):
            return try_.value
        else:
            return try_.get_or_else(lambda: 0) + 1

    true_future = Future.successful(1)
    true_future.on_complete(functor=functor)(ec=ec)
    assert 2 == true_future.result()


def test_successful():
    from category import Future, Success

    success_future = Future[bool].successful(value=True)
    assert Future is type(success_future)
    assert True is success_future.result()
    assert Success(value=True) == success_future.value
    assert True is success_future.value.value


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
    failure_future = multi_context(value=0)(ec=ec)
    assert Future is type(failure_future)
    assert Failure is type(failure_future.value)
    assert Exception is type(failure_future.value.value)

    # Success case
    success_future = multi_context(value=1)(ec=ec)
    assert Future is type(success_future)
    assert 1 == success_future.result()
    assert Success is type(success_future.value)
    assert 1 == success_future.value.value


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
        one = yield from multi_context(value=1)(ec=ec)()
        two = 2
        three = yield from multi_context(value=0)(ec=ec)()
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
        one = yield from multi_context(value=1)(ec=ec)()
        two = 2
        three = yield from multi_context(value=3)(ec=ec)()
        return one + two + three

    assert Future is type(success_context())
    assert 6 == success_context().result()
    assert Success is type(success_context().value)
    assert 6 == success_context().value.value
