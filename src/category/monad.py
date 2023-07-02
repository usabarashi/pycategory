"""Monad"""
from __future__ import annotations

from functools import wraps
from typing import (
    Any,
    Callable,
    Generator,
    Optional,
    ParamSpec,
    Type,
    TypeVar,
    cast,
)

from . import applicative

Tp = TypeVar("Tp", covariant=True)
TTp = TypeVar("TTp", covariant=True)
P = ParamSpec("P")

FixedMonad = 0


class Monad(applicative.Applicative[Tp]):
    """Monad

    class Monad m where
        return :: a -> m a
        (>>=) :: m a -> (a -> m b) -> m b
        (>>) :: m a -> m b -> m b
        x >> y = x >>= _ -> y
        fail :: String -> m a
        fail msg = error msg
    """

    def __iter__(self) -> Generator[Monad[Tp], None, Tp]:
        raise NotImplementedError()

    def flat_map(self, func: Callable[[Tp], Monad[TTp]], /) -> Monad[TTp]:
        raise NotImplementedError()

    @staticmethod
    def do(context: Callable[P, Generator[Monad[Any], None, Tp]], /) -> Callable[P, Monad[Tp]]:
        """map, flat_map combination syntax sugar."""

        @wraps(context)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Monad[Tp]:
            context_ = context(*args, **kwargs)
            yield_state: Optional[Monad[Any]] = None
            context_type: Optional[Type[Monad[Tp]]] = None
            try:
                while yield_state := next(context_):
                    if not isinstance(yield_state, Monad):  # type: ignore # Runtime type check
                        raise TypeError(yield_state)
                    match context_type:
                        case None:
                            context_type = type(yield_state)
                        case _ if type(yield_state) is not context_type:
                            raise TypeError(
                                yield_state,
                                f"""
                                A different type ${type(yield_state)} \
                                from the context ${context_} is specified.
                                """,
                            )
                        case _ if type(yield_state) is context_type:
                            # Priority is given to the value of the subgenerator's return monad.
                            pass
                        case _:
                            raise ValueError(context)

            except GeneratorExit as exit:
                return cast(Monad[Tp], exit.args[FixedMonad])

            except StopIteration as return_:
                if yield_state is None:
                    raise TypeError(context, "No context type specification")
                if context_type is None:
                    raise TypeError(context, "No context type specification")
                result: Tp = return_.value
                return cast(Monad[Tp], yield_state.map(lambda _: result))

            raise TypeError(context, "No context type specification")

        return wrapper
