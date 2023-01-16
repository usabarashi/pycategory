def test_implicit_parameter():
    from category import implicit_

    assert None is implicit_.parameter(bool)

    class ExistImplicit:
        ...

    _implicit_parameter = ExistImplicit()

    def exist():
        assert _implicit_parameter == implicit_.parameter(ExistImplicit)

    exist()

    class NotExistImplicit:
        ...

    def not_exist():
        assert None is implicit_.parameter(NotExistImplicit)

    not_exist()


def test_optional_arguments_implicit_parameter():
    from category import implicit_

    class ExistImplicit:
        ...

    _implicit_parameter = ExistImplicit()

    def exist(optional_param: implicit_.Implicit[ExistImplicit] = None):
        assert _implicit_parameter == implicit_.find_parameter(
            param=optional_param, target=ExistImplicit
        )

    exist(_implicit_parameter)

    class NotExistImplicit:
        ...

    def not_exist(optional_param: implicit_.Implicit[NotExistImplicit] = None):
        assert None is implicit_.find_parameter(
            param=optional_param, target=NotExistImplicit
        )

    not_exist()


def test_implicit():
    from category import implicit, implicit_

    @implicit[int, bool].hold
    def implicit_func(boolean: bool) -> int:
        if (implicit_int := implicit_.parameter(int)) is None:
            raise implicit_.CannotFindImplicitParameter(int)
        if (implicit_bool := implicit_.parameter(bool)) is None:
            raise implicit_.CannotFindImplicitParameter(bool)
        return implicit_int * implicit_bool

    try:
        implicit_func(False)
    except implicit_.CannotFindImplicitParameter:
        assert True
    except Exception:
        assert False

    _implicit_int = 42
    _implicit_bool = True
    _ = implicit_func
    assert implicit_.Implicit is type(implicit_func)
    assert callable(implicit_func)
    _ = implicit_func(False)
    assert int is type(implicit_func(False))
    assert 42 == implicit_func(False)


def test_explicit():
    from category import explicit, implicit_

    @explicit[int, bool].hold
    def explicit_func(boolean: bool) -> int:
        if (implicit_int := implicit_.parameter(int)) is None:
            raise implicit_.CannotFindImplicitParameter(int)
        if (implicit_bool := implicit_.parameter(bool)) is None:
            raise implicit_.CannotFindImplicitParameter(bool)
        return implicit_int * implicit_bool

    try:
        assert int is type(explicit_func(False)("42", lambda a: a))
    except implicit_.CannotFindImplicitParameter:
        assert True
    except Exception:
        assert False

    _ = explicit_func
    assert callable(explicit_func)
    _ = explicit_func(False)
    assert callable(explicit_func(False))
    assert int is type(explicit_func(False)(42, True))
    assert 42 == explicit_func(False)(42, True)
