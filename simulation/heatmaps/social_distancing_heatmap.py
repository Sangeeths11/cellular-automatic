import math
from typing import Generator, Iterable

from simulation.core.cell import Cell
from simulation.core.cell_state import CellState
from simulation.core.grid_base import GridBase
from simulation.core.pedestrian import Pedestrian
from simulation.core.position import Position
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.heatmap_generator_base import HeatmapGeneratorBase


class SocialDistancingHeatmapGenerator(HeatmapGeneratorBase):
    """
    Heatmap generator which adds a social distancing force from each occupied cell
    """

    def __init__(self, distancing: DistanceBase, width: float, height: float, blocked: set[CellState] = None):
        """
        :param distancing: algorithm for calculating distance between cells
        :param width: width of the social distancing force
        :param height: height of the social distancing force
        :param blocked: set of CellStates that are considered blocked, default is {CellState.OCCUPIED}
        """
        super().__init__()
        self._distancing = distancing
        self._width = width
        self._height = height
        self._neighbour_width = math.ceil(width / 2)
        self._neighbour_height = math.ceil(height / 2)
        self._blocked = {CellState.OCCUPIED}

    def get_bias(self, center: Position, neighbour: Position):
        return self.calculate_value(self._distancing.calculate_distance(center, neighbour))

    def get_max_value(self):
        return self.calculate_value(self._width - 0.01)

    def calculate_value(self, distance: float):
        if abs(distance) < self._width:
            return self._height * math.exp(1/(math.pow(distance/self._width, 2) - 1))
        else:
            return 0

    def generate_heatmap(self, target: Iterable[Cell], grid: SimulationGrid) -> Heatmap:
        """
        :param target: a list of cells which should be used to generate repulsive force, only cells with state in blocked are considered
        :param grid: the simulation grid the heatmap should be generated for
        :return: a heatmap where each obstacle creates a repulsive force
        """
        heatmap = Heatmap(grid.get_width(), grid.get_height(), 0.0)
        for cell in target:
            if cell.get_state() in self._blocked:
                heatmap.set_cell_at_pos(cell, Heatmap.INFINITY)
                for neighbour in grid.get_neighbours_at(cell, self._neighbour_width, self._neighbour_height):
                    current_value = heatmap.get_cell_at_pos(neighbour)
                    if current_value is not Heatmap.INFINITY :
                        value = self.calculate_value(self._distancing.calculate_distance(cell, neighbour))
                        heatmap.set_cell_at_pos(neighbour, current_value + value)

        return heatmap