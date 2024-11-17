from src.dtoModule.tileDTO import TileDTO
from src.simulation.tile import Tile
from src.enums.tileStatus import TileStatus
from src.exceptions.simulationException import SimulationException
from src.exceptions.simulationErrorCodes import SimulationErrorCodes

class Grid():

    def __init__(self, length, width) -> None:
        self.length = length
        self.width = width
        self.tiles: list[list] = self._initTiles()

    def __repr__(self) -> str:
        returnString = ""
        for line in self.tiles:
            for tile in line:
                returnString += str(tile)
            returnString += "\n"
        return returnString

    def getTiles(self) -> list[list]:
        return self.tiles
    
    def getTile(self, x: int, y: int) -> Tile:
        if not self.contains(x, y):
            raise SimulationException(SimulationErrorCodes.POINT_NOT_ON_GRID)
        return self.tiles[x][y]
        
    def simulate(self):
        #TODO: Create a smart way to step in time
        pass

    def updateTileValues(self) -> None:
        #TODO: Find a way to update the TileValues
        pass

    def contains(self, x: int, y: int) -> bool:
        return -1 < x < self.length and -1 <= y < self.width

    def _initTiles(self) -> list[list]:
        return [
            [Tile(TileDTO(TileStatus.FREE, 0)) for _ in range(self.width)]
            for __ in range(self.length)
        ]
    