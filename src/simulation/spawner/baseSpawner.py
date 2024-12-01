from src.enums.tileStatus import TileStatus
from src.simulation.tile import Tile
from src.simulation.agent.baseAgent import BaseAgent
from typing import List
import random

class BaseSpawner():
    def __init__(self, spawnerTiles: List[Tile], locomotionHeatMapName: str, numberOfTotalSpawns: float=float("inf"), maxSpawnsPerBatch:float=float("inf"), delayBeforeNextSpawn:int = 0, initialDelay:int=0) -> None:
        self.spawnerTiles = spawnerTiles
        self.locomotionHeatMapName = locomotionHeatMapName
        self.numberOfTotalSpawns = numberOfTotalSpawns
        self.maxSpawnsPerBatch = maxSpawnsPerBatch
        self.delayBeforeNextSpawn = delayBeforeNextSpawn
        self.initalDelay = initialDelay
        self.timestampsElapsedSinceLastSpawn = 0
        self.totalSpawend = 0

    def update(self) -> List[BaseAgent]:
        if(self.timestampsElapsedSinceLastSpawn <= self.delayBeforeNextSpawn):
            self.timestampsElapsedSinceLastSpawn = 0
            return self._spawn()
        else:
            self.timestampsElapsedSinceLastSpawn += 1
            return []

    def _spawn(self) -> List[BaseAgent]:
        numberOfSpawns = self._getNumberOfSpawns()
        random.shuffle(self.spawnerTiles)
        spawnedAgents = []
        currentSpawnerTilePosition = 0
        while len(spawnedAgents) < numberOfSpawns:
            if (self.spawnerTiles[currentSpawnerTilePosition].getTileStatus() == TileStatus.FREE):
                self.spawnerTiles[currentSpawnerTilePosition].changeState(TileStatus.PEDESTRIAN)
                spawnedXPosition = self.spawnerTiles[currentSpawnerTilePosition].getXPositionOnGrid()
                spawnedYPosition = self.spawnerTiles[currentSpawnerTilePosition].getYPositionOnGrid()
                spawnedAgents.append(BaseAgent(spawnedXPosition, spawnedYPosition, self.locomotionHeatMapName))
            currentSpawnerTilePosition += 1
        self.totalSpawend += len(spawnedAgents)
        return spawnedAgents


    def _getNumberOfSpawns(self) -> float:
        if(self.totalSpawend >= self.numberOfTotalSpawns):
            return 0
        return min(self.maxSpawnsPerBatch, self.numberOfTotalSpawns - self.totalSpawend, self._getNumberOfFreeTiles())

    def _getNumberOfFreeTiles(self) -> float:
        freeTiles: float = 0.0
        for tile in self.spawnerTiles:
            if tile.getTileStatus() == TileStatus.FREE:
                freeTiles += 1.0
        return freeTiles
    
    def __repr__(self) -> str:
        return str(self.totalSpawend)