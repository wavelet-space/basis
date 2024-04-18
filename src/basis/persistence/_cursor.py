from typing import Protocol


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

    def fetchall(self) -> list[tuple]: ...

    def fetchmany(self, size: int) -> list[tuple]: ...

    @property
    def arraysize(self) -> int: ...



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
