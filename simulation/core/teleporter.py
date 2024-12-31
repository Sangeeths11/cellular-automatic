import random
from typing import Generator
from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from simulation.core.pedestrian import Pedestrian

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.core.cell import Cell
    from simulation.core.target import Target
    from simulation.core.spawner import Spawner
    from simulation.heatmaps.distancing.base_distance import DistanceBase

class Teleporter():

    def __init__(self, cells: list['Cell']) -> None:
        self._cells: list['Cell'] = cells

    def has_free_cell(self) -> bool:
        for cell in self._cells:
            if (cell.is_free()):
                return True
        return False
    
    def spawn(self, speed, spawner: 'Spawner', target: 'Target', distancing: 'DistanceBase', time_alive: float) -> Pedestrian:
        free_cells = list([cell for cell in self._cells if cell.is_free()])
        random.shuffle(free_cells)
        if len(free_cells) < 1:
            raise SimulationError(SimulationErrorCode.TELEPORTER_FULL)
        cell = free_cells[0]
        pedestrian = Pedestrian(cell.get_x(), cell.get_y(), speed, spawner, target, distancing, time_alive)
        return pedestrian