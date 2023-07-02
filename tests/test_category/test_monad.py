def test_do():
    from category import (
        Either,
        EitherDo,
        Option,
        OptionDo,
        Right,
        Some,
        Success,
        Try,
        TryDo,
    )

    @Either.do
    def either_context() -> EitherDo[IndexError | KeyError, int]:
        _ = 42
        result = yield from Right[IndexError, int](42)
        _ = True
        _ = yield from Right[KeyError, int](42)
        _ = yield from Right[IndexError, bool](True)
        return result

    assert 42 == either_context().get()

    @Option.do
    def option_context() -> OptionDo[int]:
        _ = 42
        result = yield from Some[int](42)
        _ = True
        _ = yield from Some[bool](True)
        return result

    assert 42 == option_context().get()

    @Try.do
    def try_context() -> TryDo[int]:
        _ = 42
        result = yield from Success[int](42)
        _ = True
        _ = yield from Success[bool](True)
        return result

    assert 42 == try_context().get()
