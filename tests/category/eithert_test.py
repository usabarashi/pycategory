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
        assert ValueError is type(error)
    assert Failure is type(failure_context().value)
    assert Exception is type(failure_context().value.value)

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
