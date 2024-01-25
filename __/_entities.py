# -*- coding: utf-8 -*-


"""
The abstract classes to implements a _Repository pattern_.
"""


from typing import TypeVar, Generic


__all__ = tuple(["Id", "Entity"])


T = TypeVar("T")  # Entity type
Id = TypeVar("Id")


# Id = TypeVar("Id", Hashable) # MUST be immutable e.g. UUID, int etc.


class Entity(Generic[Id]):
    def __init__(self, id: Id):
        self.__id = id

    @property
    def id(self) -> Id:
        return self.__id

    def __eq__(self, that: object) -> bool:
        return isinstance(that, type(self)) and self.id == that.id

    def __hash__(self) -> int:
        return hash([self, self.id])
