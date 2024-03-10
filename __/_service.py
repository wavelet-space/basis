# -*- coding: utf-8 -*-

"""
FIXME
"""


from uuid import UUID

__all__ = tuple(("Service"))


class Service:  # Versionable, Configurable.
    def __init__(self, id: UUID, name: str, status: object):
        self.id = id
        self.name = name
        self.status = status

    def __call__(self) -> None:
        """
        Run the service.
        """
