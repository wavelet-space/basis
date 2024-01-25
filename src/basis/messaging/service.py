from abc import abstractmethod
from uuid import UUID

from basis.messaging.actor import Actor


class Service(Actor):
    def __init__(self, id: UUID, name: str, version: str, summary: str):
        super().__init__()
        self.id = id
        self.name = name
        self.version = version
        self.summary = summary

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        """
        The asynchronous method.
        """

    @property
    def summary(self) -> str:
        """
        Returns the summary about service.
        """
