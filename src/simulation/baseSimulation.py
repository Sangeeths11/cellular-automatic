from src.exceptions.simulationErrorCodes import SimulationErrorCodes
from src.exceptions.simulationException import SimulationException

class BaseSimulation():

    def __init__(self, grid):
        self.grid = grid
        self.tilesOverTime = []

    def simulateStep(self):
        raise SimulationException(SimulationErrorCodes.NOT_IMPLEMENTED_IN_SIMULATION)

    def getTilesOverTime(self) -> dict:
        return self.tilesOverTime

