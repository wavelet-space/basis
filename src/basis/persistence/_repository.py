"""
Modul obsahuje třídy abstrahující ukládání a načítání entit do/z úložiště (návrhový vzor repository).
"""
import os
from abc import abstractmethod
from typing import Protocol, Self, Callable, Iterable

# from ..aggregate import Entity
from ._connection import Connection
import requests


# https://stackoverflow.com/questions/54118095/


class PersistenceError(Exception):
    def __init__(self, message, *errors):
        super().__init__(self, message)
        self.errors = errors


class ConflictError(PersistenceError):
    """
    Raised when entity can't be stored due some conflicts.
    """


# class AbstractReadableRepository: ...
# class AbstractWrietableRepository: ...


class RepositoryProtocol[Entity, Identifier](Protocol):
    # def next_id() -> Id: ...
    # def save_all(self, entities) -> None: ...
    # def find_all(self, predicate) -> Iterable[T]: ...
    _identity_function: Callable = None

    def _get_identifier(self, entity: Entity) -> Identifier:
        if self._identity_function is None:
            identifier = entity.identifier
        else:
            identifier = self._identity_function(entity)
        return identifier

    def save(self, entity: Entity) -> Identifier:
        """
        Save the entity to the storage.

        :param entity: Entity to save.
        :raises: ConflictError
        """

    def find(self, entity_id: Identifier) -> Entity:  # Entity[Identifier]
        """
        Find the entity in the storage.
        """

    def count(self) -> int:
        """
        Count the persisted entities.
        """

    def exists(self, entity: Entity) -> bool:
        """
        Check if the entity is alrady persisted.

        :param: ...
        """

    def commit(self) -> None:
        """
        Commit changes.

        :raises: ...
        """

    def revert(self) -> None:
        """
        Revert (abort) changes.

        :raises: ...
        """
        # revert/rollback

    def __enter__(self) -> Self:
        return self

    def __exit__(self, error_type, error_value, traceback) -> None:
        if error_type:
            self.revert()
        else:
            self.commit()


class AbstractSQLRepository[Entity, Identifier](RepositoryProtocol):
    _context: Connection

    def __init__(self, context: Connection, identity_function: Callable = None) -> None:
        self._identity_function = identity_function
        self._context = context

    @abstractmethod
    def save(self, entity: Entity) -> Identifier:
        """
        Save the entity to the storage.
        """

    @abstractmethod
    def find(self, entity_id: Identifier) -> Entity | None:  # Entity[Identifier]
        """
        Find the entity in the storage.
        """

    @abstractmethod
    def count(self) -> int:
        """
        Count the persisted entities.
        """

    @abstractmethod
    def exists(self, entity: Entity) -> bool:
        """
        Check if the entity is alrady persisted.

        :param: ...
        """

    def commit(self) -> None:
        """
        Commit changes.

        :raises: ...
        """
        self._context.commit()

    def revert(self) -> None:
        """
        Revert (abort) changes.

        :raises: ...
        """
        # revert/rollback
        self._context.rollback()


# The conrete implementations of repositories.


class MemoryRepository[Entity, Identifier](RepositoryProtocol):
    """
    The repository storing entities in the computer's memory.

    Examples:

        ...
    """

    _storage: dict[Identifier, Entity]
    _current: list[Entity]

    def __init__(self, entities: Iterable[Entity] = None, identity_function: Callable = None) -> None:
        if entities is None:
            entities = []

        self._identity_function = identity_function
        self._storage = {}  # Should be class variable?
        self._storage |= {self._get_identifier(e): e for e in entities}
        self._current = []

    def save(self, entity: Entity) -> Identifier:
        if self.exists(entity):
            raise ConflictError("Conflict {entity}")
        self._current.append(entity)
        return self._get_identifier(entity)

    def find(
            self, entity_id: Identifier
    ) -> Entity | None:  # Entity[Identifier] can!t be used?
        return self._storage.get(entity_id, None)

    def count(self) -> int:
        # NOTE: no update, so it can just sum commited and uncommited
        return len(self._storage.keys()) + len(self._current)

    def exists(self, entity: Entity) -> bool:
        return self._get_identifier(entity) in self._storage

    def commit(self) -> None:
        self._storage |= {self._get_identifier(e): e for e in self._current}
        self._current = []

    def revert(self) -> None:
        self._current = []


class Requester:

    def __init__(self, **request_args: dict):
        self.request_args = request_args

    def get(self, url):
        return requests.get(url, **self.request_args)

    def put(self, url, data):
        return requests.put(url, data, **self.request_args)

    def post(self, url, data):

        return requests.post(url, data, **self.request_args)

    def delete(self, url):
        return requests.delete(url, **self.request_args)


class RestRepository[Entity, Identifier, DataSend](RepositoryProtocol[Entity, Identifier]):
    def __init__(self, base_url: str, entity_uri: str, **request_args):
        self._requester = Requester(**request_args)
        self._base_url = base_url
        self._entity_uri = entity_uri

    @abstractmethod
    def _to_data(self, entity: Entity) -> DataSend:
        ...

    @abstractmethod
    def _to_entity(self, data: DataSend) -> Entity:
        ...

    def save(self, entity: Entity) -> Identifier:
        """
        Save the entity to the storage.

        :param entity: Entity to save.
        :raises: ConflictError
        """
        if self.exists(entity):
            raise ConflictError(f"Conflict {entity}")
        data = self._to_data(entity)
        returned_data = self._requester.post(os.path.join(self._base_url, self._entity_uri), data)
        entity = self._to_entity(returned_data)
        identifier = self._get_identifier(entity)
        return identifier

    def find(self, entity_id: Identifier) -> Entity:  # Entity[Identifier]
        """
        Find the entity in the storage.
        """
        if entity_id is None:
            return None
        data = self._requester.get(os.path.join(self._base_url, self._entity_uri, str(entity_id)))
        if data:
            return self._to_entity(data)
        return None

    @abstractmethod
    def count(self) -> int:
        """
        Count the persisted entities.
        """
        ...

    def exists(self, entity: Entity) -> bool:
        """
        Check if the entity is alrady persisted.

        :param: ...
        """
        return self.find(self._get_identifier(entity)) is not None

    def commit(self) -> None:
        """
        Commit changes.

        :raises: ...
        """
        pass

    def revert(self) -> None:
        """
        Revert (abort) changes.

        :raises: ...
        """
        raise NotImplementedError("Rest api cannot roll back.")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
