# -*- coding: utf-8 -*-


from typing import Tuple, Generic, TypeVar, NewType, Optional


__all__ = tuple(("Pair", "PositiveIntegerRange"))


T = TypeVar("T")

PositiveInt = NewType('PositiveInt', int)


def check_positive(n: int) -> PositiveInt:
    if n < 0:
        raise ValueError("The number must be a positive integer")
    return PositiveInt(n)


def safe_require_positive(n: int) -> Optional[PositiveInt]:
    try:
        return check_positive(n)
    except:
        return None


def check_order_asc(*items: T) -> None:
    for index, value in enumerate(items[1:]):
        current, previous = value, items[index - 1]
        if current < previous:
            print(current, previous)
            raise ValueError("The i-th value must be greater the (i-1)-th value.")


class Pair(Generic[T]):
    def __init__(self, one: T, two: T) -> None:
        self.__values = (one, two)

    @property
    def first(self) -> T:
        return self.__values[0]

    @property
    def second(self) ->T:
        return self.__values[1]

    def __eq__(self, that) -> bool:
        return self.first, self.last == that.first, that.second

    def __hash__(self) -> int:
        return hash((type(self), self.first, self.second))

    def __copy__(self, that) -> 'Pair':
        return type(self)(self.first, self.second)


class PositiveIntegerRange:
    def __init__(self, min: PositiveInt, max: PositiveInt):
        check_positive(min)
        check_positive(max)
        check_order_asc(min, max)
        self._items = range(min, max + 1, 1)

    @property
    def items(self):
        return tuple(self._items)

    def range(self):
        for item in self.items:
            yield item


if __name__ == "__main__":

    pair: Pair[int] = Pair(1, 2)

    print(
        pair.first,
        pair.second
    )
