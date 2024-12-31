from typing import Iterable

from simulation.core.cell import Cell
from simulation.core.cell_state import CellState
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.heatmap_generator_base import HeatmapGeneratorBase
from simulation.heatmaps.distancing.base_distance import DistanceBase


class InfinityHeatmapGenerator(HeatmapGeneratorBase):
    def __init__(self, distancing: DistanceBase, blocked=None):
        """
        :param distancing: algorithm for calculating distance between cells
        :param delta_x: distance between cells
        :param blocked: set of CellStates that are considered blocked, default is {CellState.OBSTACLE}
        """
        super().__init__(blocked if blocked is not None else {CellState.OBSTACLE})
        self._distancing = distancing
        self._delta_x = distancing.get_scale()

    def generate_heatmap(self, target: Iterable[Cell], grid: SimulationGrid) -> Heatmap:
        heatmap = Heatmap(grid.get_width(), grid.get_height())
        for cell in grid.get_cells():
            heatmap.set_cell_at_pos(cell, Heatmap.INFINITY)

        return heatmap