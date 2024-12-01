from typing import List

class SpawnerConfiguration():
    def __init__(self,
                 spawnerTilesCoordinates: List[tuple],
                 locomotionHeatMapName: str,
                 numberOfTotalSpawns: float=float("inf"),
                 maxSpawnsPerBatch:float=float("inf"),
                 delayBeforeNextSpawn:int = 0,
                 initialDelay:int=0):
        self.spawnerTilesCoordinates = spawnerTilesCoordinates
        self.locomotionHeatMapName = locomotionHeatMapName
        self.numberOfTotalSpawns = numberOfTotalSpawns
        self.maxSpawnsPerBatch = maxSpawnsPerBatch
        self.delayBeforeNextSpawn = delayBeforeNextSpawn
        self.initialDelay = initialDelay

    def getArgs(self)-> dict:
        return {
            "numberOfTotalSpawns": self.numberOfTotalSpawns,
            "locomotionHeatMapName": self.locomotionHeatMapName,
            "maxSpawnsPerBatch": self.maxSpawnsPerBatch,
            "delayBeforeNextSpawn": self.delayBeforeNextSpawn,
            "initialDelay": self.initialDelay
        }
    
    def getSpawnerTilesCoordinates(self) -> List[tuple]:
        return self.spawnerTilesCoordinates