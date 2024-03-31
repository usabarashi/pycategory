"""Constraints"""

from typing import Type


class SubtypeConstraints[F, T]:
    """Subtyping constraints"""

    def __init__(self, from_: Type[F], to_: Type[T]):
        if not issubclass(from_, to_):
            raise TypeError(from_, to_)
