# -*- coding: utf-8 -*-

"""
This module contains helpers for implementing factories for an aggregates.
"""

from typing import Callable, TypeVar, Any

__all__ = tuple(())


E = TypeVar("E", Any) # FIXME Entity
I = TypeVar("I", Any) # FIXME Identitfier for Entity identity

# Factory can be simply a function with the following signature:

Factory = Callable[[Any], E] # Get arguments and return Entity.
