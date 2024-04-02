import inspect
import typing
from abc import ABC
from typing import TypeVar, Hashable, Generic, Protocol

Identifier = TypeVar("Identifier", bound=Hashable)
"""The identifier is unique per aggregate. Must be immutable and hashable, e.g., 'int', 'UUID', tuple, etc.
Remember that an identifier should match domain needs; it doesn't have to always be an integer or UUID."""


class Identifiable(Protocol, Generic[Identifier]):  # type: ignore
    """
    Represents an entity with identifier.
    """

    @property
    def identifier(self) -> Identifier:
        """The entitie's unique identifier."""


class Entity(ABC, Generic[Identifier]):
    """
    As generic as possible entity object to be used in repository.

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


EntityType = TypeVar("EntityType", bound=Entity)


class DictEntity(Entity[Identifier]):
    def __init__(self, identifier: Identifier, data: dict):
        super().__init__(identifier)
        self._data = data

    @property
    def data(self) -> typing.Any:
        return self._data
