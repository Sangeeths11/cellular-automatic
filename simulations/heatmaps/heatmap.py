from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from simulation.core.grid_base import GridBase
from simulation.core.position import Position


class Heatmap(GridBase[float]):
    INFINITY = float("inf")

    def __init__(self, width: int, height: int, initial_value: float = INFINITY):
        self._initial_value = initial_value
        super().__init__(width, height)

    def _init_cell(self, x: int, y: int) -> float:
        return self._initial_value

    def set_cell(self, x: int, y: int, value: float) -> None:
        self.check_bounds(x, y)
        self.cells[self._get_cell_index(x, y)] = value

    def set_cell_at_pos(self, pos: Position, value: float) -> None:
        self.set_cell(pos.get_x(), pos.get_y(), value)