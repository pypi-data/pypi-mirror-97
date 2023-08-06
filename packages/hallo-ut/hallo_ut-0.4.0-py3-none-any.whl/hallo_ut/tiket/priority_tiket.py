from enum import Enum


class PriorityTiket(Enum):
    LOW = 1, "Low"
    MEDIUM = 2, "Medium"
    HIGH = 3, "High"

    def __str__(self) -> str:
        return self.value[1]

    @property
    def id(self) -> int:
        return self.value[0]
