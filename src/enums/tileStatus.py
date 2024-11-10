from enum import Enum

class TileStatus(Enum):
    FREE = 1
    BLOCKED = 2
    PEDESTRIAN = 3
    SOURCE = 4
    DESTINATION = 5