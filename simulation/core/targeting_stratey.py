from enum import Enum


class TargetingStrategy(Enum):
    RANDOM = 1,
    CLOSEST = 2,
    FARTHEST = 3