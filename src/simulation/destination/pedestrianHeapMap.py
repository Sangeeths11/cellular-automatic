from typing import List


class PedestrianHeapMap():
    
    def __init__(self, length: int, width: int) -> None:
        self.heatMap: List[List[float]] = [[float("inf") for _ in range(width)] for _ in range(length)]

    def updateValue(self, x: int, y: int, value: float) -> None:
        #TODO Check for bounderies
        self.heatMap[x][y] = value
    
    def getValue(self, x: int, y:int) -> float:
        return self.heatMap[x][y]
    
    def __repr__(self) -> str:
        returnValue = ""
        for line in self.heatMap:
            returnValue += "["
            for value in line:
                returnValue +=f"{value: .2f}, "
            returnValue += "]\n"
        return returnValue