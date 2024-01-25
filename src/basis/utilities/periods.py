"""
This module contains functions to work with date and time periods.

e.g. Get
- every monday this year
- days of current month

"""

from typing import Iterator
from datetime import datetime, timedelta
from enum import StrEnum, auto, unique


@unique
class Resolution(StrEnum):
    WEEKS = auto()
    DAYS = auto()
    HOURS = auto()
    MINUTES = auto()
    MILISECONDS = auto()
    MICROSECONDS = auto()


def between(
    start: datetime,
    end: datetime,
    step: int = 1,
    resolution: Resolution = Resolution.DAYS,
) -> Iterator[datetime]:
    """Generate datetime units between start and end datetime.

    :param start: The start :class:`datetime` value.
    :param end: The end :class:`datetime` value.
    :param step: The :class:`timedelta` resolution step value (can be negative).
    :param resolution: The :class:`timedelta` resolution e.g  days or hours.
    """
    current = start
    while current < end:
        yield current
        current += timedelta(**{str(Resolution.DAYS): step})


if __name__ == "__main__":
    period = between(datetime.now(), datetime.now() + timedelta(days=3))
    for i in period:
        print(i)
