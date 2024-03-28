from typing import Any, Protocol


class Cursor(Protocol):
    """
    A connection cursor object protocol as defined in PEP 249 <https://peps.python.org/pep-0249/>_.
    """

    @property
    def description(self) -> tuple:  # TODO
        ...

    @property
    def rowcount(self) -> int:
        ...

    def execute(self, query) -> None:
        ...

    #def executemany() -> None:
        #...

    def fetchone(self) -> tuple:
        ...

    # def fetchall() -> None: ...

    # def fetchmany() -> None: ...

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

class SQLCursor(Cursor):
    def __init__(self, cursor: Any) -> None:
        """Takes cursor of any relational database, which implements PEP 249"""
        self._cursor = cursor

    @property
    def description(self) -> tuple:
        """TODO: find if this can even be generalized"""
        return self._cursor.description

    @property
    def rowcount(self) -> int:
        return self._cursor.rowcount

    def close(self) -> None:
        self._cursor.close()

    def execute(self, query) -> None:
        self._cursor.execute(query)

    def fetchone(self) -> tuple:
        return self._cursor.fetchone()