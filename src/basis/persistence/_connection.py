from typing import Protocol

from ._cursor import Cursor, SQLCursor


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


class SQLConnection(Connection):
    """
    A database connection object which uses object,
    that already works according to the PEP 249
    """
    def __init__(self, library, *args, **kwargs):
        # TODO: probably add some way to check if connection was successful?
        # is this even a good idea? maybe just let the errors surface as normal?
        # TODO: add way to use autocommit
        self.connection = library.connect(*args, **kwargs)

    def close(self) -> None:
        self.connection.close()

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()

    def cursor(self) -> Cursor:
        return SQLCursor(self.connection.cursor())