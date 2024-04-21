"""
FIXME

Should ewe use connection pool?
https://stackoverflow.com/questions/11889104/
"""

from basis.persistence._connection import Connection

class Connector:
    """
    Connector is a factory class which provides a connection object. 
    It either creates a new one or select one from connection pool.
    """

    def __init__(self, credentials, configuration) -> None:
        self._credentials = credentials
        self._configuration = configuration

    async def get_connection(self) -> Connection:
        ...

    async def get_pooled_connection(self) -> Connection: 
        # import psycopg_pool
        # psycopg_pool.ConnectionPool(conninfo=credentials)
        ...

    @property
    def credentials(self):
        return self._credentials
    
    @property
    def configuration(self):
        return self._configuration


if __name__ == "__main__":
    pass