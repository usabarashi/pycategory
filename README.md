# category

# Installation

pip install works for this library.

```console
pip install pycategory
```

# Usage

Here is an example of how to use the `category` package:

## curry

```python
from category import curry

@curry
def function(arg1: int, /, arg2: int, arg3: int = 3, *, arg4: int = 4) -> int:
    return arg1 + arg2 + arg3 + arg4

function2 = function        # (int) -> ((int) -> int)
function1 = function2(1)    # (int) -> int
result = function1(2)       # int
```

## Pipeline

```python
from category import Pipeline, curry

def squared(value: int) -> int:
    return value**2

assert 42**2**2 == ~(Pipeline(42) >> squared >> squared)

@Pipeline
@curry
def cubed(arg1: int, arg2: int, arg3: int) -> int:
    return arg1 * arg2 * arg3

assert 42**3 == ~(cubed << 42 << 42 << 42)
```

## Either

```python
from category import Either, EitherDo, Frame, Left, Right

class Error(Frame):
    ...

@Either.do
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
```

## Option

```python
from category import VOID, Option, OptionDo, Some, Void

@Option.do
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
```

## Try

```python
from category import Failure, Success, Try, TryDo

@Try.hold(unmask=("value",))
def hold_context(value: int, /) -> int:
    if not value:
        raise Exception("error")
    return value

@Try.do
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

```
