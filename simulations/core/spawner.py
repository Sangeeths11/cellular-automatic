import random
from typing import Generator
from simulation.core.pedestrian import Pedestrian

from utils.clipped_normal_distribution import ClippedNormalDistribution

from typing import TYPE_CHECKING

from utils.immutable_list import ImmutableList

if TYPE_CHECKING:
    from simulation.core.cell import Cell
    from simulation.core.target import Target
    from simulation.heatmaps.distancing.base_distance import DistanceBase


class Spawner:
    # clipping is chosen at random
    # TODO: choose better value based on scientific research
    SPEED_DISTRIBUTION = ClippedNormalDistribution(1.34, 0.26, 0.1, 3.0)

    def __init__(self, name: str, distancing: 'DistanceBase', cells: list['Cell'], targets: list['Target'],
                 total_spawns: int | None, batch_size: int | None, spawn_delay: float, initial_delay: float):
        self._name: str = name
        self._cells: list['Cell'] = cells
        self._targets: list['Target'] = targets
        self._total_spawns: int | None = total_spawns
        self._batch_size: int | None = None if batch_size is None else min(batch_size,
                                                                           len(cells))  # can't spawn more pedestrians than there are cells in one batch
        self._spawn_delay: float = spawn_delay
        self._current_delay: float = initial_delay
        self._distancing: 'DistanceBase' = distancing

    def get_name(self) -> str:
        return self._name

    def get_cells(self) -> ImmutableList['Cell']:
        return ImmutableList(self._cells)

    def can_spawn(self) -> bool:
        return (self._total_spawns is None or self._total_spawns > 0) and self._current_delay <= 0

    def is_done(self) -> bool:
        return self._total_spawns == 0

    def update(self, delta: float) -> Generator[Pedestrian]:
        self._current_delay -= delta
        if self.can_spawn():
            self._current_delay = self._spawn_delay
            if self._total_spawns is not None:
                self._total_spawns -= 1
            yield from self.spawn()

    def spawn(self) -> Generator[Pedestrian]:
        free_cells = list([cell for cell in self._cells if cell.is_free()])
        random.shuffle(free_cells)
        for spawn_index in range(min(len(free_cells), self._batch_size)):
            cell = free_cells[spawn_index]
            target = random.choice(self._targets)
            speed = self.SPEED_DISTRIBUTION.sample()
            pedestrian = Pedestrian(cell.get_x(), cell.get_y(), speed, target, self._distancing)
            yield pedestrian
