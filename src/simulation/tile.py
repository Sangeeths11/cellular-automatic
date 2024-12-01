from src.dtoModule.tileDTO import TileDTO
from src.enums.tileStatus import TileStatus

from random import uniform

class Tile():

    def __init__(self, xPositionOnGrid: int, yPositionOnGrid: int, tileStatus: TileStatus) -> None:
        self.xPositionOnGrid = xPositionOnGrid
        self.yPositionOnGrid= yPositionOnGrid
        self.tileStatus: TileStatus = tileStatus
    
    def getTileStatus(self) -> TileStatus:
        return self.tileStatus
    
    def getXPositionOnGrid(self) -> int:
        return self.xPositionOnGrid
    
    def getYPositionOnGrid(self) -> int:
        return self.yPositionOnGrid
    
    def changeState(self, tileStatus: TileStatus) -> bool:
        # TODO make some changeChecks
        self.tileStatus = tileStatus
        return True

    def __repr__(self) -> str:
        if self.tileStatus == TileStatus.FREE:
            return "-"
        if self.tileStatus == TileStatus.BLOCKED:
            return "X"
        if self.tileStatus == TileStatus.PEDESTRIAN:
            return "O"
        if self.tileStatus == TileStatus.SOURCE:
            return "S"
        if self.tileStatus == TileStatus.DESTINATION:
            return "D"
        return "N"