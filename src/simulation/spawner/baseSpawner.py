from src.enums.tileStatus import TileStatus
from src.simulation.tile import Tile
from typing import List
import random

class BaseSpawner():
    def __init__(self, spawnerTiles: List[Tile], numberOfTotalSpawns: float=float("inf"), maxSpawnsPerBatch:float=float("inf"), delayBeforeNextSpawn:int = 0, initialDelay:int=0) -> None:
        self.spawnerTiles = spawnerTiles
        self.numberOfTotalSpawns = numberOfTotalSpawns
        self.maxSpawnsPerBatch = maxSpawnsPerBatch
        self.delayBeforeNextSpawn = delayBeforeNextSpawn
        self.initalDelay = initialDelay
        self.timestampsElapsedSinceLastSpawn = 0
        self.totalSpawend = 0

    def update(self) -> None:
        if(self.timestampsElapsedSinceLastSpawn <= self.delayBeforeNextSpawn):
            self._spawn()
            self.timestampsElapsedSinceLastSpawn = 0
        else:
            self.timestampsElapsedSinceLastSpawn += 1

    def _spawn(self) -> None:
        numberOfSpawns = self._getNumberOfSpawns()
        random.shuffle(self.spawnerTiles)
        spawned = 0
        currentSpawnerTilePosition = 0
        while spawned < numberOfSpawns:
            if (self.spawnerTiles[currentSpawnerTilePosition].tileDTO.getTileStatus() == TileStatus.FREE):
                self.spawnerTiles[currentSpawnerTilePosition].changeState(TileStatus.PEDESTRIAN)
                spawned += 1
            currentSpawnerTilePosition += 1


    def _getNumberOfSpawns(self) -> float:
        return min(self.maxSpawnsPerBatch, self.numberOfTotalSpawns - self.totalSpawend, self._getNumberOfFreeTiles())

    def _getNumberOfFreeTiles(self) -> float:
        freeTiles: float = 0.0
        for tile in self.spawnerTiles:
            if tile.tileDTO.getTileStatus() == TileStatus.FREE:
                freeTiles += 1.0
        return freeTiles
    
    def __repr__(self) -> str:
        return str(self.totalSpawend)