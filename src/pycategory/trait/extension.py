"""Extension"""

from typing import Callable


class Extension:
    def chain[A, B](self: A, func: Callable[[A], B], /) -> B:
        return func(self)
