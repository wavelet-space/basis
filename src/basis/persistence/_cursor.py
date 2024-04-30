from typing import Protocol, Any
from abc import abstractmethod


class Cursor(Protocol):
    """
    A connection cursor object protocol as defined in PEP 249 <https://peps.python.org/pep-0249/>_.
    """

    @property
    @abstractmethod
    def description(self) -> tuple:  # TODO
        ...

    @property
    @abstractmethod
    def rowcount(self) -> int:
        ...

    def execute(self, query, data=None) -> None:
        ...

    def executemany(self, query, data=None) -> None:
        ...

    def fetchone(self) -> tuple:
        ...

    def fetchall(self) -> list[tuple]:
        ...

    def fetchmany(self, size: Any) -> list[tuple]:
        ...

    # @property
    # @abstractmethod
    # def arraysize(self) -> Any:
    #     ...

    # ##################################################################### #

    # def nextset() -> None: ...

    # def arraysize() -> None: ...

    # def setinputsize() -> None: ...

    # def setoutputsize() -> None: ...


class CursorExtended(Cursor):
    """
    A connection cursor object protocol with optional features.
    """

    ...
