def test_function1():
    from category.function import Function, Function1

    _ = Function1[int, None](lambda: None)
    _ = Function1[int, None](lambda arg1: None)
    _ = Function1[int, None](lambda arg1, arg2: None)
    assert isinstance(Function1[int, None](lambda arg1: None), Function)
    assert Function1 is type(Function1[int, None](lambda arg1: None))

    def func_args0() -> None:
        ...

    def func_args1(arg: int) -> None:
        ...

    def func_args2(arg1: int, arg2: int) -> None:
        ...

    _ = Function1[int, None](func_args0)
    _ = Function1[int, None](func_args1)
    _ = Function1[int, None](func_args2)
    assert isinstance(Function1[int, None](func_args1), Function)
    assert Function1 is type(Function1[int, None](func_args1))


def test_function1___call__():
    from typing import Any

    from category.function import Function1

    result = Function1[Any, None](lambda a: None)(42)
    assert None is result


def test_function1_apply():
    from typing import Any

    from category.function import Function1

    result = Function1[Any, None](lambda a: None).apply(42)
    assert None is result


def test_function1_compose():
    from category.function import Function1

    assert "arg compose2 compose1" == Function1[str, str](
        lambda string: string + " compose1"
    ).compose(Function1[str, str](lambda string: string + " compose2"))("arg")

    assert "arg compose2 compose1" == Function1[str, str](
        lambda string: string + " compose1"
    ).compose(Function1[str, str](lambda string: string + " compose2")).apply("arg")

    assert "arg compose2 compose1" == Function1[str, str](
        lambda string: string + " compose1"
    ).compose(Function1[str, str](lambda string: string + " compose2"))("arg")

    assert "arg compose2 compose1" == Function1[str, str](
        lambda string: string + " compose1"
    ).compose(Function1[str, str](lambda string: string + " compose2")).apply("arg")


def test_function1_and_then():
    from category.function import Function1

    assert "arg and_then1 and_then2" == Function1[str, str](
        lambda string: string + " and_then1"
    ).and_then(Function1[str, str](lambda string: string + " and_then2"))("arg")

    assert "arg and_then1 and_then2" == Function1[str, str](
        lambda string: string + " and_then1"
    ).and_then(Function1[str, str](lambda string: string + " and_then2")).apply("arg")

    assert "arg and_then1 and_then2" == Function1[str, str](
        lambda string: string + " and_then1"
    ).and_then(Function1[str, str](lambda string: string + " and_then2"))("arg")

    assert "arg and_then1 and_then2" == Function1[str, str](
        lambda string: string + " and_then1"
    ).and_then(Function1[str, str](lambda string: string + " and_then2")).apply("arg")


def test_function2():
    from category.function import Function, Function2

    _ = Function2[int, int, None](lambda: None)
    _ = Function2[int, int, None](lambda arg1: None)
    _ = Function2[int, int, None](lambda arg1, arg2: None)
    _ = Function2[int, int, None](lambda arg1, arg2, arg3: None)
    assert isinstance(Function2[int, int, None](lambda arg1, arg2: None), Function)
    assert Function2 is type(Function2[int, int, None](lambda arg1, arg2: None))
    assert None is Function2[int, int, None](lambda arg1, arg2: None)(42, 42)

    def func_args0() -> None:
        ...

    def func_args1(arg1: int) -> None:
        ...

    def func_args2(arg1: int, arg2: int) -> None:
        ...

    def func_args3(arg1: int, arg2: int, arg3: int) -> None:
        ...

    _ = Function2[int, int, None](func_args0)
    _ = Function2[int, int, None](func_args1)
    _ = Function2[int, int, None](func_args2)
    _ = Function2[int, int, None](func_args3)
    assert isinstance(Function2[int, int, None](func_args2), Function)
    assert Function2 is type(Function2[int, int, None](func_args2))
    assert None is Function2[int, int, None](func_args2)(42, 42)
    assert None is Function2[int, int, None](func_args2)(arg1=42, arg2=42)


def test_function2___call__():
    from category.function import Function2

    result = Function2[int, int, None](lambda arg1, arg2: None)(42, 42)
    assert None is result


def test_function2_apply():
    from category.function import Function2

    result = Function2[int, int, None](lambda arg1, arg2: None).apply(42, 42)
    assert None is result


def test_function2_curried():
    from category.function import Function2

    curried = Function2[int, int, None](lambda arg1, arg2: None).curried
    assert None is curried(42)(42)


def test_function2_tupled():
    from category.function import Function2

    tupled = Function2[int, int, None](lambda arg1, arg2: None).tupled
    assert None is tupled((42, 42))


def test_function3():
    from category.function import Function, Function3

    lambda3 = lambda arg1, arg2, arg3: 42
    function3 = Function3[int, int, int, int](lambda3)
    assert isinstance(function3, Function)
    assert 42 == function3(arg1=42, arg2=42, arg3=42)
    assert 42 == function3.apply(arg1=42, arg2=42, arg3=42)
    assert 42 == function3.curried(42)(42)(42)
    assert 42 == function3.tupled((42, 42, 42))


def test_function4():
    from category.function import Function, Function4

    lambda4 = lambda arg1, arg2, arg3, arg4: 42
    function4 = Function4[int, int, int, int, int](lambda4)
    assert isinstance(function4, Function)
    assert 42 == function4(arg1=42, arg2=42, arg3=42, arg4=42)
    assert 42 == function4.apply(arg1=42, arg2=42, arg3=42, arg4=42)
    assert 42 == function4.curried(42)(42)(42)(42)
    assert 42 == function4.tupled((42, 42, 42, 42))


def test_function5():
    from category.function import Function, Function5

    lambda5 = lambda arg1, arg2, arg3, arg4, arg5: 42
    function5 = Function5[int, int, int, int, int, int](lambda5)
    assert isinstance(function5, Function)
    assert 42 == function5(arg1=42, arg2=42, arg3=42, arg4=42, arg5=42)
    assert 42 == function5.apply(arg1=42, arg2=42, arg3=42, arg4=42, arg5=42)
    assert 42 == function5.curried(42)(42)(42)(42)(42)
    assert 42 == function5.tupled((42, 42, 42, 42, 42))


def test_function6():
    from category.function import Function, Function6

    lambda6 = lambda arg1, arg2, arg3, arg4, arg5, arg6: 42
    function6 = Function6[int, int, int, int, int, int, int](lambda6)
    assert isinstance(function6, Function)
    assert 42 == function6(arg1=42, arg2=42, arg3=42, arg4=42, arg5=42, arg6=42)
    assert 42 == function6.apply(arg1=42, arg2=42, arg3=42, arg4=42, arg5=42, arg6=42)
    assert 42 == function6.curried(42)(42)(42)(42)(42)(42)
    assert 42 == function6.tupled((42, 42, 42, 42, 42, 42))


def test_function7():
    from category.function import Function, Function7

    lambda7 = lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7: 42
    function7 = Function7[int, int, int, int, int, int, int, int](lambda7)
    assert isinstance(function7, Function)
    assert 42 == function7(
        arg1=42, arg2=42, arg3=42, arg4=42, arg5=42, arg6=42, arg7=42
    )
    assert 42 == function7.apply(
        arg1=42, arg2=42, arg3=42, arg4=42, arg5=42, arg6=42, arg7=42
    )
    assert 42 == function7.curried(42)(42)(42)(42)(42)(42)(42)
    assert 42 == function7.tupled((42, 42, 42, 42, 42, 42, 42))


def test_function8():
    from category.function import Function, Function8

    lambda8 = lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8: 42
    function8 = Function8[int, int, int, int, int, int, int, int, int](lambda8)
    assert isinstance(function8, Function)
    assert 42 == function8(
        arg1=42, arg2=42, arg3=42, arg4=42, arg5=42, arg6=42, arg7=42, arg8=42
    )
    assert 42 == function8.apply(
        arg1=42, arg2=42, arg3=42, arg4=42, arg5=42, arg6=42, arg7=42, arg8=42
    )
    assert 42 == function8.curried(42)(42)(42)(42)(42)(42)(42)(42)
    assert 42 == function8.tupled((42, 42, 42, 42, 42, 42, 42, 42))


def test_function9():
    from category.function import Function, Function9

    lambda9 = lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9: 42
    function9 = Function9[int, int, int, int, int, int, int, int, int, int](lambda9)
    assert isinstance(function9, Function)
    assert 42 == function9(
        arg1=42, arg2=42, arg3=42, arg4=42, arg5=42, arg6=42, arg7=42, arg8=42, arg9=42
    )
    assert 42 == function9.apply(
        arg1=42, arg2=42, arg3=42, arg4=42, arg5=42, arg6=42, arg7=42, arg8=42, arg9=42
    )
    assert 42 == function9.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)
    assert 42 == function9.tupled((42, 42, 42, 42, 42, 42, 42, 42, 42))


def test_function10():
    from category.function import Function, Function10

    lambda10 = lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10: 42
    function10 = Function10[int, int, int, int, int, int, int, int, int, int, int](
        lambda10
    )
    assert isinstance(function10, Function)
    assert 42 == function10(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
    )
    assert 42 == function10.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
    )
    assert 42 == function10.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)
    assert 42 == function10.tupled((42, 42, 42, 42, 42, 42, 42, 42, 42, 42))


def test_function11():
    from category.function import Function, Function11

    lambda11 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11: 42
    )
    function11 = Function11[int, int, int, int, int, int, int, int, int, int, int, int](
        lambda11
    )
    assert isinstance(function11, Function)
    assert 42 == function11(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
    )
    assert 42 == function11.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
    )
    assert 42 == function11.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)
    assert 42 == function11.tupled((42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42))


def test_function12():
    from category.function import Function, Function12

    lambda12 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12: 42
    )
    function12 = Function12[
        int, int, int, int, int, int, int, int, int, int, int, int, int
    ](lambda12)
    assert isinstance(function12, Function)
    assert 42 == function12(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
    )
    assert 42 == function12.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
    )
    assert 42 == function12.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)
    assert 42 == function12.tupled((42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42))


def test_function13():
    from category.function import Function, Function13

    lambda13 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13: 42
    )
    function13 = Function13[
        int, int, int, int, int, int, int, int, int, int, int, int, int, int
    ](lambda13)
    assert isinstance(function13, Function)
    assert 42 == function13(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
    )
    assert 42 == function13.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
    )
    assert 42 == function13.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)
    assert 42 == function13.tupled((42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42))


def test_function14():
    from category.function import Function, Function14

    lambda14 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14: 42
    )
    function14 = Function14[
        int, int, int, int, int, int, int, int, int, int, int, int, int, int, int
    ](lambda14)
    assert isinstance(function14, Function)
    assert 42 == function14(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
    )
    assert 42 == function14.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
    )
    assert 42 == function14.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(
        42
    )
    assert 42 == function14.tupled(
        (42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42)
    )


def test_function15():
    from category.function import Function, Function15

    lambda15 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15: 42
    )
    function15 = Function15[
        int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int
    ](lambda15)
    assert isinstance(function15, Function)
    assert 42 == function15(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
    )
    assert 42 == function15.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
    )
    assert 42 == function15.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(
        42
    )(42)
    assert 42 == function15.tupled(
        (42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42)
    )


def test_function16():
    from category.function import Function, Function16

    lambda16 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16: 42
    )
    function16 = Function16[
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
    ](lambda16)
    assert isinstance(function16, Function)
    assert 42 == function16(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
    )
    assert 42 == function16.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
    )
    assert 42 == function16.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(
        42
    )(42)(42)
    assert 42 == function16.tupled(
        (42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42)
    )


def test_function17():
    from category.function import Function, Function17

    lambda17 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17: 42
    )
    function17 = Function17[
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
    ](lambda17)
    assert isinstance(function17, Function)
    assert 42 == function17(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
    )
    assert 42 == function17.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
    )
    assert 42 == function17.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(
        42
    )(42)(42)(42)
    assert 42 == function17.tupled(
        (42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42)
    )


def test_function18():
    from category.function import Function, Function18

    lambda18 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18: 42
    )
    function18 = Function18[
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
    ](lambda18)
    assert isinstance(function18, Function)
    assert 42 == function18(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
        arg18=42,
    )
    assert 42 == function18.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
        arg18=42,
    )
    assert 42 == function18.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(
        42
    )(42)(42)(42)(42)
    assert 42 == function18.tupled(
        (42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42)
    )


def test_function19():
    from category.function import Function, Function19

    lambda19 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19: 42
    )
    function19 = Function19[
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
    ](lambda19)
    assert isinstance(function19, Function)
    assert 42 == function19(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
        arg18=42,
        arg19=42,
    )
    assert 42 == function19.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
        arg18=42,
        arg19=42,
    )
    assert 42 == function19.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(
        42
    )(42)(42)(42)(42)(42)
    assert 42 == function19.tupled(
        (42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42)
    )


def test_function20():
    from category.function import Function, Function20

    lambda20 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19, arg20: 42
    )
    function20 = Function20[
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
    ](lambda20)
    assert isinstance(function20, Function)
    assert 42 == function20(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
        arg18=42,
        arg19=42,
        arg20=42,
    )
    assert 42 == function20.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
        arg18=42,
        arg19=42,
        arg20=42,
    )
    assert 42 == function20.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(
        42
    )(42)(42)(42)(42)(42)(42)
    assert 42 == function20.tupled(
        (42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42)
    )


def test_function21():
    from category.function import Function, Function21

    lambda21 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19, arg20, arg21: 42
    )
    function21 = Function21[
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
    ](lambda21)
    assert isinstance(function21, Function)
    assert 42 == function21(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
        arg18=42,
        arg19=42,
        arg20=42,
        arg21=42,
    )
    assert 42 == function21.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
        arg18=42,
        arg19=42,
        arg20=42,
        arg21=42,
    )
    assert 42 == function21.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(
        42
    )(42)(42)(42)(42)(42)(42)(42)
    assert 42 == function21.tupled(
        (
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
        )
    )


def test_function22():
    from category.function import Function, Function22

    lambda22 = (
        lambda arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16, arg17, arg18, arg19, arg20, arg21, arg22: 42
    )
    function22 = Function22[
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
    ](lambda22)
    assert isinstance(function22, Function)
    assert 42 == function22(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
        arg18=42,
        arg19=42,
        arg20=42,
        arg21=42,
        arg22=42,
    )
    assert 42 == function22.apply(
        arg1=42,
        arg2=42,
        arg3=42,
        arg4=42,
        arg5=42,
        arg6=42,
        arg7=42,
        arg8=42,
        arg9=42,
        arg10=42,
        arg11=42,
        arg12=42,
        arg13=42,
        arg14=42,
        arg15=42,
        arg16=42,
        arg17=42,
        arg18=42,
        arg19=42,
        arg20=42,
        arg21=42,
        arg22=42,
    )
    assert 42 == function22.curried(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(42)(
        42
    )(42)(42)(42)(42)(42)(42)(42)(42)
    assert 42 == function22.tupled(
        (
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
            42,
        )
    )
