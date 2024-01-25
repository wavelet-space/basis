from abc import ABC, abstractmethod
from typing import TypeVar, Generic

__all__ = ("Actor",)


class Actor(ABC):
    """
    The actor  is an callable object with additioanal information
    which is better to encapsulate to class instead of function.
    """

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        """
        The asynchronous method.
        """


class Agent(Actor):
    """
    An alias for actor.
    """


T = TypeVar("T")
U = TypeVar("U")


class Message(Generic[T, U]):
    """
    A message delivered to the type T with a content U.
    """

    def __init__(self, content: U):
        self._content = content

    @property
    def content(self) -> U:
        return self._content

    def __eq__(self, other) -> bool:
        return (
            False
            if other is None or not isinstance(other, type(self))
            else other.content == self.content
        )

    def __hash__(self) -> int:
        return hash((type(self), self.content))

    def __str__(self) -> str:
        return f"{type(self)}({self.content})"


class Action(Message):
    """
    The action (or command) is a type of message used in event sourced
    applications to deliver a request to change a domain model.
    """
