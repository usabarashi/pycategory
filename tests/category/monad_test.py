def test_do():
    from category import (
        Either,
        EitherDo,
        EitherTFuture,
        EitherTFutureDo,
        EitherTTry,
        EitherTTryDo,
        Future,
        FutureDo,
        Monad,
        OptionDo,
        Right,
        Some,
        Success,
        TryDo,
    )

    @Monad.do
    def either_context() -> EitherDo[IndexError | KeyError, int]:
        _ = 42
        result = yield from Right[IndexError, int](42)
        _ = True
        _ = yield from Right[KeyError, int](42)
        _ = yield from Right[IndexError, bool](True)
        return result

    assert 42 == either_context().get()

    @Monad.do
    def option_context() -> OptionDo[int]:
        _ = 42
        result = yield from Some[int](42)
        _ = True
        _ = yield from Some[bool](True)
        return result

    assert 42 == option_context().get()

    @Monad.do
    def try_context() -> TryDo[int]:
        _ = 42
        result = yield from Success[int](42)
        _ = True
        _ = yield from Success[bool](True)
        return result

    assert 42 == try_context().get()

    @Monad.do
    def future_context() -> FutureDo[int]:
        _ = 42
        result = yield from Future[int].successful(42)
        _ = True
        _ = yield from Future[bool].successful(True)
        return result

    assert 42 == future_context().result()

    @Monad.do
    def eitherttry_context() -> EitherTTryDo[ValueError | Exception, int]:
        _ = 42
        result = yield from EitherTTry[Exception, int](
            Success[Either[Exception, int]](Right[Exception, int](42))
        )
        _ = True
        _ = yield from EitherTTry[Exception, bool](
            Success[Either[Exception, bool]](Right[Exception, bool](True))
        )
        return result

    assert 42 == eitherttry_context().get()

    @Monad.do
    def eithertfuture_context() -> EitherTFutureDo[Exception, int]:
        _ = 42
        result = yield from EitherTFuture[Exception, int](
            Future[Either[Exception, int]].successful(Right[Exception, int](42))
        )
        _ = True
        _ = yield from EitherTFuture[Exception, bool](
            Future[Either[Exception, bool]].successful(Right[Exception, bool](True))
        )
        return result

    assert 42 == eithertfuture_context().get()
