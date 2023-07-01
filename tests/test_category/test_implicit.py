def test_implicit_parameter():
    from category import implicit

    assert None is implicit.parameter(bool)

    class ExistImplicit:
        ...

    implicit_ = ExistImplicit()

    def exist():
        assert implicit_ == implicit.parameter(ExistImplicit)

    exist()

    class NotExistImplicit:
        ...

    def not_exist():
        assert None is implicit.parameter(NotExistImplicit)

    not_exist()


def test_optional_arguments_implicit_parameter():
    from category import implicit

    class ExistImplicit:
        ...

    implicit_ = ExistImplicit()

    def exist(optional_param: implicit.Implicit[ExistImplicit] = None):
        assert implicit_ == implicit.find_parameter(
            implicit_parameter=optional_param, target=ExistImplicit
        )

    exist(implicit_)

    class NotExistImplicit:
        ...

    def not_exist(optional_param: implicit.Implicit[NotExistImplicit] = None):
        assert None is implicit.find_parameter(
            implicit_parameter=optional_param, target=NotExistImplicit
        )

    not_exist()


def test_explicit_hold():
    from category import implicit

    class ExistImplicit:
        ...

    @implicit.explicit_hold(bool)
    def exit():
        assert ExistImplicit is type(implicit.parameter(ExistImplicit))

    implicit_ = ExistImplicit
    exit()

    class NotExistImplicit:
        ...

    @implicit.explicit_hold(bool)
    def not_exit():
        assert None is implicit.parameter(NotExistImplicit)

    not_exit()
