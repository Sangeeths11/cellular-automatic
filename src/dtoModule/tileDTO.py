from src.enums.tileStatus import TileStatus

class TileDTO():

    def __init__(self, tileStatus: TileStatus, pedastrianValue: float) -> None:
        self.tileStatus = tileStatus
        self.pedastrianValue = pedastrianValue

    def getTileStatus(self) -> TileStatus:
        return self.tileStatus
    
    def getPedestrianValue(self) -> float:
        return self.pedastrianValue
    
    def setPedestrianValue(self) -> None:
        return self.pedastrianValue