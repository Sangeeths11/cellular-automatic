from src.exceptions.simulationErrorCodes import SimulationErrorCodes
from src.exceptions.simulationException import SimulationException
from src.simulation.spawner.spawnerConfiguration import SpawnerConfiguration
from src.simulation.spawner.baseSpawner import BaseSpawner
from src.simulation.grid import Grid
from src.simulation.tile import Tile
from src.dtoModule.tileDTO import TileDTO
from src.config.config import _Config
from typing import List

class BaseSimulation():

    def __init__(self, grid: Grid, config: _Config) -> None:
        self.grid: Grid = grid
        self.config: _Config = config
        self.tilesOverTime: List[TileDTO] = []
        self.spawners: List[BaseSpawner] = []

    def simulateStep(self) -> None:
        self._spawn()
        self._step()
        self._saveStep()
    
    def setSpawner(self, spawnerConfiguration: SpawnerConfiguration):
        spawnerTiles: List[Tile] = []
        for x, y in spawnerConfiguration.getSpawnerTilesCoordinates():
            spawnerTiles.append(self.grid.getTile(x, y))
        baseSpawner: BaseSpawner = BaseSpawner(spawnerTiles, **spawnerConfiguration.getArgs())
        self.spawners.append(baseSpawner)

    def getTilesOverTime(self) -> dict:
        return self.tilesOverTime
    
    def _spawn(self) -> None:
        for spawner in self.spawners:
            spawner.update()

    def _step(self) -> None:
        pass

    def _saveStep(self) -> None:
        pass

    def __repr__(self) -> str:
        returnValue: str = "--- Base Simulation ---\n -- Grid --\n"
        returnValue += str(self.grid)
        returnValue += "\n -- Config --\n"
        returnValue += str(self.config)
        returnValue += "\n -- Spawners --\n"
        for spawner in self.spawners:
            returnValue += "---\n"
            returnValue += str(spawner)
        return returnValue