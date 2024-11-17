from typing import List

class SpawnerConfiguration():
    def __init__(self,
                 spawnerTilesCoordinates: List[tuple],
                 numberOfTotalSpawns: float=float("inf"),
                 maxSpawnsPerBatch:float=float("inf"),
                 delayBeforeNextSpawn:int = 0,
                 initialDelay:int=0):
        self.spawnerTilesCoordinates = spawnerTilesCoordinates
        self.numberOfTotalSpawns = numberOfTotalSpawns
        self.maxSpawnsPerBatch = maxSpawnsPerBatch
        self.delayBeforeNextSpawn = delayBeforeNextSpawn
        self.initialDelay = initialDelay

    def getArgs(self)-> dict:
        return {
            "numberOfTotalSpawns": self.numberOfTotalSpawns,
            "maxSpawnsPerBatch": self.maxSpawnsPerBatch,
            "delayBeforeNextSpawn": self.delayBeforeNextSpawn,
            "initialDelay": self.initialDelay
        }
    
    def getSpawnerTilesCoordinates(self) -> List[tuple]:
        return self.spawnerTilesCoordinates