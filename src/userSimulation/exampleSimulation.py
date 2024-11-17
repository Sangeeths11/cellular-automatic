from src.simulation.baseSimulation import BaseSimulation
from src.config.config import ConfigBuilder
from src.simulation.spawner.spawnerConfiguration import SpawnerConfiguration
from src.simulation.grid import Grid
import os

def run():
    configBuilder = ConfigBuilder()
    config = configBuilder.build()
    grid = Grid(10, 10)
    baseSimulation: BaseSimulation = BaseSimulation(grid=grid, config=config)
    spawnerTilesCoordinates = [(0, 0), (0, 1), (1, 0), (1, 1)]
    spawnerConfiguration = SpawnerConfiguration(spawnerTilesCoordinates, 12, 4)
    baseSimulation.setSpawner(spawnerConfiguration)
    print(baseSimulation)
    baseSimulation.simulateStep()
    print(baseSimulation)
