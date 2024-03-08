from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Message:
    type: str = field(init=False, repr=False)
    name: str
    data: Any


@dataclass(frozen=True, slots=True)
class Event(Message):
    ...
