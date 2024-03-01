"""
Modul obsahuje třídy abstrahující ukládání a načítání entit do/z úložiště (návrhový vzor repository).
"""

from abc import abstractmethod, abstractclassmethod
from typing import Generic, TypeVar, Any, Self

from basis.persistence.interface import Connection


Entity = TypeVar("Entity", bound=Any)
"""A domain entity type."""
Identifier = TypeVar("Identifier", bound=Any)
"""A domain entity identifier type."""

# https://stackoverflow.com/questions/54118095/


class PersistenceError(Exception):
    def __init__(self, message, *errors):
        super().__init__(self, message)
        self.errors = errors


# class AbstractReadableRepository: ...
# class AbstractWrietableRepository: ...


class AbstractRepository(Generic[Entity, Identifier]):
    def __init__(self, context: Connection = None) -> None:
        self.context = context

    @abstractmethod
    def save(self, entity) -> None:
        """
        Save the entity to the storage.
        """

    # def save_all(self, entities) -> None: ...

    @abstractmethod
    def find(self, entity_id: Identifier) -> Entity:  # Entity[Identifier]
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


class MemoryRepository(AbstractRepository[Entity, Identifier]):
    storage = {}

    def __init__(self, *entities) -> None:
        MemoryRepository.storage |= {e.identifier: e for e in entities}
        self._current = []

    def save(self, entity) -> None:
        if self.exists(entity.identifier):
            raise ValueError("Conflict {entity}")
        self._current.append(entity)

    def find(self, entity_id: Identifier) -> Entity | None:  # Entity[Identifier]
        return self._storage.get(entity_id, None)

    def count(self) -> int:
        return len(self._storage.keys())

    def exists(self, entity_id) -> bool:
        return entity_id in self._storage

    def _commit(self) -> None:
        self._storage |= {e.identifier: e for e in self._current}
        self._current = []

    def _revert(self) -> None:
        self._current = []


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    repo = AbstractRepository()
