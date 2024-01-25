# -*- coding: utf-8 -*-

"""
FIXME
"""

from uuid import UUID


__all__ = tuple(("Application"))


class Application:  # (Service):
    """
    The application service or application is top-level service which comunicates
    with the external world and is responsible for managing and delegatig the
    application tasks aka use cases. It is the only class which should be
    instantiated in the `__main__` module.
    """

    def __init__(self, id: UUID, name: str, status: object = None):
        self.id = id
        self.name = name
        self.status = status
        # super().__init__(self, id, name, status)
