
from abc import ABC, abstractmethod
from typing import Self
from pathlib import Path

import tempfile 


class Transaction(ABC):

    @abstractmethod
    def __enter__(self) -> Self:
        pass
    
    @abstractmethod
    def __exit__(self) -> None:
        pass


def transactional():
    """A decorator for functions to run in transaction."""
    ...


class PostgreSQLTransaction(Transaction):
    def __enter__(self) -> Self:
        ...

    def __exit__(self) -> None:
        ...


class FileSystemTransaction(Transaction):
    """
    An atomic operation for file system.
    """

    def __init__(self, path: Path, timeout=42):
        if not path.is_dir():
            raise ValueError(f"The provided path `{path}` is not a directory.")
        
    def __enter__(self) -> Self:
        ...

    def __exit__(self) -> None:
        ...

    