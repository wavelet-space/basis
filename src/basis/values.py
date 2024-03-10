from dataclasses import dataclass

__all__ = ["SingleCaseValue"]


@dataclass(frozen=True, slots=True)
class SingleCaseValue[T]:
    """
    Represents a data class with a single value.

    This is a convention, so you don't have to think about how to name a value attribute.

    Example:

    .. code-block:: python

        @dataclass(frozen=True, slots=True)
        class Name(SingleCaseValue):
            def __post_init__(self) -> None:
                if len(self.value) == 0:
                    raise ValueError("empty name is not allowed")

    """

    value: T
