"""
Abstractions around PEP 249 <https://peps.python.org/pep-0249/>_
"""

from typing import Protocol


class CursorLike(Protocol):
    """Represents a database connection cursor"""


class Connection(Protocol):
    """Represents a database connection."""

    autocommit: bool

    def close(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def cursor(self) -> CursorLike:
        ...


class Cursor(Protocol):
    ...
