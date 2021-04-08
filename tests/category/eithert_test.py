def test_eitherttry_map():
    from category import Either, EitherTTry, Failure, Left, Right, Success

    # Failure case
    failure = EitherTTry[Exception, int](
        value=Failure[Either[Exception, int]](value=Exception())
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
    from category import Either, EitherTTry, Failure, Left, Right, Success

    # Failure case
    failure = EitherTTry[Exception, int](
        value=Failure[Either[Exception, int]](value=Exception())
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
    from category import Either, EitherTTry, Failure, Left, Right, Success

    # Failure case
    try:
        EitherTTry[Exception, int](
            value=Failure[Either[Exception, int]](value=Exception())
        ).get()
        assert False
    except Exception as error:
        assert ValueError is type(error)

    # Success[Left[L, R]] case
    try:
        EitherTTry[Exception, int](
            value=Success[Either[Exception, int]](
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
            value=Success[Either[Exception, int]](value=Right[Exception, int](value=1))
        ).get()
    )


def test_eitherttry_getorelse():
    from category import Either, EitherTTry, Failure, Left, Right, Success

    # Failure case
    assert False is EitherTTry[Exception, int](
        value=Failure[Either[Exception, int]](value=Exception())
    ).get_or_else(lambda: False)

    # Success[Left[L, R]] case
    assert False is EitherTTry[Exception, int](
        value=Success[Either[Exception, int]](
            value=Left[Exception, int](value=Exception())
        )
    ).get_or_else(lambda: False)

    # Success[Right[L, R]] case
    assert 1 == EitherTTry[Exception, int](
        value=Success[Either[Exception, int]](value=Right[Exception, int](value=1))
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
    from category import Either, EitherTFuture, Future, Left, Right

    # Failure case
    failure_future = Future[Either[Exception, int]]()
    failure_future.set_exception(exception=Exception())
    try:
        EitherTFuture[Exception, int](value=failure_future).get()
        assert False
    except Exception as error:
        assert Exception is type(error)

    # Success[Left[L, R]] case
    try:
        EitherTFuture[Exception, int](
            value=Future[Either[Exception, int]].successful(
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
            value=Future[Either[Exception, int]].successful(
                value=Right[Exception, int](value=1)
            )
        ).get()
    )


def test_eithertfuture_getorelse():
    from category import Either, EitherTFuture, Future, Left, Right

    # Failure case
    failure_future = Future[Either[Exception, int]]()
    failure_future.set_exception(exception=Exception())
    assert False is EitherTFuture[Exception, int](value=failure_future).get_or_else(
        default=lambda: False
    )

    # Success[Left[L, R]] case
    assert False is EitherTFuture[Exception, int](
        value=Future[Either[Exception, int]].successful(
            value=Left[Exception, int](value=Exception())
        )
    ).get_or_else(default=lambda: False)

    # Success[Right[L, R]] case
    assert 1 == EitherTFuture[Exception, int](
        value=Future[Either[Exception, int]].successful(
            value=Right[Exception, int](value=1)
        )
    ).get_or_else(default=lambda: False)


def test_eithertfuture_map():
    from category import Either, EitherTFuture
    from category import ExecutionContext as ec
    from category import Future, Left, Right

    # Failure case
    failure_future = Future[Either[Exception, int]]()
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
        value=Future[Either[Exception, int]].successful(
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
        value=Future[Either[Exception, int]].successful(
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
    from category import Either, EitherTFuture
    from category import ExecutionContext as ec
    from category import Future, Left, Right

    # Failure case
    failure_future = Future[Either[Exception, int]]()
    failure_future.set_exception(exception=Exception())
    failure = EitherTFuture[Exception, int](value=failure_future)
    mapped_failure = failure.flatmap(
        functor=lambda right: EitherTFuture[Exception, int](
            Future[Either[Exception, int]].successful(Right[Exception, int](1))
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
        value=Future[Either[Exception, int]].successful(
            value=Left[Exception, int](value=Exception())
        )
    )
    mapped_left = left.flatmap(
        functor=lambda right: EitherTFuture[Exception, int](
            value=Future[Either[Exception, int]].successful(
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
        value=Future[Either[Exception, int]].successful(
            value=Right[Exception, int](value=1)
        )
    )
    flatmapped_right = right.flatmap(
        functor=lambda right: EitherTFuture[Exception, int](
            value=Future[Either[Exception, int]].successful(
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
        Either,
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
            value=Future[Either[Exception, int]].successful(
                value=Right[Exception, int](value=1)
            )
        )()
        two = 2
        future = Future[Either[Exception, int]]()
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
            value=Future[Either[Exception, int]].successful(
                value=Right[Exception, int](value=1)
            )
        )()
        two = 2
        future = Future[Either[Exception, int]]()
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
            value=Future[Either[Exception, int]].successful(
                value=Right[Exception, int](value=1)
            )
        )()
        two = 2
        three = yield from EitherTFuture[Exception, int](
            value=Future[Either[Exception, int]].successful(
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
            value=Future[Either[Exception, int]].successful(
                value=Right[Exception, int](value=1)
            )
        )()
        two = 2
        three = yield from EitherTFuture[Exception, int](
            value=Future[Either[Exception, int]].successful(
                value=Right[Exception, int](value=3)
            )
        )()
        return one + two + three

    assert EitherTFuture is type(success_right_context())
    assert 6 == success_right_context().get()
    assert Future is type(success_right_context().value)
    assert Right is type(success_right_context().value._result)
    assert 6 == success_right_context().value._result.value


def test_convert():
    from typing import Callable, TypeVar

    from category import (
        Either,
        EitherTFuture,
        Future,
        Left,
        Option,
        Right,
        Success,
        Void,
    )

    T = TypeVar("T")
    L = TypeVar("L")
    R = TypeVar("R")
    E = TypeVar("E")

    def if_left_then(
        report: Callable[[L], E]
    ) -> Callable[[Either[L, R]], EitherTFuture[E, R]]:
        def convert(either: Either[L, R]) -> EitherTFuture[E, R]:
            if isinstance(either.pattern, Left):
                value = report(either.pattern.value)
                left = Left[E, R](value=value)
                future = Future[Either[E, R]].successful(value=left)
                return EitherTFuture[E, R](value=future)
            else:
                right = Right[E, R](value=either.pattern.value)
                future = Future[Either[E, R]].successful(value=right)
                return EitherTFuture[E, R](value=future)

        return convert

    left = Left[Exception, int](value=Exception()).convert(
        functor=if_left_then(report=lambda left: Exception())
    )
    assert EitherTFuture is type(left)
    assert Future is type(left.value)
    assert Success is type(left.value.value)
    assert Left is type(left.value.value.value)
    assert Exception is type(left.value.value.value.value)

    def if_failure_then(
        report: Callable[[Exception], E]
    ) -> Callable[[Future[T]], EitherTFuture[E, T]]:
        def convert(future: Future[T]) -> EitherTFuture[E, T]:
            try:
                value = future.result()
                right = Right[E, T](value=value)
                success = Future[Either[E, T]].successful(value=right)
                return EitherTFuture[E, T](value=success)
            except Exception as error:
                left = Left[E, T](value=error)
                success = Future[Either[E, T]].successful(value=left)
                return EitherTFuture[E, T](value=success)

        return convert

    future = Future[int]()
    future.set_exception(exception=Exception())
    failure = future.convert(
        functor=if_failure_then(report=lambda failure: Exception(failure))
    )
    assert EitherTFuture is type(failure)
    assert Future is type(failure.value)
    assert Success is type(failure.value.value)
    assert Left is type(failure.value.value.value)
    assert Exception is type(failure.value.value.value.value)

    def if_not_exists(
        report: Callable[..., E]
    ) -> Callable[[Future[Option[T]]], EitherTFuture[E, T]]:
        def convert(future: Future[Option[T]]) -> EitherTFuture[E, T]:
            try:
                either = future.result()
                if isinstance(either.pattern, Void):
                    left = Left[E, T](value=report())
                    failure = Future[Either[E, T]].successful(value=left)
                    return EitherTFuture[E, T](value=failure)
                else:
                    right = Right[E, T](value=either.pattern.value)
                    failure = Future[Either[E, T]].successful(value=right)
                    return EitherTFuture[E, T](value=failure)
            except Exception as error:
                left = Left[E, T](value=error)
                success = Future[Either[E, T]].successful(value=left)
                return EitherTFuture[E, T](value=success)

        return convert

    none = (
        Future[Option[int]]
        .successful(value=Void[int]())
        .convert(functor=if_not_exists(report=lambda: Exception()))
    )
    assert EitherTFuture is type(none)
    assert Future is type(none.value)
    assert Success is type(none.value.value)
    assert Left is type(none.value.value.value)
    assert Exception is type(none.value.value.value.value)
