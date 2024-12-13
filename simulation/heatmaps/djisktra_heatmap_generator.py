import heapq
from typing import Iterable

from simulation.core.cell import Cell
from simulation.core.cell_state import CellState
from simulation.core.grid_base import GridBase
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.heatmap_generator_base import HeatmapGeneratorBase
from simulation.heatmaps.pathfinding_queue import PathfindingQueue


class DijkstraHeatmapGenerator(HeatmapGeneratorBase):
    """
    Heatmap generator using the Dijkstra algorithm
    """
    def __init__(self, distancing: DistanceBase, blocked: set[CellState] = None):
        """
        :param distancing: algorithm for calculating distance between cells
        :param blocked:  set of CellStates that are considered blocked, default is {CellState.OBSTACLE}
        """
        super().__init__(blocked or {CellState.OBSTACLE})
        self._distancing = distancing


    def generate_heatmap(self, target: Iterable[Cell], grid: SimulationGrid) -> Heatmap:
        heatmap = Heatmap(grid.get_width(), grid.get_height())
        visited: PathfindingQueue[Cell] = PathfindingQueue()

        for cell in target:
            heatmap.set_cell(cell.get_x(), cell.get_y(), 0)
            visited.push(cell, 0)

        for cell in grid.get_cells():
            if cell.get_state() in self._blocked:  # can't enter cells which aren't free
                heatmap.set_cell(cell.get_x(), cell.get_y(), Heatmap.INFINITY)
                visited.mark_visited(cell)

        while len(visited) > 0:
            current = visited.pop()
            current_distance = heatmap.get_cell_at_pos(current)
            neighbours = grid.get_neighbours_at(current, 1)
            for neighbour in neighbours:
                if neighbour not in visited:
                    distance = current_distance + self._distancing.calculate_distance(current, neighbour)
                    if heatmap.get_cell_at_pos(neighbour) > distance:
                        heatmap.set_cell(neighbour.get_x(), neighbour.get_y(), distance)
                        visited.push(neighbour, distance)

        return heatmap
