

class BaseAgent():

    def __init__(self, currentLocationX: int, currentLocationY: int, locomotionHeatMapName: str) -> None:
        self.locomotionHeatMapName = locomotionHeatMapName
        self.currentLocationX = currentLocationX
        self.currentLocationY = currentLocationY

    def getCurrentLocationX(self) -> int:
        return self.currentLocationX
    
    def setCurrentLocationX(self, currentLocationX: int) -> None:
        self.currentLocationX = currentLocationX

    def getCurrentLocationY(self) -> int:
        return self.currentLocationY
    
    def setCurrentLocationY(self, currentLocationY: int) -> None:
        self.currentLocationY
    
    def getLocomotionHeatMapName(self) -> str:
        return self.locomotionHeatMapName
    
    def setLocomotionHeatMapName(self, locomotionHeatMapName: str) -> None:
        self.locomotionHeatMapName = locomotionHeatMapName