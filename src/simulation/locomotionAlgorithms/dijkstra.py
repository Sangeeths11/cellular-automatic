from typing import List
from src.enums.tileStatus import TileStatus
from src.simulation.destination.pedestrianHeapMap import PedestrianHeapMap
from src.exceptions.simulationException import SimulationException
from src.exceptions.simulationErrorCodes import SimulationErrorCodes
from src.simulation.grid import Grid
from src.simulation.tile import Tile

import numpy as np

class Dijkstra():

    def __init__(self, grid: Grid, destinationTiles: List[tuple]) -> None:
        #Dont use the constructor directly
        self.grid = grid
        self.destinationTiles = destinationTiles
        self.stack: List[tuple] = []
        self.pedestrianHeatMap: PedestrianHeapMap = PedestrianHeapMap(grid.length, grid.width)

    def calculatePedestrianHeapMap(self) -> PedestrianHeapMap:
        self._setStartNodes()
        while len(self.stack) > 0:
            currentNode = self._getNextNode()
            self._evaluateNode(currentNode)
        return self.pedestrianHeatMap

    def _setStartNodes(self):
        for x, y in self.destinationTiles:
            self.pedestrianHeatMap.updateValue(x, y, 0)
            self.stack.append((x, y, 0))

    def _getNextNode(self) -> tuple:
        returnTuple = min(self.stack, key=lambda x: x[2])
        self.stack.remove(returnTuple)
        return returnTuple
    
    def _evaluateNode(self, currentNode) -> None:
        for newX in range(currentNode[0] - 1, currentNode[0] + 2):
            for newY in range(currentNode[1] - 1, currentNode[1] + 2):
                if self.grid.contains(newX, newY) and self.grid.getTileStatus(newX, newY) != TileStatus.BLOCKED:
                    distance = 1 if self._isDiagonalStep(currentNode[0], currentNode[1], newX, newY) else np.sqrt(2)
                    newValue = currentNode[2] + distance
                    if (self.pedestrianHeatMap.getValue(newX, newY) > newValue):
                        self.pedestrianHeatMap.updateValue(newX, newY, newValue)
                        self.stack.append((newX, newY, newValue))
    
    def _isDiagonalStep(self, x:int, y:int, xNew:int, yNew: int) -> bool:
        return (x - xNew)*(y - yNew) == 0


    @classmethod
    def generatePedestrianHeatMap(cls, grid: Grid, destinationTiles: List[tuple]) -> PedestrianHeapMap:
        cls._checkInput(grid, destinationTiles)
        dijkstra = Dijkstra(grid, destinationTiles)
        return dijkstra.calculatePedestrianHeapMap()

    @classmethod
    def _checkInput(cls, grid: Grid, destinationTiles: List[tuple]) -> None:
        if grid == None or destinationTiles == None or len(destinationTiles) < 1:
            raise SimulationException(SimulationErrorCodes.PEDESTRIAN_HEAT_MAP_CALCULATION_FAILED)
        for x, y in destinationTiles:
            if not grid.contains(x, y):
                raise SimulationException(SimulationErrorCodes.PEDESTRIAN_HEAT_MAP_CALCULATION_FAILED)
            