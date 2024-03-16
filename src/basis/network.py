"""
Contains network related functions and classes.
"""

import requests


def read_public_ip() -> str:
    return requests.get("https://checkip.amazonaws.com").text.strip()
