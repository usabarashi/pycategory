def test___init__():
    from pycategory import Pipeline

    assert Pipeline is type(Pipeline(42))
    assert 42 == Pipeline(42).value

    def function(value: int) -> int:
        return value

    assert Pipeline is type(Pipeline(function))
    assert callable(Pipeline(function).value)


def test____call__():
    from pycategory import Pipeline

    def function(value: int) -> int:
        return value

    assert Pipeline is type(Pipeline(function)(42))
    assert 42 == Pipeline(function)(42).value


def test___lshift__():
    from pycategory import Pipeline, curry

    @curry
    def function(arg1: int, arg2: int) -> int:
        return arg1 + arg2

    assert 3 == (Pipeline(function) << 1 << 2).value


def test___rshift__():
    from pycategory import Pipeline

    def function(value: int) -> int:
        return value

    assert Pipeline is type(Pipeline(42) >> function >> function)
    assert 42 == (Pipeline(42) >> function >> function).value


def test___invert__():
    from pycategory import Pipeline

    def function(value: int) -> int:
        return value

    assert 42 == ~(Pipeline(42) >> function >> function)


def test_get__():
    from pycategory import Pipeline

    assert 42 == Pipeline(42).get()
