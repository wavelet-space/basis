"""
Modul obsahuje třídy abstrahující ukládání a načítání entit do/z úložiště (návrhový vzor repository).
"""

from abc import abstractmethod
from typing import TypeVar, Protocol, Generic

# from ..aggregate import Entity
from ._connection import Connection, SQLConnection
from ._entity import Entity, DictEntity, Identifier, EntityType


# https://stackoverflow.com/questions/54118095/


class PersistenceError(Exception):
    def __init__(self, message, *errors):
        super().__init__(self, message)
        self.errors = errors


# class AbstractReadableRepository: ...
# class AbstractWrietableRepository: ...


class RepositoryProtocol[EntityType, Identifier](Protocol):
    @abstractmethod
    def save(self, entity: EntityType) -> None:
        """
        Save the entity to the storage.
        """

    # def save_all(self, entities) -> None: ...

    @abstractmethod
    def get(self, entity_id: Identifier) -> EntityType:  # Entity[Identifier]
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
    def exists(self, entity_id: Identifier) -> bool:
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

    def __enter__(self):  # -> Self supported only from 3.10
        return self

    def __exit__(self, error_type, error_value, traceback) -> None:
        if error_type:
            self._revert()
        else:
            self._commit()


class AbstractRepository[EntityType, Identifier](RepositoryProtocol):
    def __init__(self, context: Connection = None) -> None:
        self.context = context

    @abstractmethod
    def save(self, entity: EntityType) -> None:
        """
        Save the entity to the storage.
        """

    # def save_all(self, entities) -> None: ...

    @abstractmethod
    def get(self, entity_id: Identifier) -> EntityType:  # Entity[Identifier]
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
    def exists(self, entity_id: Identifier) -> bool:
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
        self.context.commit()

    @abstractmethod
    def _revert(self) -> None:
        """
        Revert (abort) changes.

        :raises: ...
        """
        # revert/rollback
        self.context.rollback()

    def __enter__(self):  # -> Self supported only from 3.10
        return self

    def __exit__(self, error_type, error_value, traceback) -> None:
        if error_type:
            self._revert()
        else:
            self._commit()


class MemoryRepository[EntityType, Identifier](RepositoryProtocol):
    def __init__(self, *entities) -> None:
        self.storage = {}  # Should be class variable?
        self.storage |= {e.identifier: e.data for e in entities}
        self._current = []

    def save(self, entity: DictEntity) -> None:
        if self.exists(entity.identifier):
            raise ValueError("Conflict {entity}")
        self._current.append(entity)

    def get(
            self, entity_id: Identifier
    ) -> DictEntity | None:  # Entity[Identifier] can!t be used?
        return self.storage.get(entity_id, None)

    def count(self) -> int:
        return len(self.storage.keys())

    def exists(self, entity_id: Identifier) -> bool:
        return entity_id in self.storage

    def _commit(self) -> None:
        self.storage |= {e.identifier: e for e in self._current}
        self._current = []

    def _revert(self) -> None:
        self._current = []


IDENTITY_NAME = 'id'
TABLE_NAME = 'test'


class SQLRepository[Identifier](RepositoryProtocol[DictEntity, Identifier]):
    """Interesting problems:
                            * User of repository MUST already know the mapping
                            * id column name MUST also be known ahead of the time
                            * does it make even sense to have generic identifier, when ids are numbers?
                            * but they don't have to be number, or a single column, even though it is a liiiitle bit idiotic
    """
    context: SQLConnection

    def __init__(self, context: SQLConnection, mapping=None) -> None:
        """Initialize the SQLRepository class.
            Args:
                context (SQLConnection): Connection to the database
                mapping (dict): Mapping between keys in used entity and columns in table
        """
        # does not actually initialize context for some reason, probably badly set up Inheritance
        self.context = context
        self._cursor = self.context.cursor()
        self._from_key_to_column = mapping or dict()
        print(self._from_key_to_column)
        self._from_column_to_key = {key: value for key, value in
                                    zip(self._from_key_to_column.values(), self._from_key_to_column.keys())}

    def save(self, entity: DictEntity) -> None:
        if self.exists(entity.identifier):
            raise ValueError(f"Conflict {entity}")

        # this is extremely suspicious part of code
        # this does not unsuprisingly work, he types are not converted well this way into sql instruction value
        value_names = ', '.join([str(x) for x in entity.data.keys()])
        values = ', '.join([str(x) for x in entity.data.values()])
        # TODO: USE MORE UNIVERSAL WAY TO SEND VALUE DATA
        query = f'INSERT INTO {TABLE_NAME} ({value_names}) VALUES ({values})'
        self._cursor.execute(query)

    def get(
            self, entity_id: Identifier
    ) -> DictEntity | None:  # Entity[Identifier] can!t be used? maybe can?

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

        entity = DictEntity[Identifier](entity_id, result)
        return entity

    def count(self) -> int:
        return self._cursor.rowcount

    def exists(self, entity_id: Identifier) -> bool:
        query = f'SELECT {IDENTITY_NAME} FROM {TABLE_NAME} WHERE {IDENTITY_NAME}={entity_id}'
        self._cursor.execute(query)
        return self._cursor.fetchone() is not None

    def _commit(self) -> None:
        return super()._commit()

    def _revert(self) -> None:
        return super()._revert()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
