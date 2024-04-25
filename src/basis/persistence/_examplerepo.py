from ..aggregate import Entity
import json
from _repository import AbstractSQLRepository, ConflictError, Connection
import datetime
import psycopg2
import sqlite3
from typing import Callable


class Entity1(Entity[int]):
    def __init__(self, identifier: int, real: float, date: datetime.date, json_obj, text: str,
                 integer: int, timestamp: datetime.time):
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

    def save(self, entity: Entity1) -> None:
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
        Check if the entity is alrady persisted.

        :param: ...
        """
        query = f'SELECT * FROM {self._table} WHERE id={self._placeholder}'
        data = (self._get_identifier(entity),)
        cursor = self._context.cursor()
        cursor.execute(query, data)
        return cursor.fetchone() is not None