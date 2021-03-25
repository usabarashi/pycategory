def test_map():

    from category import Future
    from category import ThreadPoolExecutionContext as ec

    success_future = Future.successful(1)
    mapped_future = success_future.map(functor=lambda success: success + 1, ec=ec)
    assert success_future is not mapped_future
    assert isinstance(mapped_future, Future)
    assert 2 == mapped_future.result()


def test_try_complete():
    from category import Future, Success

    true_future = Future.successful(1)
    assert False is true_future.try_complete(result=Success(value=0))
    assert 1 == true_future.result()


def test_on_complete():
    from typing import TypeVar, Union

    from category import Failure, Future, ThreadPoolExecutionContext, TryST

    T = TypeVar("T")

    def functor(try_: TryST[T]) -> Union[Exception, int]:
        if isinstance(try_, Failure):
            return try_.value
        else:
            return try_.get_or_else(0) + 1

    true_future = Future.successful(1)
    true_future.on_complete(
        functor=functor,
        ec=ThreadPoolExecutionContext,
    )
    assert 2 == true_future.result()


def test_successful():
    from category import Future, Success

    future = Future.successful(True)
    assert Success(value=True) == future.value
    assert True is future.value.value

    assert True is future.result()
