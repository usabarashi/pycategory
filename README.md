# python-category

![license](https://img.shields.io/badge/license-MIT-green)
![license](https://img.shields.io/badge/python-3.10-blue)

## Examples

### Either

```python
from category import Either, EitherDo, Left, Right

@Either.do
def context() -> EitherDo[str, int]:
    one = yield from Left[str, int]("one")
    two = 2
    three = yield from Right[str, int](3)
    return one + two + three

match context().pattern:
    case Left(value):
        print(f"Left case {value}")
    case Right(value):
        print(f"Right case {value}")
```

### Option

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

### Try

```python
from category import Failure, Success, Try, TryDo

@Try.hold
def hold_context(value: int, /) -> int:
    if not value:
        raise Exception(value)
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
