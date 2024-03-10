from dataclasses import dataclass
from typing import Self

# from numbers import Number


@dataclass(frozen=True, slots=True)
class Range[T]:
    minimum: T
    maximum: T

    @property
    def span(self) -> T:
        return abs(self.maximum - self.minimum)

    def __post_init__(self):
        if self.minimum >= self.maximum:
            raise ValueError("Expected the maximum be greater then maximum.")


class Natural:
    """
    A natural number :math:`\\mathbb{N}`.
    """

    def __init__(self, value: int | float) -> Self:
        if 0 > int(value):
            raise ValueError("Expected value be greater the zero.")
        self._value = value

    @property
    def value(self):
        return self._value

    def __hash__(self) -> int:
        return hash((type(self), self.value))

    def __eq__(self, other) -> bool:
        return isinstance(self, type(self)) and self.value == other.value

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value})"


if __name__ == "__main__":
    r = Range(-1, 1)
    print(r, r.span)
    print(repr(r))

    n = Natural(1)
    print(n)


# RESOLVE this older code
# from typing import Tuple, Generic, TypeVar, NewType, Optional


# T = TypeVar("T")

# PositiveInt = NewType('PositiveInt', int)


# def check_positive(n: int) -> PositiveInt:
#     if n < 0:
#         raise ValueError("The number must be a positive integer")
#     return PositiveInt(n)


# def safe_require_positive(n: int) -> Optional[PositiveInt]:
#     try:
#         return check_positive(n)
#     except:
#         return None


# def check_order_asc(*items: T) -> None:
#     for index, value in enumerate(items[1:]):
#         current, previous = value, items[index - 1]
#         if current < previous:
#             print(current, previous)
#             raise ValueError("The i-th value must be greater the (i-1)-th value.")


# class PositiveIntegerRange:
#     def __init__(self, min: PositiveInt, max: PositiveInt):
#         check_positive(min)
#         check_positive(max)
#         check_order_asc(min, max)
#         self._items = range(min, max + 1, 1)

#     @property
#     def items(self):
#         return tuple(self._items)

#     def range(self):
#         for item in self.items:
#             yield item
