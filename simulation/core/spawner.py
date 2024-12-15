import random
from typing import Generator

from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from serialization.serializable import Serializable
from simulation.core.pedestrian import Pedestrian
from simulation.core.targeting_stratey import TargetingStrategy

from utils.clipped_normal_distribution import ClippedNormalDistribution

from typing import TYPE_CHECKING

from utils.immutable_list import ImmutableList

if TYPE_CHECKING:
    from simulation.core.cell import Cell
    from simulation.core.target import Target
    from simulation.heatmaps.distancing.base_distance import DistanceBase


class Spawner(Serializable):
    # clipping is chosen at random
    # TODO: choose better value based on scientific research
    SPEED_DISTRIBUTION = ClippedNormalDistribution(1.34, 0.26, 0.1, 3.0)

    def __init__(self, name: str, distancing: 'DistanceBase', cells: list['Cell'], targets: list['Target'], total_spawns: int | None, batch_size: int | None, spawn_delay: float, initial_delay: float, targeting_strategy: TargetingStrategy = TargetingStrategy.RANDOM):
        self._name: str = name
        self._cells: list['Cell'] = cells
        self._targets: list['Target'] = targets
        self._total_spawns: int | None = total_spawns
        self._batch_size: int | None = None if batch_size is None else min(batch_size, len(cells))  # can't spawn more pedestrians than there are cells in one batch
        self._spawn_delay: float = spawn_delay
        self._current_delay: float = initial_delay
        self._distancing: 'DistanceBase' = distancing
        self._targeting_strategy: TargetingStrategy = targeting_strategy

    def get_name(self) -> str:
        return self._name

    def get_cells(self) -> ImmutableList['Cell']:
        return ImmutableList(self._cells)

    def can_spawn(self) -> bool:
        return (self._total_spawns is None or self._total_spawns > 0) and self._current_delay <= 0

    def is_done(self) -> bool:
        return self._total_spawns == 0

    def update(self, delta: float) -> Generator[Pedestrian]:
        if not self.is_done():
            self._current_delay -= delta
            if self.can_spawn():
                self._current_delay = self._spawn_delay
                yield from self.spawn()

    def decrement_total_spawns(self) -> bool:
        if self._total_spawns is not None:
            if self._total_spawns > 0:
                self._total_spawns -= 1
                return True
            else:
                return False

        return True

    def _get_target(self, cell) -> 'Target':
        if self._targeting_strategy == TargetingStrategy.RANDOM:
            return random.choice(self._targets)
        elif self._targeting_strategy == TargetingStrategy.CLOSEST:
            return min(self._targets, key=lambda target: min(self._distancing.calculate_distance(cell, x) for x in target.get_cells()))
        elif self._targeting_strategy == TargetingStrategy.FARTHEST:
            return max(self._targets, key=lambda target: max(self._distancing.calculate_distance(cell, x) for x in target.get_cells()))
        else:
            raise SimulationError(SimulationErrorCode.NOT_IMPLEMENTED_IN_SIMULATION, {"targeting-strategy": self._targeting_strategy})

    def spawn(self) -> Generator[Pedestrian]:
        free_cells = list([cell for cell in self._cells if cell.is_free()])
        random.shuffle(free_cells)
        for spawn_index in range(min(len(free_cells), self._batch_size)):
            if self.decrement_total_spawns() is False:
                break

            cell = free_cells[spawn_index]
            target = self._get_target(cell)
            speed = self.SPEED_DISTRIBUTION.sample()
            pedestrian = Pedestrian(cell.get_x(), cell.get_y(), speed, self, target, self._distancing)
            yield pedestrian

    def get_serialization_data(self) -> dict[str, any]:
        return {
            "id": self.get_identifier(),
            "total_spawns": self._total_spawns,
            "current_delay": self._current_delay
        }

    def get_identifier(self) -> str:
        return self._name