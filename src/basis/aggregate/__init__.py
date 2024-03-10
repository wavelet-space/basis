# -*- coding: utf-8 -*-


"""
The abstract classes to implements a _Repository pattern_.
"""

import inspect
from typing import Protocol

__all__ = tuple(["Entity"])


class Identifiable[Identifier](Protocol):
    @property
    def identifier(self) -> Identifier:
        """The unique identifier for a group of objects of the same type."""


# Hashable + immutable e.g. UUID, int etc.


class Entity[Identifier]:
    """
    An entity object in the terms of domain-driven design.

    :tparam: A domain entity identifier type.
    :param identifier: The entity's identifier unique accros aggregate.
    """

    def __init__(self, identifier: Identifier) -> None:
        self._identifier: Identifier = identifier

    @property
    def identifier(self) -> Identifier:
        return self._identifier

    def __eq__(self, that: object) -> bool:
        return isinstance(that, type(self)) and self.identifier == that.identifier

    def __hash__(self) -> int:
        return hash((type(self), self.identifier))

    def __str__(self) -> str:
        fields = inspect.getmembers(type(self), lambda a: not (inspect.isroutine(a)))
        fields_filtered = [
            f"{f[0]}={getattr(self, str(f[0]))}"
            for f in fields
            if (not f[0].startswith("_")) and (not f[0].startswith("__"))
        ]
        return f"{type(self).__name__}({','.join(fields_filtered)})"

    __repr__ = __str__  # Maybe prefer not to override this.


class VersionedEntity[Identifier, Version](Entity[Identifier]):
    def __init__(self, identifier: Identifier, version: Version) -> None:
        super().__init__(identifier=identifier)
        self._version = version

    @property
    def version(self) -> Version:
        return self._version
