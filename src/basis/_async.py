from typing import ParamSpec, TypeVar
from collections.abc import Awaitable, Callable

P = ParamSpec("P")
R = TypeVar("R")


def to_async(func: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    ...
