from src.enums.locomotionAlgorithms import LocomationAlgorihms
from src.simulation.baseSimulation import BaseSimulation
from src.config.config import ConfigBuilder
from src.simulation.destination.destinationConfiguration import DestinationConfiguration
from src.simulation.spawner.spawnerConfiguration import SpawnerConfiguration
from src.simulation.grid import Grid
import os

def run():
    configBuilder = ConfigBuilder()
    config = configBuilder.build()
    grid = Grid(10, 10)
    baseSimulation: BaseSimulation = BaseSimulation(grid=grid, config=config)

    blocks = [(4,3),(5,3),(4,5),(5,4),(5,5),]
    baseSimulation.setBlockingCells(blocks)

    spawnerTilesCoordinates = [(0, 0), (0, 1), (1, 0), (1, 1)]
    spawnerConfiguration = SpawnerConfiguration(spawnerTilesCoordinates, "Final", 4, 4)
    baseSimulation.setSpawner(spawnerConfiguration)

    destinationCoordinates = [(9,9), (9,8), (9,7), (0,5)]
    destinationName = "Final"
    locomotionAlgorithm = LocomationAlgorihms.dijksta
    destinationConfiguration = DestinationConfiguration(
        name=destinationName,
        destinationTilesCoordination=destinationCoordinates,
        locomotionAlgorithm=locomotionAlgorithm)
    baseSimulation.setDestination(destinationConfiguration)

    print(baseSimulation)
    baseSimulation.simulateStep()
    baseSimulation.simulateStep()
    baseSimulation.simulateStep()
    print(baseSimulation)
    tilesOverTime = baseSimulation.getTilesOverTime()
    for TileOverTime in tilesOverTime:
        print(TileOverTime)
    baseSimulation.save("exampleSimulation")