"""
Modul obsahuje protokoly, rozhraní pomocné funkce používané napříč knihovnou.
"""

from typing import Protocol


def is_singleton(this: object) -> bool:
    return isinstance(this, type(Singleton))


class Singleton:
    """Marker interface to subclass."""


class Versionable[Version](Protocol):
    """
    Represents an object with defined version. 
    
    Version e.g. ``str``, ``int``, or ``tuple[int, int, int]``.
    """
    
    @property
    def version(self) -> Version:
        ...


class Configurable(Protocol):
    @property
    def configuration(self):  # -> ?
        ...
