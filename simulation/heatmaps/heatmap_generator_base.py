from abc import ABC, abstractmethod
from typing import Iterable

from simulation.core.cell import Cell
from simulation.core.cell_state import CellState
from simulation.core.grid_base import GridBase
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.heatmap import Heatmap


class HeatmapGeneratorBase(ABC):
    """
    Base class for heatmap generators. Heatmap generators generate heatmaps based on the given target and grid
    """

    def __init__(self, blocked: set[CellState] ):
        self._blocked: set[CellState]  = blocked
        pass


    @abstractmethod
    def generate_heatmap(self, target: Iterable[Cell], grid: SimulationGrid) -> Heatmap:
        """
        Generates heatmap based on the given target and grid
        :param target: target cells off the heatmap
        :param grid: the simulation grid the heatmap should be generated for
        :return: a heatmap where each cell is assigned a distance to the closest target cell
        """
        pass

    def get_blocked(self) -> set[CellState]:
        return self._blocked