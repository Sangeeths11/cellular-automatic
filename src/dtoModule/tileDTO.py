from src.enums.tileStatus import TileStatus

# what is DTO? Please do not use abbreviations that are not clear
class TileDTO():

    def __init__(self, tileStatus: TileStatus, pedastrianValue: float) -> None:
        self.tileStatus = tileStatus
        self.pedastrianValue = pedastrianValue

    def getTileStatus(self) -> TileStatus:
        return self.tileStatus
    
    def setTileStatus(self, tileStatus: TileStatus) -> None:
        self.tileStatus = tileStatus
    
    def getPedestrianValue(self) -> float:
        return self.pedastrianValue
    
    def setPedestrianValue(self, pedastrianValue: float) -> None:
        self.pedastrianValue = pedastrianValue