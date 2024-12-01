from src.enums.tileStatus import TileStatus
from src.exceptions.simulationErrorCodes import SimulationErrorCodes
from src.exceptions.simulationException import SimulationException
from src.simulation.spawner.spawnerConfiguration import SpawnerConfiguration
from src.simulation.destination.baseDestination import BaseDestination
from src.simulation.destination.destinationConfiguration import DestinationConfiguration
from src.simulation.spawner.baseSpawner import BaseSpawner
from src.simulation.agent.baseAgent import BaseAgent
from src.simulation.destination.pedestrianHeapMap import PedestrianHeapMap
from src.simulation.grid import Grid
from src.simulation.tile import Tile
from src.dtoModule.tileDTO import TileDTO
from src.config.config import _Config
from typing import List, Tuple
import os
import numpy as np

class BaseSimulation():

    def __init__(self, grid: Grid, config: _Config) -> None:
        self.grid: Grid = grid
        self.config: _Config = config
        self.agents: List[BaseAgent] = []
        self.tilesOverTime: List[List[List[int]]] = []
        self.spawners: List[BaseSpawner] = []
        self.destinations: List[BaseDestination] = []

    def simulateStep(self) -> None:
        self._calculateDestinationHeatMaps()
        self._spawn()
        self._step()
        self._saveStep()
    
    def setSpawner(self, spawnerConfiguration: SpawnerConfiguration) -> None:
        spawnerTiles: List[Tile] = []
        for x, y in spawnerConfiguration.getSpawnerTilesCoordinates():
            spawnerTiles.append(self.grid.getTile(x, y))
        baseSpawner: BaseSpawner = BaseSpawner(spawnerTiles, **spawnerConfiguration.getArgs())
        self.spawners.append(baseSpawner)

    def setDestination(self, destinationConfiguration: DestinationConfiguration) -> None:
        baseDestination: BaseDestination = BaseDestination(destinationName=destinationConfiguration.getName(), destinationTiles=destinationConfiguration.getDestinationTilesCoordination(), grid=self.grid, locomtionAlgorithm=destinationConfiguration.getLocomotionAlgorithm())
        self.destinations.append(baseDestination)

    def setBlockingCells(self, blockList: List[tuple]) -> None:
        for x, y in blockList:
            self.grid.setTileStatus(x, y, TileStatus.BLOCKED)

    def getTilesOverTime(self) -> List[List[List[Tile]]]:
        return self.tilesOverTime
    
    def save(self, name: str) -> None:
        if not os.path.exists(self.config.getSavePath()):
            os.makedirs(self.config.getSavePath())
        savePath = os.path.join(self.config.getSavePath(), f"{name}.npy")
        numpyArray = np.array(self.tilesOverTime)
        np.save(savePath, numpyArray)

    def _calculateDestinationHeatMaps(self) -> None:
        for destination in self.destinations:
            destination.generatePedestrianHeatMap()

    def _spawn(self) -> None:
        for spawner in self.spawners:
            self.agents.extend(spawner.update())

    def _step(self) -> None:
        for agent in self.agents:
            self._updateAgent(agent)

    def _updateAgent(self, agent: BaseAgent) -> None:
        pedestrianHeatMap: PedestrianHeapMap = self._getPedestrianHeatMapByName(agent.getLocomotionHeatMapName())
        targetPostion: Tuple[int, int] = self._getLowestFreePosition(agent, pedestrianHeatMap)
        
        self.grid.setTileStatus(*targetPostion, TileStatus.PEDESTRIAN)
        self.grid.setTileStatus(agent.getCurrentLocationX(), agent.getCurrentLocationY(), TileStatus.FREE)
        
        agent.setCurrentLocationX(targetPostion[0])
        agent.setCurrentLocationY(targetPostion[1])

    def _getPedestrianHeatMapByName(self, pedestrianHeatMapName: str) -> PedestrianHeapMap:
        for destination in self.destinations:
            if destination.getDestinationName() == pedestrianHeatMapName:
                return destination.getPedestrianHeatMap() if destination.getPedestrianHeatMap() != None else destination.generatePedestrianHeatMap()
        raise SimulationException(SimulationErrorCodes.PEDESTRIAN_HEAT_MAP_NOT_FOUND)

    def _getLowestFreePosition(self, agent: BaseAgent, pedestrianHeatMap: PedestrianHeapMap) -> Tuple[int, int]:
        reachableFields: Tuple[int, int, float] = self._getReachableFields(agent, pedestrianHeatMap)
        sorted(reachableFields, key=lambda x: reachableFields[2], reverse=True)
        for x, y, _ in reachableFields:
            if (self.grid.getTileStatus(x, y) == TileStatus.FREE):
                return (x, y)
        return (agent.getCurrentLocationX(), agent.getCurrentLocationY())

    def _getReachableFields(self, agent: BaseAgent, pedestrianHeatMap: PedestrianHeapMap) -> Tuple[int, int, float]:
        returnList: Tuple[int, int, float] = []
        for x in range(agent.getCurrentLocationX() - 1, agent.getCurrentLocationX() + 2):
            for y in range(agent.getCurrentLocationY() - 1, agent.getCurrentLocationY() + 2):
                if (pedestrianHeatMap.isOnHeatMap(x, y)):
                    returnList.append((x, y, pedestrianHeatMap.getValue(x, y)))
        return returnList

    def _saveStep(self) -> None:
        self.tilesOverTime.append(self.grid.getTilesAsInteger())

    def __repr__(self) -> str:
        returnValue: str = "--- Base Simulation ---\n -- Grid --\n"
        returnValue += str(self.grid)
        returnValue += "\n -- Config --\n"
        returnValue += str(self.config)
        returnValue += "\n -- Spawners --\n"
        for spawner in self.spawners:
            returnValue += "---\n"
            returnValue += str(spawner)
        returnValue += "\n -- Destinations -- \n"
        for destination in self.destinations:
            returnValue += "---\n"
            returnValue += str(destination)
        return returnValue