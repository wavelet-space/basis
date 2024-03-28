"""
Modul obsahuje třídy abstrahující ukládání a načítání entit do/z úložiště (návrhový vzor repository).
"""

from abc import abstractmethod
from typing import Self, TypeVar, Protocol

#from ..aggregate import Entity
from ._connection import Connection, SQLConnection
from ._entity import Entity

Entity = TypeVar("Entity", bound=Entity)
"""A domain entity type."""


# https://stackoverflow.com/questions/54118095/


class PersistenceError(Exception):
    def __init__(self, message, *errors):
        super().__init__(self, message)
        self.errors = errors


# class AbstractReadableRepository: ...
# class AbstractWrietableRepository: ...


class AbstractRepository[Entity, Identifier](Protocol):
    def __init__(self, context: Connection = None) -> None:
        self.context = context

    @abstractmethod
    def save(self, entity) -> None:
        """
        Save the entity to the storage.
        """

    # def save_all(self, entities) -> None: ...

    @abstractmethod
    def get(self, entity_id: Identifier) -> Entity:  # Entity[Identifier]
        """
        Find the entity in the storage.
        """

    # def find_all(self, predicate) -> Iterable[T]: ...

    # @abstractclassmethod
    # def next_id() -> Id: ...

    @abstractmethod
    def count(self) -> int:
        """
        Count the persisted entities.
        """

    @abstractmethod
    def exists(self, entity_id) -> bool:
        """
        Check if the entity is alrady persisted.

        :param: ...
        """

    @abstractmethod
    def _commit(self) -> None:
        """
        Commit changes.

        :raises: ...
        """

    @abstractmethod
    def _revert(self) -> None:
        """
        Revert (abort) changes.

        :raises: ...
        """
        # revert/rollback
        ...

    def __enter__(self) -> Self:
        return self

    def __exit__(self, error_type, error_value, traceback) -> None:
        if error_type:
            self._revert()
        else:
            self._commit()


class MemoryRepository[DictEntity, Identifier](AbstractRepository):
    def __init__(self, *entities) -> None:
        self.storage = {}  # Should be class variable?
        self.storage |= {e.identifier: e.data for e in entities}
        self._current = []

    def save(self, entity) -> None:
        if self.exists(entity.identifier):
            raise ValueError("Conflict {entity}")
        self._current.append(entity)

    def get(
        self, entity_id: Identifier
    ) -> Entity | None:  # Entity[Identifier] can!t be used?
        return self.storage.get(entity_id, None)

    def count(self) -> int:
        return len(self.storage.keys())

    def exists(self, entity_id) -> bool:
        return entity_id in self.storage

    def _commit(self) -> None:
        self.storage |= {e.identifier: e for e in self._current}
        self._current = []

    def _revert(self) -> None:
        self._current = []

IDENTITY_NAME = 'id'
TABLE_NAME = 'test'


class SQLRepository[DictEntity, Identifier](AbstractRepository):

    """Interesting problems:
                            * User of repository MUST already know the mapping
    """
    def __init__(self, connection: SQLConnection, mapping=None) -> None:
        """Initialize the SQLRepository class.
            Args:
                connection (SQLConnection): Connection to the database
                mapping (dict): Mapping between keys in used entity and columns in table
        """

        self._connection = connection
        self._cursor = connection.cursor()
        self._from_key_to_column = mapping or {}
        self._from_column_to_key = zip(self._from_key_to_column.values(), self._from_key_to_column.keys())


    def save(self, entity) -> None:
        if self.exists(entity.identifier):
            raise ValueError("Conflict {entity}")

        # this is extremely suspicious part of code
        query = f'INSERT INTO {TABLE_NAME} {tuple(entity.data.keys())} VALUES {tuple(entity.data.values())}'
        self._cursor.execute(query)

    def get(
        self, entity_id: Identifier
    ) -> Entity | None:  # Entity[Identifier] can!t be used?

        query = f'SELECT * FROM {TABLE_NAME} WHERE {IDENTITY_NAME}={entity_id}'
        self._cursor.execute(query)
        result_values = self._cursor.fetchone()
        # could also possible be x.name, but this id not think is specified by PEP
        result_columns = [x[0] for x in self._cursor.description]
        result = {}

        # should be most likely encapsulated
        for column, value in zip(result_columns, result_values):
            key = column
            if column in self._from_column_to_key.keys():
                key = self._from_column_to_key[column]
            result[key] = value

        return self.storage.get(entity_id, None)

    def count(self) -> int:
        return self._cursor.rowcount

    def exists(self, entity_id) -> bool:
        query = f'SELECT {IDENTITY_NAME} FROM {TABLE_NAME} WHERE {IDENTITY_NAME}={entity_id}'
        self._cursor.execute(query)
        return self._cursor.fetchone() is not None

    def _commit(self) -> None:
        self._connection.commit()

    def _revert(self) -> None:
        self._connection.rollback()


if __name__ == "__main__":
    import doctest

    doctest.testmod()

