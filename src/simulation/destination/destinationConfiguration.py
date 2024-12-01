from typing import List

from src.enums.locomotionAlgorithms import LocomationAlgorihms


class DestinationConfiguration():

    def __init__(self, name:str, destinationTilesCoordination: List[tuple], locomotionAlgorithm: LocomationAlgorihms) -> None:
        self.name = name
        self.destinationTilesCoordination: List[tuple] = destinationTilesCoordination
        self.locomotionAlgorithm = locomotionAlgorithm

    def getName(self) -> str:
        return self.name
    
    def getDestinationTilesCoordination(self) -> List[tuple]:
        return self.destinationTilesCoordination
    
    def getLocomotionAlgorithm(self) -> LocomationAlgorihms:
        return self.locomotionAlgorithm