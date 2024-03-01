# -*- coding: utf-8 -*-


"""
The abstract classes to implements a _Repository pattern_.
"""

import inspect
from typing import TypeVar, Protocol


__all__ = tuple(["Identifier", "Entity"])


"""A domain entity identifier type."""
Identifier = TypeVar("Identifier")
# Hashable + immutable e.g. UUID, int etc.


class Identifiable[Identifier](Protocol):
    @property
    def identifier(self) -> Identifier:
        """The entitiy unique identifier."""


class Entity[Identifier]:
    """
    An entity object in the terms of Doman-driven design.

    :param identifier:
    """

    def __init__(self, identifier: Identifier):
        self._identifier: Identifier = identifier

    @property
    def identifier(self) -> Identifier:
        return self._identifier

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.identifier == other.identifier

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

    # NOTE The transfer layer (data transfer object) related method.
    # Maybe use a standalone :class:`JsonEncoder` in DTO module.
    # def to_json(self): return NotImplemented
