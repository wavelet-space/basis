"""
Abstractions around PEP 249 <https://peps.python.org/pep-0249/>_
"""


from typing import Protocol


class Cursor(Protocol):
    # REQUIRED

    @property
    def description(self): ...

    @property
    def rowcount(self) -> int: ...

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
    # OPTIONAL
    ...


class Connection(Protocol):
    """Represents a database connection."""

    autocommit: bool

    def close(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def cursor(self) -> Cursor:
        ...
