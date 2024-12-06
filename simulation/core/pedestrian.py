from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from simulation.core.cell_state import CellState
from simulation.core.position import Position
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.core.cell import Cell
    from simulation.core.target import Target
    from simulation.heatmaps.heatmap import Heatmap
    from simulation.heatmaps.distancing.base_distance import DistanceBase

class Pedestrian(Position):
    NEGATIVE_INFINITY = float('-inf')
    INFINITY = float('inf')
    ID_COUNTER = 0

    @staticmethod
    def get_next_id() -> int:
        Pedestrian.ID_COUNTER += 1
        return Pedestrian.ID_COUNTER

    def __init__(self, x: int, y: int, speed: float, target: 'Target', distancing: 'DistanceBase'):
        super().__init__(x, y)
        self._id: int = Pedestrian.get_next_id()
        self._optimal_speed: float = speed
        self._current_speed: float = speed
        self._target: 'Target' = target
        self._current_distance: float = Pedestrian.INFINITY
        self._distance_to_target: float = Pedestrian.INFINITY
        self._distancing: 'DistanceBase' = distancing
        self._target_cell: 'Cell' | None = None
        self._time_alive: float = 0
        self._total_distance_moved: float = 0

    def set_target_cell(self, target_cell: 'Cell') -> None:
        if target_cell is None:
            self._target_cell = None
            self._current_distance = Pedestrian.NEGATIVE_INFINITY
        else:
            if target_cell.get_position() == self.get_position():
                raise SimulationError(SimulationErrorCode.ALREADY_IN_CELL, {"cell": target_cell})

            self._current_distance = self._distancing.calculate_distance(self, target_cell)
            self._distance_to_target = self._current_distance
            self._target_cell = target_cell

    def get_id(self) -> int:
        return self._id

    def is_inside_target(self) -> bool:
        return self._target.is_inside_target(self)

    def get_targeted_cell(self) -> 'Cell':
        return self._target_cell

    def can_move(self) -> bool:
        return self._current_distance < 0 and self.has_targeted_cell() and self._target_cell.is_free()

    def move(self) -> None:
        if not self.can_move():
            raise SimulationError(SimulationErrorCode.CANNOT_MOVE)

        self._target_cell.set_pedestrian(self)
        self._x = self._target_cell.get_x()
        self._y = self._target_cell.get_y()
        self._total_distance_moved += self._distance_to_target
        self.set_target_cell(None)
        self._distance_to_target = Pedestrian.INFINITY

    def get_occupation_bias(self) -> float:
        if self._target_cell is None:
            return 1
        else:
            return 1.0 - (max(0.0, self._current_distance)/self._distance_to_target)

    def get_average_speed(self) -> float:
        return self._total_distance_moved / self._time_alive

    def update(self, delta: float):
        self._time_alive += delta
        self._current_distance -= self._current_speed * delta

    def get_current_distance(self) -> float:
        return self._current_distance

    def get_optimal_speed(self) -> float:
        return self._optimal_speed

    def get_target(self) -> 'Target':
        return self._target

    def get_heatmap(self) -> 'Heatmap':
        return self._target.get_heatmap()

    def has_targeted_cell(self):
        return self._target_cell is not None
