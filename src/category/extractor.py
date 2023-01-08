from typing import Any


class Extractor:

    __match_args__: tuple[()] | tuple[str, ...] = ()

    @classmethod
    def apply(cls, *args: ..., **kwargs: ...):
        instance = cls.__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance

    def unapply(self) -> tuple[()] | tuple[Any, ...]:
        """Return match attributes as tuples."""
        if len(self.__match_args__) <= 0:
            return ()
        else:
            return tuple(
                value for key, value in vars(self).items() if key in self.__match_args__
            )
