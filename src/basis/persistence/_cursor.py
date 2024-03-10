from typing import Any, Protocol


class Cursor(Protocol):
    """
    A connection cursor object protocol as defined in PEP 249 <https://peps.python.org/pep-0249/>_.
    """

    @property
    def description(self) -> Any:  # TODO
        ...

    @property
    def rowcount(self) -> int:
        ...

    def execute() -> None:
        ...

    def executemany() -> None:
        ...

    # def fetchone() -> None: ...

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
