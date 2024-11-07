from src.dtoModule.tileDTO import TileDTO
from src.enums.tileStatus import TileStatus

from random import uniform

# sure it's a tile?
class Tile():

    def __init__(self, tileDTO: TileDTO) -> None:
        self.tileDTO = tileDTO

    def getTileDTO(self):
        return self.tileDTO
    
    def changeState(self, tileStatus: TileStatus) -> bool:
        # TODO make some changeChecks
        self.tileDTO.setTileStatus(tileStatus)
        return True
    
    def updatePedastrianValue(self) -> None:
        #TODO make some updatePolicy
        self.tileDTO.setPedestrianValue(uniform(1, 10))