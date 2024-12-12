from enum import Enum, IntEnum


class TargetingStrategy(IntEnum):
    RANDOM = 1,
    CLOSEST = 2,
    FARTHEST = 3