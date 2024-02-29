# -*- coding: utf-8 -*-

"""
FIXME
"""


from essence.core._protocols import Singleton


__all__ = tuple(("Environment"))


class Environment(Singleton):
    def __init__(self, *args, **kwargs):
        self.args = args
