"""Monad"""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Generator, Optional, cast

from pycategory.trait import applicative


class ShortCircuit(GeneratorExit):
    args: tuple[Monad[Any], ...]

    @property
    def state(self) -> Monad[Any]:
        return self.args[0]


class Monad[A](applicative.Applicative[A]):
    """Monad

    class Monad m where
        return :: a -> m a
        (>>=) :: m a -> (a -> m b) -> m b
        (>>) :: m a -> m b -> m b
        x >> y = x >>= _ -> y
        fail :: String -> m a
        fail msg = error msg
    """

    def __iter__(self) -> Generator[Monad[A], None, A]:
        """

        :raises ShortCircuit: In case of short-circuit evaluation of flat_map.
        """
        raise NotImplementedError()

    def flat_map[B](self, func: Callable[[A], Monad[B]], /) -> Monad[B]:
        raise NotImplementedError()

    @staticmethod
    def do[**P](context: Callable[P, Generator[Monad[Any], None, A]], /) -> Callable[P, Monad[A]]:
        """Syntax Sugar for Monadic Compositions."""

        @wraps(context)
        def trampoline(*args: P.args, **kwargs: P.kwargs) -> Monad[A]:
            context_ = context(*args, **kwargs)
            yield_: Optional[Monad[Any]] = None
            composite: Optional[Monad[A]] = None
            try:
                while yield_ := next(context_):
                    # Runtime type check
                    if not isinstance(yield_, Monad):  # type: ignore
                        raise TypeError(
                            yield_, f"""${type(yield_)} cannot be monadic composition."""
                        )
                    match composite:
                        case None:
                            composite = yield_
                        case _ if type(yield_) is not type(composite):
                            raise TypeError(
                                yield_,
                                f"""
                                ${type(yield_)} cannot be \
                                monadic composition \
                                with ${type(composite)}.
                                """,
                            )
                        case _ if type(yield_) is type(composite):
                            composite = composite.flat_map(lambda _: cast(Monad[Any], yield_))
                        case _:
                            raise ValueError(context)

            except ShortCircuit as short_circuit:
                return cast(Monad[A], short_circuit.state)

            except StopIteration as return_:
                if composite is None:
                    raise TypeError(context, "Not a monadic composition.")
                result: A = return_.value
                return cast(Monad[A], composite.map(lambda _: result))

            raise ValueError(context)

        return trampoline
