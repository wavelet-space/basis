"""
Modul obsahuje třídy abstrahující ukládání a načítání entit do/z úložiště (návrhový vzor repository).
"""

from abc import abstractmethod
from typing import Generic ,TypeVar, Any, Self


Entity = TypeVar("Entity", bound=Any)


class AbstractRepository(Generic[Entity]):
    def __init__(self, context) -> None:
        self.context = context

    @abstractmethod
    def save(self, entity) -> None:
        """
        Save the entity to the storage.
        """

    @abstractmethod
    def load(self, entity_id) -> Entity:
        """
        Load the entity from the storage.
        """

    @abstractmethod
    def count(self) -> int:
        """
        Count the persisted entities.
        """

    @abstractmethod
    def exists(self, entity_id) -> bool:
        """
        Check if the entity is persisted.
        """
    
    @abstractmethod
    def commit(self) -> None:
        """
        Commit changes.
        :raises:
        """

    abstractmethod
    def abort(self) -> None:
        """
        Abort changes.
        :raises:
        """
        # revert/rollback
        ...

    def __enter__(self) -> Self:
        return self

    def __exit__(self) -> None:
        self._abort()


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    repo = AbstractRepository()