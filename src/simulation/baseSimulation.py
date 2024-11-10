from src.exceptions.simulationErrorCodes import SimulationErrorCodes
from src.exceptions.simulationException import SimulationException
from src.config.config import _Config

class BaseSimulation():

    def __init__(self, grid, config: _Config):
        self.grid = grid
        self.config = config
        self.tilesOverTime = []

    def simulateStep(self):
        raise SimulationException(SimulationErrorCodes.NOT_IMPLEMENTED_IN_SIMULATION)

    def getTilesOverTime(self) -> dict:
        return self.tilesOverTime

