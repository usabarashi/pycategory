def test_eitherttry_map():
    from category import EitherST, EitherTTry, Failure, Left, Right, Success

    # Failure case
    failure = EitherTTry[Exception, int](
        value=Failure[EitherST[Exception, int]](value=Exception())
    )
    mapped_failure = failure.map(functor=lambda right: right + 1)
    assert failure is not mapped_failure
    assert EitherTTry is type(mapped_failure)
    assert Failure is type(mapped_failure.value)

    # Success[Left[L, R]] case
    success_left = EitherTTry[Exception, int](
        value=Success(value=Left[Exception, int](value=Exception()))
    )
    mapped_success_left = success_left.map(functor=lambda right: right + 1)
    assert success_left is not mapped_success_left
    assert EitherTTry is type(mapped_success_left)
    assert Success is type(mapped_success_left.value)
    assert Left is type(mapped_success_left.value.value)
    assert Exception is type(mapped_success_left.value.value.value)

    # Success[Right[L, R]] case
    success_right = EitherTTry[Exception, int](
        value=Success(value=Right[Exception, int](value=1))
    )
    mapped_success_right = success_right.map(functor=lambda right: right + 1)
    assert success_right is not mapped_success_right
    assert EitherTTry is type(mapped_success_right)
    assert Success is type(mapped_success_right.value)
    assert Right is type(mapped_success_right.value.value)
    assert 2 == mapped_success_right.value.value.value


def test_eitherttry_flatmap():
    from category import EitherST, EitherTTry, Failure, Left, Right, Success

    # Failure case
    failure = EitherTTry[Exception, int](
        value=Failure[EitherST[Exception, int]](value=Exception())
    )
    flatmapped_failure = failure.flatmap(
        functor=lambda right: EitherTTry[Exception, int](
            value=Failure(value=Exception())
        )
    )
    assert failure is not flatmapped_failure
    assert EitherTTry is type(flatmapped_failure)
    assert Failure is type(flatmapped_failure.value)

    # Success[Left[L, R]] case
    success_left = EitherTTry[Exception, int](
        value=Success(value=Left[Exception, int](value=Exception()))
    )
    flatmapped_success_left = success_left.flatmap(
        functor=lambda right: EitherTTry[Exception, int](
            value=Success(value=Left[Exception, int](value=Exception()))
        )
    )
    assert success_left is not flatmapped_success_left
    assert EitherTTry is type(flatmapped_success_left)
    assert Success is type(flatmapped_success_left.value)
    assert Left is type(flatmapped_success_left.value.value)
    assert Exception is type(flatmapped_success_left.value.value.value)

    # Success[Right[L, R]] case
    success_right = EitherTTry[Exception, int](
        value=Success(value=Right[Exception, int](value=1))
    )
    flatmapped_success_right = success_right.flatmap(
        functor=lambda right: EitherTTry[Exception, int](
            value=Success(value=Right[Exception, int](value=right + 1))
        )
    )
    assert success_right is not flatmapped_success_right
    assert EitherTTry is type(flatmapped_success_right)
    assert Success is type(flatmapped_success_right.value)
    assert Right is type(flatmapped_success_right.value.value)
    assert 2 == flatmapped_success_right.value.value.value


def test_eitherttry_get():
    from category import EitherST, EitherTTry, Failure, Left, Right, Success

    # Failure case
    try:
        EitherTTry[Exception, int](
            value=Failure[EitherST[Exception, int]](value=Exception())
        ).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)

    # Success[Left[L, R]] case
    try:
        EitherTTry[Exception, int](
            value=Success[EitherST[Exception, int]](
                value=Left[Exception, int](value=Exception())
            )
        ).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)

    # Success[Right[L, R]] case
    assert (
        1
        == EitherTTry[Exception, int](
            value=Success[EitherST[Exception, int]](
                value=Right[Exception, int](value=1)
            )
        ).get()
    )


def test_eitherttry_getorelse():
    from category import EitherST, EitherTTry, Failure, Left, Right, Success

    # Failure case
    assert False is EitherTTry[Exception, int](
        value=Failure[EitherST[Exception, int]](value=Exception())
    ).get_or_else(lambda: False)

    # Success[Left[L, R]] case
    assert False is EitherTTry[Exception, int](
        value=Success[EitherST[Exception, int]](
            value=Left[Exception, int](value=Exception())
        )
    ).get_or_else(lambda: False)

    # Success[Right[L, R]] case
    assert 1 == EitherTTry[Exception, int](
        value=Success[EitherST[Exception, int]](value=Right[Exception, int](value=1))
    ).get_or_else(lambda: False)


def test_eitherttry_do():
    from category import EitherTTry, EitherTTryDo, Failure, Left, Right, Success

    # Failrue case
    @EitherTTry.do
    def failure_context() -> EitherTTryDo[Exception, int]:
        one = yield from EitherTTry[Exception, int](
            value=Success(value=Right[Exception, int](value=1))
        )()
        two = 2
        three = yield from EitherTTry[Exception, int](
            value=Failure(value=Exception())
        )()
        return one + two + three

    assert EitherTTry is type(failure_context())
    try:
        failure_context().get()
        assert False
    except Exception as error:
        ValueError is type(error)
    assert Failure is type(failure_context().value)
    assert Exception is type(failure_context().value.value)

    @EitherTTry.do
    def failure_convert_context() -> EitherTTryDo[Exception, int]:
        one = yield from EitherTTry[Exception, int](
            value=Success(value=Right[Exception, int](value=1))
        )()
        two = 2
        three = yield from EitherTTry[Exception, int](value=Failure(value=Exception()))(
            convert=lambda exception: Failure[Left[Exception, int]](value=Exception())
        )
        return one + two + three

    assert EitherTTry is type(failure_convert_context())
    try:
        failure_convert_context().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert Failure is type(failure_convert_context().value)
    assert Exception is type(failure_convert_context().value.value)

    # Success[Left[L, R]] case
    @EitherTTry.do
    def success_left_context() -> EitherTTryDo[Exception, int]:
        one = yield from EitherTTry[Exception, int](
            value=Success(value=Right[Exception, int](value=1))
        )()
        two = 2
        three = yield from EitherTTry[Exception, int](
            value=Success(value=Left[Exception, int](value=Exception()))
        )()
        return one + two + three

    assert EitherTTry is type(success_left_context())
    try:
        success_left_context().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert Success is type(success_left_context().value)
    assert Left is type(success_left_context().value.value)
    assert Exception is type(success_left_context().value.value.value)

    @EitherTTry.do
    def success_left_convert_context() -> EitherTTryDo[Exception, int]:
        one = yield from EitherTTry[Exception, int](
            value=Success(value=Right[Exception, int](value=1))
        )()
        two = 2
        three = yield from EitherTTry[Exception, int](
            value=Success(value=Left[Exception, int](value=Exception()))
        )(
            convert=Success[Left[Exception, int]](
                value=Left[Exception, int](value=Exception())
            )
        )
        return one + two + three

    try:
        success_left_convert_context().get()
        assert False
    except BaseException as error:
        assert GeneratorExit is type(error)

    # Success[Right[L, R]] case
    @EitherTTry.do
    def success_right_context() -> EitherTTryDo[Exception, int]:
        one = yield from EitherTTry[Exception, int](
            value=Success(value=Right[Exception, int](value=1))
        )()
        two = 2
        three = yield from EitherTTry[Exception, int](
            value=Success(value=Right[Exception, int](value=3))
        )()
        return one + two + three

    assert EitherTTry is type(success_right_context())
    assert 6 == success_right_context().get()
    assert Success is type(success_right_context().value)
    assert Right is type(success_right_context().value.value)
    assert 6 == success_right_context().value.value.value

    @EitherTTry.do
    def success_right_convert_context() -> EitherTTryDo[Exception, int]:
        one = yield from EitherTTry[Exception, int](
            value=Success(value=Right[Exception, int](value=1))
        )()
        two = 2
        three = yield from EitherTTry[Exception, int](
            value=Success(value=Right[Exception, int](value=3))
        )(
            convert=lambda success_right: Success[Right[Exception, int]](
                value=Right[Exception, int](value=3)
            )
        )
        return one + two + three

    try:
        success_right_convert_context()
        assert False
    except BaseException as error:
        assert GeneratorExit is type(error)


def test_eithertfuture_get():
    from category import EitherST, EitherTFuture, Future, Left, Right

    # Failure case
    failure_future = Future[EitherST[Exception, int]]()
    failure_future.set_exception(exception=Exception())
    try:
        EitherTFuture[Exception, int](value=failure_future).get()
        assert False
    except Exception as error:
        assert Exception is type(error)

    # Success[Left[L, R]] case
    try:
        EitherTFuture[Exception, int](
            value=Future[EitherST[Exception, int]].successful(
                value=Left[Exception, int](value=Exception())
            )
        ).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)

    # Success[Right[L, R]] case
    assert (
        1
        == EitherTFuture[Exception, int](
            value=Future[EitherST[Exception, int]].successful(
                value=Right[Exception, int](value=1)
            )
        ).get()
    )


def test_eithertfuture_getorelse():
    from category import EitherST, EitherTFuture, Future, Left, Right

    # Failure case
    failure_future = Future[EitherST[Exception, int]]()
    failure_future.set_exception(exception=Exception())
    assert False is EitherTFuture[Exception, int](value=failure_future).get_or_else(
        default=lambda: False
    )

    # Success[Left[L, R]] case
    assert False is EitherTFuture[Exception, int](
        value=Future[EitherST[Exception, int]].successful(
            value=Left[Exception, int](value=Exception())
        )
    ).get_or_else(default=lambda: False)

    # Success[Right[L, R]] case
    assert 1 == EitherTFuture[Exception, int](
        value=Future[EitherST[Exception, int]].successful(
            value=Right[Exception, int](value=1)
        )
    ).get_or_else(default=lambda: False)


def test_eithertfuture_map():
    from category import EitherST, EitherTFuture
    from category import ExecutionContext as ec
    from category import Future, Left, Right

    # Failure case
    failure_future = Future[EitherST[Exception, int]]()
    failure_future.set_exception(exception=Exception())
    failure = EitherTFuture[Exception, int](value=failure_future)
    mapped_failure = failure.map(functor=lambda right: right + 1)(ec=ec)
    assert failure is not mapped_failure
    assert EitherTFuture is type(mapped_failure)
    assert False is mapped_failure.get_or_else(default=lambda: False)
    try:
        mapped_failure.value.result()
        assert False
    except Exception as error:
        assert Exception is type(error)

    # Success[Left[L, R]] case
    left = EitherTFuture[Exception, int](
        value=Future[EitherST[Exception, int]].successful(
            value=Left[Exception, int](value=Exception())
        )
    )
    mapped_left = left.map(functor=lambda right: right + 1)(ec=ec)
    assert left is not mapped_left
    assert EitherTFuture is type(mapped_left)
    assert False is mapped_left.get_or_else(default=lambda: False)
    assert Left is type(mapped_left.value.result())
    assert Exception is type(mapped_left.value.result().value)

    # Success[Right[L, R]] case
    right = EitherTFuture[Exception, int](
        value=Future[EitherST[Exception, int]].successful(
            value=Right[Exception, int](value=1)
        )
    )
    mapped_right = right.map(functor=lambda right: right + 1)(ec=ec)
    assert right is not mapped_right
    assert EitherTFuture is type(mapped_right)
    assert 2 == mapped_right.get()
    assert Right is type(mapped_right.value.result())
    assert 2 == mapped_right.value.result().value


def test_eithertfuture_flatmap():
    from category import EitherST, EitherTFuture
    from category import ExecutionContext as ec
    from category import Future, Left, Right

    # Failure case
    failure_future = Future[EitherST[Exception, int]]()
    failure_future.set_exception(exception=Exception())
    failure = EitherTFuture[Exception, int](value=failure_future)
    mapped_failure = failure.flatmap(
        functor=lambda right: EitherTFuture[Exception, int](
            Future[EitherST[Exception, int]].successful(Right[Exception, int](1))
        )
    )(ec=ec)
    assert failure is not mapped_failure
    assert EitherTFuture is type(mapped_failure)
    assert False is mapped_failure.get_or_else(default=lambda: False)
    try:
        mapped_failure.value.result()
        assert False
    except Exception as error:
        assert Exception is type(error)

    # Success[Left[L, R]] case
    left = EitherTFuture[Exception, int](
        value=Future[EitherST[Exception, int]].successful(
            value=Left[Exception, int](value=Exception())
        )
    )
    mapped_left = left.flatmap(
        functor=lambda right: EitherTFuture[Exception, int](
            value=Future[EitherST[Exception, int]].successful(
                value=Right[Exception, int](value=right + 1)
            )
        )
    )(ec=ec)
    assert left is not mapped_left
    assert EitherTFuture is type(mapped_left)
    assert False is mapped_left.get_or_else(default=lambda: False)
    assert Left is type(mapped_left.value.result())
    assert Exception is type(mapped_left.value.result().value)

    # Success[Right[L, R]] case
    right = EitherTFuture[Exception, int](
        value=Future[EitherST[Exception, int]].successful(
            value=Right[Exception, int](value=1)
        )
    )
    flatmapped_right = right.flatmap(
        functor=lambda right: EitherTFuture[Exception, int](
            value=Future[EitherST[Exception, int]].successful(
                value=Right[Exception, int](value=right + 1)
            )
        )
    )(ec=ec)
    assert right is not flatmapped_right
    assert EitherTFuture is type(flatmapped_right)
    assert 2 == flatmapped_right.get()
    assert Right is type(flatmapped_right.value.result())
    assert 2 == flatmapped_right.value.result().value


def test_eithertfuture_do():
    from category import (
        EitherST,
        EitherTFuture,
        EitherTFutureDo,
        Future,
        Left,
        Right,
        Success,
    )

    # Failrue case
    @EitherTFuture.do
    def failure_context() -> EitherTFutureDo[Exception, int]:
        one = yield from EitherTFuture[Exception, int](
            value=Future[EitherST[Exception, int]].successful(
                value=Right[Exception, int](value=1)
            )
        )()
        two = 2
        future = Future[EitherST[Exception, int]]()
        future.set_exception(exception=Exception())
        three = yield from EitherTFuture[Exception, int](value=future)()
        return one + two + three

    try:
        EitherTFuture is type(failure_context())
        assert False
    except BaseException as error:
        assert GeneratorExit is type(error)

    @EitherTFuture.do
    def if_failure_then_context() -> EitherTFutureDo[Exception, int]:
        one = yield from EitherTFuture[Exception, int](
            value=Future[EitherST[Exception, int]].successful(
                value=Right[Exception, int](value=1)
            )
        )()
        two = 2
        future = Future[EitherST[Exception, int]]()
        future.set_exception(exception=Exception())
        three = yield from EitherTFuture[Exception, int](value=future)(
            convert=lambda exception: Success(Left[Exception, int](value=Exception()))
        )
        return one + two + three

    assert EitherTFuture is type(if_failure_then_context())
    try:
        if_failure_then_context().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert Future is type(if_failure_then_context().value)
    assert Left is type(if_failure_then_context().value._result)
    assert Exception is type(if_failure_then_context().value._result.value)

    # Success[Left[L, R]] case
    @EitherTFuture.do
    def success_left_context() -> EitherTFutureDo[Exception, int]:
        one = yield from EitherTFuture[Exception, int](
            value=Future[EitherST[Exception, int]].successful(
                value=Right[Exception, int](value=1)
            )
        )()
        two = 2
        three = yield from EitherTFuture[Exception, int](
            value=Future[EitherST[Exception, int]].successful(
                value=Left[Exception, int](value=Exception())
            )
        )()
        return one + two + three

    assert EitherTFuture is type(success_left_context())
    try:
        success_left_context().get()
        assert False
    except Exception as error:
        assert ValueError is type(error)
    assert Future is type(success_left_context().value)
    assert Left is type(success_left_context().value._result)
    assert Exception is type(success_left_context().value._result.value)

    # Success[Right[L, R]] case
    @EitherTFuture.do
    def success_right_context() -> EitherTFutureDo[Exception, int]:
        one = yield from EitherTFuture[Exception, int](
            value=Future[EitherST[Exception, int]].successful(
                value=Right[Exception, int](value=1)
            )
        )()
        two = 2
        three = yield from EitherTFuture[Exception, int](
            value=Future[EitherST[Exception, int]].successful(
                value=Right[Exception, int](value=3)
            )
        )()
        return one + two + three

    assert EitherTFuture is type(success_right_context())
    assert 6 == success_right_context().get()
    assert Future is type(success_right_context().value)
    assert Right is type(success_right_context().value._result)
    assert 6 == success_right_context().value._result.value
