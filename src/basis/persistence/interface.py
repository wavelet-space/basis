"""
Abstraction as defined in PEP 249 <https://peps.python.org/pep-0249/>_.
"""

from typing import Protocol


class Cursor(Protocol):
    """
    A connection cursor object protocol.
    """

    @property
    def description(self):
        ...

    @property
    def rowcount(self) -> int:
        ...

    # execute()
    # execuremany()
    # fetchone()
    # fetchmany()
    # fetchall()
    # nextset()
    # arraysize()
    # setinputsize()
    # setoutputsize()


class CursorExtended(Cursor):
    """
    A connection cursor object protocol with optional features.
    """

    ...


class Connection(Protocol):
    """
    A database connection object.
    """

    autocommit: bool

    def close(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def cursor(self) -> Cursor:
        ...
