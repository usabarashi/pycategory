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
