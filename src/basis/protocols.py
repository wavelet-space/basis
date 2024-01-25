"""
Modul obsahuje protokoly, rozhraní pomocné funkce používané napříč knihovnou.
"""

from typing import Protocol, TypeVar, Generic


def is_singleton(this: object) -> bool:
    return isinstance(this, type(Singleton))


class Singleton:
    """
    Marker interface to subclass.
    """


class Versionable(Protocol):
    @property
    def version(self):  # -> ?
        ...


class Configurable(Protocol):
    @property
    def configuration(self):  # -> ?
        ...


Identifier = TypeVar("Identifier")
"""The identifier that is unique per aggregates."""


class Identifiable(Protocol, Generic[Identifier]):
    @property
    def identifier(self) -> Identifier:
        """The entitiy unique identifier."""
