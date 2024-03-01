"""
Modul obsahuje protokoly, rozhraní pomocné funkce používané napříč knihovnou.
"""

from typing import Protocol


def is_singleton(this: object) -> bool:
    return isinstance(this, type(Singleton))


class Singleton:
    """Marker interface to subclass."""


class Versionable(Protocol):
    @property
    def version(self) -> tuple[int, int, int]:
        ...


class Configurable(Protocol):
    @property
    def configuration(self):  # -> ?
        ...
