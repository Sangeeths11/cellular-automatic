from enum import Enum, IntEnum


class CellState(IntEnum):
    FREE = 0,
    OCCUPIED = 1,
    OBSTACLE = 2