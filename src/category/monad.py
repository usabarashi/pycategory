"""Monad"""
from __future__ import annotations

from functools import wraps
from typing import (
    Any,
    Callable,
    Generator,
    Generic,
    Optional,
    ParamSpec,
    Type,
    TypeVar,
    cast,
)

from . import applicative_functor

M = TypeVar("M", covariant=True)
A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)
P = ParamSpec("P")

FixedMonad = 0


class Monad(Generic[A], applicative_functor.ApplicativeFunctor[A]):
    """Monad

    class Monad m where
        return :: a -> m a
        (>>=) :: m a -> (a -> m b) -> m b
        (>>) :: m a -> m b -> m b
        x >> y = x >>= _ -> y
        fail :: String -> m a
        fail msg = error msg
    """

    __match_args__: tuple[()] | tuple[str] = ()

    def __bool__(self) -> bool:
        raise NotImplementedError

    def __iter__(self) -> Generator[Monad[A], None, A]:
        raise NotImplementedError

    def unapply(self) -> tuple[()] | tuple[Any, ...]:
        """

        Return match attributes as tuples
        """
        if len(self.__match_args__) <= 0:
            return ()
        else:
            return tuple(
                value for key, value in vars(self).items() if key in self.__match_args__
            )

    def flat_map(self: Monad[A], other: Callable[[A], Monad[B]], /) -> Monad[A]:
        raise NotImplementedError

    @staticmethod
    def do(context: Callable[P, Generator[M, None, A]], /) -> Callable[P, M]:
        """map, flat_map combination syntax sugar."""

        @wraps(context)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> M:
            context_ = context(*args, **kwargs)
            context_type: Optional[Type[Monad[A]]] = None
            try:
                while True:
                    yield_state = next(context_)
                    if not isinstance(yield_state, Monad):
                        raise TypeError(yield_state)
                    match context_type:
                        case None:
                            context_type = type(yield_state)
                        case _ if type(yield_state) is not context_type:
                            raise TypeError(
                                yield_state,
                                f"A different type ${type(yield_state)} from the context ${context_} is specified.",
                            )
                        case _ if type(yield_state) is context_type:
                            # Priority is given to the value of the subgenerator's return monad.
                            ...
                        case _:
                            raise ValueError(context)
            except GeneratorExit as exit:
                return cast(Monad[A], exit.args[FixedMonad])
            except StopIteration as return_:
                if context_type is None:
                    raise TypeError(context, "No context type specification")
                return cast(Monad[A], context_type).pure(return_.value)

        return wrapper
