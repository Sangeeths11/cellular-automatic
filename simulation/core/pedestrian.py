from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from serialization.serializable import Serializable
from simulation.core.cell_state import CellState
from simulation.core.position import Position
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.core.cell import Cell
    from simulation.core.target import Target
    from simulation.core.spawner import Spawner
    from simulation.heatmaps.heatmap import Heatmap
    from simulation.heatmaps.distancing.base_distance import DistanceBase

class Pedestrian(Position, Serializable):
    NEGATIVE_INFINITY = float('-inf')
    INFINITY = float('inf')
    ID_COUNTER = 0

    @staticmethod
    def get_next_id() -> int:
        Pedestrian.ID_COUNTER += 1
        return Pedestrian.ID_COUNTER

    def __init__(self, x: int, y: int, speed: float, spawner: 'Spawner', target: 'Target', distancing: 'DistanceBase'):
        super().__init__(x, y)
        self._id: int = Pedestrian.get_next_id()
        self._optimal_speed: float = speed
        self._current_speed: float = speed
        self._target: 'Target' = target
        self._spawner: 'Spawner' = spawner
        self._current_distance: float = Pedestrian.INFINITY
        self._distance_to_target: float = Pedestrian.INFINITY
        self._distancing: 'DistanceBase' = distancing
        self._target_cell: 'Cell' | None = None
        self._time_alive: float = 0
        self._total_distance_moved: float = 0
        self._refund_distance_flag = False
        self._reached_target = False

    def set_reached_target(self) -> None:
        self._reached_target = True

    def has_reached_target(self) -> bool:
        return self._reached_target

    def set_target_cell(self, target_cell: 'Cell') -> None:
        if target_cell is None:
            self._target_cell = None
            self._current_distance = Pedestrian.NEGATIVE_INFINITY
        else:
            if target_cell.pos_equals(self):
                raise SimulationError(SimulationErrorCode.ALREADY_IN_CELL, {"cell": target_cell})

            if self._refund_distance_flag and self._current_distance is not Pedestrian.NEGATIVE_INFINITY and self._current_distance is not Pedestrian.INFINITY:
                self._current_distance += self._distancing.calculate_distance(self, target_cell)
            else:
                self._current_distance = self._distancing.calculate_distance(self, target_cell)

            self._distance_to_target = self._current_distance
            self._target_cell = target_cell
            self._refund_distance_flag = True

    def get_spawner(self) -> 'Spawner':
        return self._spawner

    def get_id(self) -> int:
        return self._id

    def is_inside_target(self) -> bool:
        return self._target.is_inside_target(self)

    def get_targeted_cell(self) -> 'Cell':
        return self._target_cell

    def can_move(self) -> bool:
        return self._current_distance < 0 and self.has_targeted_cell() and self._target_cell.is_free() and not self.has_reached_target()

    def move(self) -> None:
        if not self.can_move() or self.has_reached_target():
            raise SimulationError(SimulationErrorCode.CANNOT_MOVE)

        # pedestrians shouldn't manipulate the themselves
        # self._target_cell.set_pedestrian(self)
        self._x = self._target_cell.get_x()
        self._y = self._target_cell.get_y()
        self._total_distance_moved += self._distance_to_target
        # self.set_target_cell(None)
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
        if self._current_distance < 0:
            self._refund_distance_flag = False

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

    def get_serialization_data(self) -> dict[str, any]:
        return {
            "id": self._id,
            "average_speed": self.get_average_speed(),
            "current_distance": self._current_distance,
            "time_alive": self._time_alive,
            "total_distance_moved": self._total_distance_moved,
            "optimal_speed": self._optimal_speed,
            "target": self._target.get_identifier(),
            "target_cell": self._target_cell.get_identifier() if self._target_cell is not None else None,
            "spawner": self._spawner.get_identifier(),
            "cell_id": f"{self._x}_{self._y}",
            "x": self._x,
            "y": self._y,
        }

    def get_identifier(self) -> str:
        return str(self._id)
