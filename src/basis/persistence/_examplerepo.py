import os

from ..aggregate import Entity
import json
from _repository import AbstractSQLRepository, ConflictError, Connection, RestRepository
import datetime
from typing import Callable, Any


class Entity1(Entity[int]):
    def __init__(self,
                 identifier: int = None,
                 real: float = None,
                 date: datetime.date = None,
                 json_obj=None,
                 text: str = None,
                 integer: int = None,
                 timestamp: datetime.time = None):
        super().__init__(identifier)
        self.float = real
        self.date = date
        self.json = json.dumps(json_obj)
        self.text = text
        self.integer = integer
        self.timestamp = timestamp


class SqlRepository1(AbstractSQLRepository[Entity1, int]):
    """Implemented an Example Sql repository
        It should work for most sql databases due to simplicity of used queries.

        The only problem for now, is that when fetching, simple databases cannot convert it back to the original format

        For sqlite handles datetime fine, but when fetching it returns as date string. 
    """

    def __init__(self, context: Connection, placeholder: str, table_name: str,
                 identity_function: Callable = None):
        super().__init__(context, identity_function)
        self._placeholder = placeholder
        self._table = table_name

    def save(self, entity: Entity1) -> int:
        """
        Save the entity to the storage.
        """
        if self.exists(entity):
            raise ConflictError("Entity with same identifier already exists.")
        query = "INSERT INTO {0} VALUES({1}, {1}, {1}, {1}, {1}, {1}, {1})".format(self._table, self._placeholder)
        data = (entity.identifier,
                entity.float,
                entity.date,
                entity.json,
                entity.text,
                entity.integer,
                entity.timestamp)
        self._context.cursor().execute(query, data)
        return self._get_identifier(entity)

    def find(self, entity_id: int) -> Entity1 | None:  # Entity[Identifier]
        """
        Find the entity in the storage.
        """
        query = f"SELECT * FROM {self._table} WHERE id={self._placeholder}"
        data = (entity_id,)
        cursor = self._context.cursor()
        cursor.execute(query, data)
        values = cursor.fetchone()
        if values is None:
            return None

        return Entity1(values[0], values[1], values[2], values[3], values[4], values[5], values[6])

    def count(self) -> int:
        """
        Count the persisted entities.
        """
        query = f'SELECT COUNT(*) FROM {self._table}'
        cursor = self._context.cursor()
        cursor.execute(query)
        return cursor.fetchone()[0]

    def exists(self, entity: Entity1) -> bool:
        """
        Check if the entity is already persisted.

        :param: ...
        """
        query = f'SELECT * FROM {self._table} WHERE id={self._placeholder}'
        data = (self._get_identifier(entity),)
        cursor = self._context.cursor()
        cursor.execute(query, data)
        return cursor.fetchone() is not None


class MockRequester:
    _server = {}

    def get(self, url) -> dict:
        if url in self._server.keys():
            return self._server[url]
        else:
            ValueError(f"Resource {url} not found.")

    def put(self, url, data: dict):
        if url in self._server.keys():
            for key in data.keys():
                self._server[url][key] = data[key]
        else:
            raise ValueError(f"Resource {url} not found.")

    def post(self, url, data: dict):
        if url not in self._server.keys():
            self._server[url] = data
        else:
            raise ValueError(f"Resource {url} already exists.")

    def delete(self, url: str):
        if url in self._server.keys():
            del self._server[url]
        else:
            raise ValueError(f"Resource {url} doesn't exist to be deleted.")

    def get_count_with(self, key_start: str) -> int:
        wanted_keys = [key for key in self._server.keys() if key.startswith(key_start)]
        return len(wanted_keys)


FLOAT = 'FLOAT'
DATE = 'DATE'
JSON = 'JSON'
TEXT = 'TEXT'
INTEGER = 'INTEGER'
TIMESTAMP = 'TIMESTAMP'


class ExampleRestRepository(RestRepository[Entity1, int, dict[str, Any]]):
    def __init__(self, entity_uri):
        super().__init__('url', entity_uri)
        self._requester = MockRequester()

    def _to_data(self, entity: Entity1) -> dict[str, Any]:
        return {FLOAT: entity.float,
                DATE: entity.date,
                JSON: entity.json,
                TEXT: entity.text,
                INTEGER: entity.integer,
                TIMESTAMP: entity.timestamp}

    def _to_entity(self, data: dict[str, Any]) -> Entity1:
        entity = Entity1()
        entity.float = data[FLOAT]
        entity.date = data[DATE]
        entity.integer = data[INTEGER]
        entity.text = data[TEXT]
        entity.json = data[JSON]
        entity.timestamp = data[TIMESTAMP]
        return entity

    def count(self) -> int:
        return self._requester.get_count_with(os.path.join(self._base_url, self._entity_uri))
