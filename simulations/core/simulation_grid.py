from typing import Type, Generator

from scipy.stats import wasserstein_distance

from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from simulation.core.cell import Cell
from simulation.core.cell_state import CellState
from simulation.core.grid_base import GridBase
from simulation.core.position import Position
from simulation.neighbourhood.base_neighbourhood import NeighbourhoodBase


class SimulationGrid(GridBase[Cell]):
    def __init__(self, width: int, height: int, neighbourhood: Type[NeighbourhoodBase]):
        super().__init__(width, height)
        self._neighbourhood: NeighbourhoodBase = neighbourhood(width, height)

    def _init_cell(self, x: int, y: int) -> Cell:
        return Cell(x, y)

    def get_neighbours(self, x: int, y: int, width: int = 1, height: int = 1) -> Generator[Cell]:
        for x, y in self._neighbourhood.get_neighbours(x, y, width, height):
            yield self.get_cell(x, y)

    def get_neighbours_at(self, pos: Position, width: int = 1, height: int = 1) -> Generator[Cell]:
        return self.get_neighbours(pos.get_x(), pos.get_y(), width, height)
