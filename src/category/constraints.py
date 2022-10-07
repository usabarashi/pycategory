"""Constraints"""
from typing import Generic, Type, TypeVar

From = TypeVar("From", covariant=False)
To = TypeVar("To", covariant=True)


class SubtypeConstraints(Generic[From, To]):
    """Subtyping constraints"""

    def __init__(self, from_: Type[From], to_: Type[To]):
        if not issubclass(from_, to_):
            raise TypeError(from_, to_)
