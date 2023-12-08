import abc
from typing import TypeVar, Generic, Optional, Tuple


Value = TypeVar("Value", covariant=True)
Error = TypeVar("Error", covariant=True) 


class Result(Generic[Value, Error]):

    __slots__ = ("_value", "_error")
    
    def __init__(self, value: Optional[Value], error: Optional[Error]) -> None:
        self._value = value
        self._error = error

    @property
    def value(self) -> Value:
        return self._value

    @property
    def error(self) -> Tuple[Error]:
        return self._error
    
    @abc.abstractmethod
    def __bool__(self) -> bool:
        pass
    
    def __eq__(self, that: object) -> bool:
        return isinstance(that, type(self)) and (self.value, self.error) == (that.value, that.error)
    
    def __hash__(self) -> int:
        return hash([self.value, self.error])
                    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value}, error={self.error})"


class Success(Result[Value, None]):
    """
    The success result type.
    """
    def __init__(self, value: Value) -> None:
        super().__init__(value=value, error=None)

    def __bool__(self) -> bool:
        return True


class Failure(Result[None, Error]):
    """
    The failure result type.
    """
    def __init__(self, error: Error) -> None:
        super().__init__(value=None, error=error)

    def __bool__(self) -> bool:
        return False



if __name__ == "__main__":
    # Development: remove after prototyping phase.

    success = Success(1)
    print(bool(success))

    failure = Failure(0)
    print(bool(failure))