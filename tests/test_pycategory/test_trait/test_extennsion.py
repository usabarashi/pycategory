def test_method():
    from pycategory import Extension

    class Plain(Extension):
        def __init__(self, value: int):
            self.value = value

    assert 0 == Plain(42).chain(lambda plain: plain.value * 0)
