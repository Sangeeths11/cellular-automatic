from src.dtoModule.tileDTO import TileDTO
from src.enums.tileStatus import TileStatus

from random import uniform

class Tile():

    def __init__(self, tileDTO: TileDTO) -> None:
        self.tileDTO = tileDTO

    def getTileDTO(self):
        return self.tileDTO
    
    def getTileStatus(self) -> TileStatus:
        return self.tileDTO.getTileStatus()
    
    def changeState(self, tileStatus: TileStatus) -> bool:
        # TODO make some changeChecks
        self.tileDTO.setTileStatus(tileStatus)
        return True
    
    def updatePedastrianValue(self) -> None:
        #TODO make some updatePolicy
        self.tileDTO.setPedestrianValue(uniform(1, 10))

    def __repr__(self) -> str:
        status: TileStatus = self.tileDTO.getTileStatus()
        if status == TileStatus.FREE:
            return "-"
        if status == TileStatus.BLOCKED:
            return "X"
        if status == TileStatus.PEDESTRIAN:
            return "O"
        if status == TileStatus.SOURCE:
            return "S"
        if status == TileStatus.DESTINATION:
            return "D"
        return "N"