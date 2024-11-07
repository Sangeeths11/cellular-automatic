from enum import Enum

# since it is a *cell*ular automaton, there might be a more appropriate name than tile;-)?
def TileStatus(Enum):
    FREE = 1
    BLOCKED = 2
    PEDESTRIAN = 3
    SOURCE = 4
    DESTINATION = 5