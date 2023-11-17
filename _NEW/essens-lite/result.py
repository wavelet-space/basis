"""
Modul obsahuje monádu :py:class:`Result` s podtypy :py:class:`Success` a :py:class:`Failure` reprezentující
správnou respektive chybnou hodnotu. 
"""

from typing import Generic, TypeVar, Self, Any
from dataclasses import dataclass


Value = TypeVar("Value", Any, None)
Error = TypeVar("Error", Exception, None)


# class Nothing
# class Something


@dataclass(frozen=True, slots=True)
class Result(Generic[Value, Error]):
    """
    :param: value
    :param: error
    """
    value: Value = None
    error: Error = None

    def __post_init__(self) -> None:
        match (self.value , self.error):
            case (None, None):
                raise Exception("Either value or error can be None.")
    @classmethod
    def success(cls, value: Value) -> Self:
        """The success result factory method."""
        return Success(value=value, error=None)

    @classmethod
    def failure(cls, error: Error) -> Self:
        """The failure result factory method."""
        return Failure(error=error, value=None)


class Success(Result[Value, Error]):
    def __post_init__(self) -> None:
        if self.value is None:
            raise ValueError("The value must must set!")


class Failure(Result[Value, Error]):
    def __post_init__(self) -> None:
        if self.error is None:
            raise ValueError("The error must be set!")


if __name__ == "__main__":

    value = Result.success(1)
    error = Result.failure(ValueError("reason"))

    print(value)
    print(error)