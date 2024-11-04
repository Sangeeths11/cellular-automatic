from src.dtoModule.tileDTO import TileDTO
from src.enums.tileStatus import TileStatus

class Tile():

    def __init__(self, tileDTO: TileDTO) -> None:
        self.tileDTO = tileDTO

    def getTileDTO(self):
        return self.tileDTO
    
    def changeState(self, tileStatus: TileStatus) -> bool:
        # TODO: implement
        return False