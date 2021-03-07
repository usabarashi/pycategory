def test_future():
    from category import Failure, Future, Success, TryST

    def add_one(try_: TryST[int]) -> TryST[int]:
        if isinstance(try_, Failure):
            return Success(value=0)
        else:
            return Success(value=try_.value + 1)

    def add_two_flat(try_: TryST[int]) -> Future[int]:
        if isinstance(try_, Failure):
            return Future.successful(value=0)
        else:
            return Future.successful(value=try_.value + 2)

    assert Future is type(Future[int].successful(1).transform(add_one))
    assert 2 == Future[int].successful(1).transform(add_one).value.value
    assert Future is type(
        Future[int].successful(1).transform(add_one).transform_with(add_two_flat)
    )
    assert (
        4
        == Future[int]
        .successful(1)
        .transform(add_one)
        .transform_with(add_two_flat)
        .value.value
    )
