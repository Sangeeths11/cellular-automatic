from src.simulation.baseSimulation import BaseSimulation
from src.config.config import ConfigBuilder
from src.simulation.grid import Grid
import os

def run():
    configBuilder = ConfigBuilder()
    config = configBuilder.build()
    grid = Grid(10, 10)
    print(config)
    print(grid)
