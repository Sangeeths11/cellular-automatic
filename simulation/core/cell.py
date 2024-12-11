from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from simulation.core.cell_state import CellState
from simulation.core.position import Position

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation.core.pedestrian import Pedestrian

class Cell(Position):
    def __init__(self, x: int, y: int, initial_state: CellState = CellState.FREE):
        super().__init__(x, y)
        self._state: CellState = initial_state
        self._pedestrian: 'Pedestrian' | None = None

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._x, self._y))

    def get_state(self) -> CellState:
        return self._state

    def set_osbtacle(self) -> None:
        self._state = CellState.OBSTACLE

    def set_pedestrian(self, pedestrian: 'Pedestrian') -> None:
        if self._state == CellState.OBSTACLE:
            raise SimulationError(SimulationErrorCode.CELL_BLOCKED)

        if self._state == CellState.OCCUPIED:
            raise SimulationError(SimulationErrorCode.CELL_OCCUPIED, {"pedestrian": pedestrian})

        self._pedestrian = pedestrian
        self._state = CellState.OCCUPIED

    def remove_pedestrian(self) -> None:
        if self._state != CellState.OCCUPIED:
            raise SimulationError(SimulationErrorCode.CELL_NOT_OCCUPIED, {"x": self._x, "y": self._y})

        self._pedestrian = None
        self._state = CellState.FREE

    def is_free(self):
        return self._state == CellState.FREE

    def get_pedestrian(self) -> 'Pedestrian':
        return self._pedestrian

    def is_occupied(self):
        return self._state == CellState.OCCUPIED

    def is_obstacle(self):
        return self._state == CellState.OBSTACLE