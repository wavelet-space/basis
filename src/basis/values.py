from dataclasses import dataclass


__all__ = ["SingleCaseValue"]


@dataclass(frozen=True, slots=True)
class SingleCaseValue[T]:
    value: T
