from src.enums.locomotionAlgorithms import LocomationAlgorihms
from src.simulation.baseSimulation import BaseSimulation
from src.config.config import ConfigBuilder
from src.simulation.destination.destinationConfiguration import DestinationConfiguration
from src.simulation.spawner.spawnerConfiguration import SpawnerConfiguration
from src.simulation.grid import Grid
from src.visualization import visualization
import os

def run():
    configBuilder = ConfigBuilder()
    config = configBuilder.build()
    grid = Grid(100, 100)
    baseSimulation: BaseSimulation = BaseSimulation(grid=grid, config=config)

    blocks = [(4,3),(5,3),(4,5),(5,4),(5,5),]
    baseSimulation.setBlockingCells(blocks)

    spawnerTilesCoordinates = [(0, 0), (0, 1), (1, 0), (1, 1)]
    spawnerConfiguration = SpawnerConfiguration(spawnerTilesCoordinates, 12, 4)
    baseSimulation.setSpawner(spawnerConfiguration)

    destinationCoordinates = [(9,9)]
    destinationName = "Final"
    locomotionAlgorithm = LocomationAlgorihms.dijksta
    destinationConfiguration = DestinationConfiguration(
        name=destinationName,
        destinationTilesCoordination=destinationCoordinates,
        locomotionAlgorithm=locomotionAlgorithm)
    baseSimulation.setDestination(destinationConfiguration)

    print(baseSimulation)
    baseSimulation.simulateStep()
    print(baseSimulation)