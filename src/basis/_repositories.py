"""
The abstract classes to implements a _Repository pattern_.
"""


from abc import ABC, abstractmethod, abstractclassmethod
from typing import Iterable, TypeVar, Generic, Any, Optional


T = TypeVar("T")  # Entity type
Id = TypeVar("Id")


from uuid import UUID  # vs SafeUUID?


class PersistenceError(Exception):
    def __init__(self, message, *errors):
        super().__init__(self, message)
        self.errors = errors


class Repository(Generic[T, Id]):
    """
    Generic abstract repository class for aggregate root entities.

    TODO Check that `type(T.id)`` match `Id` type.
    """

    def __init__(self, connection):
        self.connection = connection

    @abstractclassmethod
    def next_id() -> Id:
        """
        Get the next availaible identity.
        """

    def save(self, entity) -> None:
        ...

    def save_all(self, entities) -> None:
        ...

    def find_one(self, predicate) -> T:
        ...

    def find_all(self, predicate) -> Iterable[T]:
        ...


# T = TypeVar("T", bound=Entity, covariant=True)  # Entity type


class AbstractRepository(ABC, Generic[T]):

    def __init__(self, connection: Any):
        self.connection = connection  # connection pool?

    @abstractmethod
    def count(self) -> int:
        """
        Count a stored <room>s
        """

    @abstractmethod
    def exists(self, entity: T) -> bool:
        """
        Check id the given <room> exists.
        """

    @abstractmethod
    def save_one(self, entity: T) -> None:
        """
        Save the <room> aggregate.
        """

    @abstractmethod
    def find_one(self, id: UUID) -> Optional[T]:
        """
        Find the <room> aggregate.
        """
