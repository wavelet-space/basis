from typing import Protocol

from ._cursor import Cursor


class Connection(Protocol):
    """
    A database connection object as defined in PEP 249 <https://peps.python.org/pep-0249/>_.

    .. seealso::

        The `connection object <https://peps.python.org/pep-0249/#connection-objects>`_

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


class Type:
    """
    A database type.

    .. seealso::

        The `type object <https://www.python.org/dev/peps/pep-0249/#type-objects>`_
    """


class AsyncConnector:
    autocommit: bool

    async def close(self) -> None:
        ...

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...

    async def cursor(self) -> Cursor:
        ...
