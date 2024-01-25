"""
This module contains various n-tuples.
"""


class Pair[T]:
    def __init__(self, one: T, two: T) -> None:
        self.__values = (one, two)

    @property
    def first(self) -> T:
        return self.__values[0]

    @property
    def second(self) -> T:
        return self.__values[1]

    def __eq__(self, that) -> bool:
        return self.first, self.last == that.first, that.second

    def __hash__(self) -> int:
        return hash((type(self), self.first, self.second))

    def __copy__(self, that) -> "Pair":
        return type(self)(self.first, self.second)


if __name__ == "__main__":
    pair: Pair[int] = Pair(1, 2)
    print(pair.first, pair.second)
