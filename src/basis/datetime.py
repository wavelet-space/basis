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

# TODO

# tell what time it is somewhere or what some time is somewhere
# e.g 
# NOW
# Time	11:11:57 (0 seconds — late morning)
# Date	2023-11-17
# Zone	Europe/Prague (CET; +0100)
# EXPRESSIONS (PARSE)
# 2 hours ago in yyz
# 5pm in yyz -> sfo
# 5pm in vienna -> london
# 4pm on 17.05.2021 in vienna -> tokyo
# 4pm yesterday in vienna -> vienna va
# in 4 hours in san francisco
# 2pm in 2 days in new delhi
# now in yyz -> sfo -> vie -> lhr
# unix 1639067620 in tokyo
