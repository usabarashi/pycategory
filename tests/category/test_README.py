from __future__ import annotations


def test_curry():
    from category import curry

    @curry
    def function(arg1: int, /, arg2: int, arg3: int = 3, *, arg4: int = 4) -> int:
        return arg1 + arg2 + arg3 + arg4

    function2 = function  # (int) -> ((int) -> int)
    function1 = function2(1)  # (int) -> int
    result = function1(2)  # int


def test_pipeline():
    from category import Pipeline, curry

    def squared(value: int) -> int:
        return value**2

    assert 42**2**2 == ~(Pipeline(42) >> squared >> squared)

    @Pipeline
    @curry
    def cubed(arg1: int, arg2: int, arg3: int) -> int:
        return arg1 * arg2 * arg3

    assert 42**3 == ~(cubed << 42 << 42 << 42)


def test_either():
    from category import EitherDo, Frame, Left, Monad, Right

    class Error(Frame):
        ...

    @Monad.do
    def context(value: int) -> EitherDo[Error, int]:
        one = yield from Left[Error, int](Error(unmask=("value",)))
        two = 2
        three = yield from Right[Error, int](3)
        return one + two + three

    match context(42).pattern:
        case Left(value):
            print(f"Left case {value}")
        case Right(value):
            print(f"Right case {value}")


def test_option():
    from category import VOID, Monad, OptionDo, Some, Void

    @Monad.do
    def context() -> OptionDo[int]:
        one = yield from VOID
        two = 2
        three = yield from Some[int](3)
        return one + two + three

    match context().pattern:
        case Void():
            print("Void case")
        case Some(value):
            print(f"Some case {value}")


def test_try():
    from category import Failure, Monad, Success, Try, TryDo

    @Try.hold(unmask=("value",))
    def hold_context(value: int, /) -> int:
        if not value:
            raise ValueError("error")
        return value

    @Monad.do
    def context() -> TryDo[int]:
        one = yield from hold_context(0)
        two = 2
        three = yield from Success[int](3)
        return one + two + three

    match context().pattern:
        case Failure() as failure:
            print(f"Failure case {failure.exception}")
        case Success(value):
            print(f"Success case {value}")


def toplevel_process_function(value: int) -> int:
    if not value:
        raise ValueError("error")
    return value


def test_future():
    from category import (
        ExecutionContext,
        Failure,
        Future,
        FutureDo,
        Monad,
        ProcessPoolExecutionContext,
        Success,
        ThreadPoolExecutionContext,
        explicit,
    )

    pe = ProcessPoolExecutionContext(max_workers=5)
    te = ThreadPoolExecutionContext(max_workers=5)

    @Future.hold_explicit
    def thread_function(value: int) -> int:
        if not value:
            raise ValueError("error")
        return value

    @explicit[ExecutionContext].hold
    @Monad.do
    def context() -> FutureDo[int]:
        one = yield from Future.hold_explicit(toplevel_process_function)(0)(pe)
        two = 2
        three = yield from thread_function(3)(te)
        return one + two + three

    match context()(te).pattern:
        case Failure() as failure:
            print(f"Failure case {failure.exception}")
        case Success(value):
            print(f"Success case {value}")


if __name__ == "__main__":
    test_either()
    test_option()
    test_try()
    test_future()
