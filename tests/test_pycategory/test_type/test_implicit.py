import pytest


def test_implicit_given():
    import inspect
    from pycategory.type.implicit import Implicit, _IMPLICIT

    Implicit.given(42)
    Implicit.given("42")

    frame = inspect.currentframe()
    assert frame is not None
    assert bool not in frame.f_locals[_IMPLICIT]
    assert 42 == frame.f_locals[_IMPLICIT].get(int)
    assert "42" == frame.f_locals[_IMPLICIT].get(str)


def test_implicit_use():
    from pycategory.type.implicit import Implicit, ImplicitError

    Implicit.given(42)
    Implicit.given("42")

    with pytest.raises(ImplicitError):
        assert Implicit.use(bool)
    assert 42 == Implicit.use(int)
    assert "42" == Implicit.use(str)


def test_implicit_constructor():
    from pycategory.type.implicit import Implicit

    def no_args() -> int:
        return 42

    implicit_no_args = Implicit(no_args, int, str)

    def has_args(a: int, b: str) -> int:
        return 42

    implicit_has_args = Implicit(has_args, int, str)

    assert isinstance(implicit_no_args, Implicit)
    assert callable(implicit_no_args)
    assert isinstance(implicit_has_args, Implicit)
    assert callable(implicit_has_args)


def test_implicit_usage_decorator():
    from pycategory.type.implicit import Implicit

    @Implicit.usage(int, str)
    def no_args() -> int:
        return Implicit.use(bool)

    @Implicit.usage(int, str)
    def has_args(value: int) -> int:
        return Implicit.use(int)

    assert isinstance(no_args, Implicit)
    assert callable(no_args)
    assert isinstance(has_args, Implicit)
    assert callable(has_args)


def test_implicit_constructor___call__():
    from pycategory.type.implicit import Implicit, ImplicitError

    def no_args() -> int:
        return 42

    implicit_no_args = Implicit(no_args, int, str)

    def has_args(a: int, b: str) -> int:
        return 42

    implicit_has_args = Implicit(has_args, int, str)

    with pytest.raises(ImplicitError):
        implicit_no_args()
    with pytest.raises(ImplicitError):
        implicit_has_args(42, "42")

    Implicit.given(42)
    Implicit.given("42")
    assert 42 == implicit_no_args()
    assert 42 == implicit_has_args(42, "42")


def test_implicit_decorator___call__():
    from pycategory.type.implicit import Implicit, ImplicitError

    @Implicit.usage(int, str)
    def implicit_no_args() -> int:
        return 42

    @Implicit.usage(int, str)
    def implicit_has_args(a: int, b: str) -> int:
        return 42

    with pytest.raises(ImplicitError):
        implicit_no_args()
    with pytest.raises(ImplicitError):
        implicit_has_args(42, "42")

    Implicit.given(42)
    Implicit.given("42")
    assert 42 == implicit_no_args()
    assert 42 == implicit_has_args(42, "42")


def test_implicit_constructor_use():
    from pycategory.type.implicit import Implicit, ImplicitError

    def no_args() -> str:
        return Implicit.use(str)

    implicit_no_args = Implicit(no_args, int, str)

    def has_args(a: int, b: str) -> str:
        return Implicit.use(str)

    implicit_has_args = Implicit(has_args, int, str)

    with pytest.raises(ImplicitError):
        implicit_no_args()
    with pytest.raises(ImplicitError):
        implicit_has_args(42, "42")

    Implicit.given(42)
    Implicit.given("42")
    assert "42" == implicit_no_args()
    assert "42" == implicit_has_args(42, "42")


def test_implicit_decorator_use():
    from pycategory.type.implicit import Implicit, ImplicitError

    @Implicit.usage(int, str)
    def implicit_no_args() -> str:
        return Implicit.use(str)

    @Implicit.usage(int, str)
    def implicit_has_args(a: int, b: str) -> str:
        return Implicit.use(str)

    with pytest.raises(ImplicitError):
        implicit_no_args()
    with pytest.raises(ImplicitError):
        implicit_has_args(42, "42")

    Implicit.given(42)
    Implicit.given("42")
    assert "42" == implicit_no_args()
    assert "42" == implicit_has_args(42, "42")


def test_implicit_constructor_nest():
    from pycategory.type.implicit import Implicit

    def no_args():
        return Implicit.use(str)

    def has_args(a: int, b: str):
        implicit_no_args = Implicit(no_args, int, str)
        return implicit_no_args

    implicit_has_args = Implicit(has_args, int, str)

    Implicit.given(42)
    Implicit.given("42")
    assert "42" == implicit_has_args(42, "42")()


def test_implicit_decorator_nest():
    from pycategory.type.implicit import Implicit

    @Implicit.usage(int, str)
    def implicit_no_args():
        return Implicit.use(str)

    @Implicit.usage(int, str)
    def implicit_has_args(a: int, b: str):
        return implicit_no_args

    Implicit.given(42)
    Implicit.given("42")
    assert "42" == implicit_has_args(42, "42")()
