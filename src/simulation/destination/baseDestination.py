from typing import List
from src.simulation.destination.pedestrianHeapMap import PedestrianHeapMap
from src.simulation.locomotionAlgorithms.dijkstra import Dijkstra
from src.simulation.tile import Tile
from src.simulation.grid import Grid
from src.enums.locomotionAlgorithms import LocomationAlgorihms

class BaseDestination():
    def __init__(self, destinationName: str, destinationTiles: List[tuple], grid: Grid, locomtionAlgorithm: LocomationAlgorihms) -> None:
        self.destinationName: str = destinationName
        self.destinationTiles: List[tuple] = destinationTiles
        self.grid: Grid = grid
        self.locomotionAlgorithm: LocomationAlgorihms = locomtionAlgorithm
        self.pedestrianHeatMap: PedestrianHeapMap = None

    def generatePedestrianHeatMap(self) -> None:
        if self.locomotionAlgorithm == LocomationAlgorihms.dijksta:
            self.pedestrianHeatMap = Dijkstra.generatePedestrianHeatMap(self.grid, self.destinationTiles)
    
    def getPedestrianHeatMap(self) -> PedestrianHeapMap:
        return self.pedestrianHeatMap
    
    def __repr__(self) -> str:
        return f"DestiantionName: <{self.destinationName}>\nlocomationAlgorithm: <{self.locomotionAlgorithm}>\n-pedestrianHeatMap-  \n{str(self.pedestrianHeatMap)}"

    