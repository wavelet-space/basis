"""
Modul obsahuje monádu :py:class:`Result` s podtypy :class:`Success` a :class:`Failure` reprezentující
správnou respektive chybnou hodnotu. 
"""

from typing import Generic, TypeVar, Self, Any, final
from dataclasses import dataclass


Value = TypeVar("Value", Any, None)
Error = TypeVar("Error", Exception, None)


@dataclass(frozen=True, slots=True)
class Nothing:
    """Represents the missing value."""


@dataclass(frozen=True, slots=True)
class Result(Generic[Value, Error]):
    """
    :param: value
    :param: error
    """

    value: Value = Nothing
    error: Error = Nothing

    def __post_init__(self) -> None:
        if isinstance(self.value, Nothing) and isinstance(self.error, Nothing):
            raise Exception("Either value or error must be set.")

    @classmethod
    def success(cls, value: Value) -> Self:
        """
        The success result factory method.

        :param value: ...
        :returns: ...
        """
        return Success(value=value, error=Nothing)

    @classmethod
    def failure(cls, error: Error) -> Self:
        """The failure result factory method.

        :param error: ...
        :returns: ...
        """
        return Failure(error=error, value=Nothing)

    def __bool__(self) -> bool:
        match self:
            case Success():
                return True
            case Failure():
                return False


@final
class Success(Result[Value, Error]):
    def __init__(self, value: Value):
        super().__init__(value=value)

    def __post_init__(self) -> None:
        if self.value is Nothing:
            raise ValueError("The value must must set!")


@final
class Failure(Result[Value, Error]):
    def __init__(self, error: Error):
        super().__init__(error=error)

    def __post_init__(self) -> None:
        if self.error is Nothing:
            raise ValueError("The error must be set!")


if __name__ == "__main__":
    s = Result.success(1)
    f = Result.failure(ValueError("Something bad happend"))

    print(isinstance(s, Success))
    print(isinstance(f, Failure))

    print(s.value, s.error)
    print(f.error, f.value)
