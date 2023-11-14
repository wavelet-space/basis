"""
This module contains date and time related functions.
"""

from datetime import datetime

def timestamp_to_date(timestamp: float) -> str:
    """
    :param timestamp: A POSIX timestamp like `time.time()`.
    :returns: An ISO 8601 formated date string.
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")