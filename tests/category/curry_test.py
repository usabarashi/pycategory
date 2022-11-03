def test_curried():
    from category import curried

    @curried
    def curry2(arg1: int, arg2: int) -> int:
        return arg1 + arg2

    _ = curry2
    assert int is type(curry2(1)(1))
    assert 2 == curry2(1)(1)

    @curried
    def curry3(arg1: int, /, arg2: int, arg3: int) -> int:
        return arg1 + arg2 + arg3

    _ = curry3
    assert int is type(curry3(1)(1)(1))
    assert 3 == curry3(1)(1)(1)

    @curried
    def curry4(arg1: int, /, arg2: int, arg3: int, arg4: int) -> int:
        return arg1 + arg2 + arg3 + arg4

    _ = curry4
    assert int is type(curry4(1)(1)(1)(1))
    assert 4 == curry4(1)(1)(1)(1)

    @curried
    def curry5(arg1: int, /, arg2: int, arg3: int, arg4: int, arg5: int) -> int:
        return arg1 + arg2 + arg3 + arg4 + arg5

    _ = curry5
    assert int is type(curry5(1)(1)(1)(1)(1))
    assert 5 == curry5(1)(1)(1)(1)(1)

    @curried
    def curry6(
        arg1: int, /, arg2: int, arg3: int, arg4: int, arg5: int, arg6: int
    ) -> int:
        return arg1 + arg2 + arg3 + arg4 + arg5 + arg6

    _ = curry6
    assert int is type(curry6(1)(1)(1)(1)(1)(1))
    assert 6 == curry6(1)(1)(1)(1)(1)(1)

    @curried
    def curry7(
        arg1: int,
        /,
        arg2: int,
        arg3: int,
        arg4: int,
        arg5: int,
        arg6: int,
        arg7: int,
    ) -> int:
        return arg1 + arg2 + arg3 + arg4 + arg5 + arg6 + arg7

    _ = curry7
    assert int is type(curry7(1)(1)(1)(1)(1)(1)(1))
    assert 7 == curry7(1)(1)(1)(1)(1)(1)(1)

    @curried
    def curry8(
        arg1: int,
        /,
        arg2: int,
        arg3: int,
        arg4: int,
        arg5: int,
        arg6: int,
        arg7: int,
        arg8: int,
    ) -> int:
        return arg1 + arg2 + arg3 + arg4 + arg5 + arg6 + arg7 + arg8

    _ = curry8
    assert int is type(curry8(1)(1)(1)(1)(1)(1)(1)(1))
    assert 8 == curry8(1)(1)(1)(1)(1)(1)(1)(1)

    @curried
    def curry9(
        arg1: int,
        /,
        arg2: int,
        arg3: int,
        arg4: int,
        arg5: int,
        arg6: int,
        arg7: int,
        arg8: int,
        arg9: int,
    ) -> int:
        return arg1 + arg2 + arg3 + arg4 + arg5 + arg6 + arg7 + arg8 + arg9

    _ = curry9
    assert int is type(curry9(1)(1)(1)(1)(1)(1)(1)(1)(1))
    assert 9 == curry9(1)(1)(1)(1)(1)(1)(1)(1)(1)

    @curried
    def curry10(
        arg1: int,
        /,
        arg2: int,
        arg3: int,
        arg4: int,
        arg5: int,
        arg6: int,
        arg7: int,
        arg8: int,
        arg9: int,
        arg10: int,
    ) -> int:
        return arg1 + arg2 + arg3 + arg4 + arg5 + arg6 + arg7 + arg8 + arg9 + arg10

    _ = curry10
    assert int is type(curry10(1)(1)(1)(1)(1)(1)(1)(1)(1)(1))
    assert 10 == curry10(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)

    @curried
    def curry11(
        arg1: int,
        /,
        arg2: int,
        arg3: int,
        arg4: int,
        arg5: int,
        arg6: int,
        arg7: int,
        arg8: int,
        arg9: int,
        arg10: int,
        arg11: int,
    ) -> int:
        return (
            arg1 + arg2 + arg3 + arg4 + arg5 + arg6 + arg7 + arg8 + arg9 + arg10 + arg11
        )

    _ = curry11
    assert int is type(curry11(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1))
    assert 11 == curry11(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)

    @curried
    def curry12(
        arg1: int,
        arg2: int,
        arg3: int,
        arg4: int,
        arg5: int,
        arg6: int,
        arg7: int,
        arg8: int,
        arg9: int,
        arg10: int,
        arg11: int,
        arg12: int,
    ) -> int:
        return (
            arg1
            + arg2
            + arg3
            + arg4
            + arg5
            + arg6
            + arg7
            + arg8
            + arg9
            + arg10
            + arg11
            + arg12
        )

    _ = curry12
    assert int is type(curry12(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1))
    assert 12 == curry12(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)

    @curried
    def curry13(
        arg1: int,
        arg2: int,
        arg3: int,
        arg4: int,
        arg5: int,
        arg6: int,
        arg7: int,
        arg8: int,
        arg9: int,
        arg10: int,
        arg11: int,
        arg12: int,
        arg13: int,
    ) -> int:
        return (
            arg1
            + arg2
            + arg3
            + arg4
            + arg5
            + arg6
            + arg7
            + arg8
            + arg9
            + arg10
            + arg11
            + arg12
            + arg13
        )

    _ = curry13
    assert int is type(curry13(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1))
    assert 13 == curry13(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)

    @curried
    def curry14(
        arg1: int,
        arg2: int,
        arg3: int,
        arg4: int,
        arg5: int,
        arg6: int,
        arg7: int,
        arg8: int,
        arg9: int,
        arg10: int,
        arg11: int,
        arg12: int,
        arg13: int,
        arg14: int,
    ) -> int:
        return (
            arg1
            + arg2
            + arg3
            + arg4
            + arg5
            + arg6
            + arg7
            + arg8
            + arg9
            + arg10
            + arg11
            + arg12
            + arg13
            + arg14
        )

    _ = curry14
    assert int is type(curry14(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1))
    assert 14 == curry14(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)

    @curried
    def curry14p(
        arg1: int,
        arg2: int,
        arg3: int,
        arg4: int,
        arg5: int,
        arg6: int,
        arg7: int,
        arg8: int,
        arg9: int,
        arg10: int,
        arg11: int,
        arg12: int,
        arg13: int,
        arg14: int,
        arg15: int = 0,
    ) -> int:
        return (
            arg1
            + arg2
            + arg3
            + arg4
            + arg5
            + arg6
            + arg7
            + arg8
            + arg9
            + arg10
            + arg11
            + arg12
            + arg13
            + arg14
            + arg15
        )

    _ = curry14p
    assert int is type(curry14p(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1))
    assert 14 == curry14p(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)(1)

    try:

        @curried
        def curry15(
            arg1: int,
            arg2: int,
            arg3: int,
            arg4: int,
            arg5: int,
            arg6: int,
            arg7: int,
            arg8: int,
            arg9: int,
            arg10: int,
            arg11: int,
            arg12: int,
            arg13: int,
            arg14: int,
            arg15: int,
        ) -> int:
            return (
                arg1
                + arg2
                + arg3
                + arg4
                + arg5
                + arg6
                + arg7
                + arg8
                + arg9
                + arg10
                + arg11
                + arg12
                + arg13
                + arg14
                + arg15
            )
            ...

        assert False
    except Exception:
        assert True
