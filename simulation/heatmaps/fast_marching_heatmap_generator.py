import math
from typing import Iterable, Generator

from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from simulation.core.cell import Cell
from simulation.core.cell_state import CellState
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.heatmap_generator_base import HeatmapGeneratorBase
from simulation.heatmaps.pathfinding_queue import PathfindingQueue
from simulation.neighbourhood.base_neighbourhood import NeighbourhoodBase
from simulation.neighbourhood.neumann_neighbourhood import NeumannNeighbourhood

class FastMarchingHeatmapGenerator(HeatmapGeneratorBase):
    """
    Heatmap generator using the Fast Marching Method
    """
    def __init__(self, distancing: DistanceBase, delta_x: float = 1.0, blocked=None):
        """
        :param distancing: algorithm for calculating distance between cells
        :param delta_x: distance between cells
        :param blocked: set of CellStates that are considered blocked, default is {CellState.OBSTACLE}
        """
        super().__init__()
        if blocked is None:
            blocked = {CellState.OBSTACLE}
        self._narrowband = NeumannNeighbourhood(1, 1)
        self._distancing = distancing
        self._delta_x = delta_x
        self._blocked = blocked if blocked is not None else {CellState.OBSTACLE}

    def _get_narrow_band(self, cell: Cell, grid: SimulationGrid) -> Generator[Cell]:
        for x, y in self._narrowband.get_neighbours(cell.get_x(), cell.get_y(), 1, 1):
            if grid.is_in_bounds(x, y):
                yield grid.get_cell(x, y)


    def _get_fixed_neighbours(self, cell: Cell, fixed: set[Cell], grid: SimulationGrid) -> Generator[Cell]:
        narrow_band = self._get_narrow_band(cell, grid)
        for neighbour in narrow_band:
            if neighbour in fixed and neighbour.get_state() != CellState.OBSTACLE:
                yield neighbour


    def _are_opposite(self, a: Cell, b: Cell) -> bool:
        return a.get_x() == b.get_x() or a.get_y() == b.get_y()

    def _calculate_travel_time(self, cell: Cell, heatmap: Heatmap, fixed: set[Cell], grid: SimulationGrid) -> float:
        fixed_neighbours = list(self._get_fixed_neighbours(cell, fixed, grid))
        if len(fixed_neighbours) == 0:
            raise SimulationError(SimulationErrorCode.NO_FIXED_NEIGHBOURS, {"cell": cell})
        elif len(fixed_neighbours) == 1:
            return heatmap.get_cell_at_pos(fixed_neighbours[0]) + self._distancing.calculate_distance(cell, fixed_neighbours[0])
        elif len(fixed_neighbours) == 2:
            a = heatmap.get_cell_at_pos(fixed_neighbours[0])
            b = heatmap.get_cell_at_pos(fixed_neighbours[1])
            return (a + b + math.sqrt(2 * self._delta_x**2 - ((a - b) ** 2))) / 2
        elif len(fixed_neighbours) == 3:
            single = fixed_neighbours[0] if self._are_opposite(fixed_neighbours[1], fixed_neighbours[2]) else fixed_neighbours[1] if self._are_opposite(fixed_neighbours[0], fixed_neighbours[2]) else fixed_neighbours[2]
            others = [heatmap.get_cell_at_pos(neighbour) for neighbour in fixed_neighbours if neighbour != single]
            a = heatmap.get_cell_at_pos(single)
            b = min(others[0], others[1])
            return (a + b + math.sqrt(2 * self._delta_x**2 - ((a - b) ** 2))) / 2



    def generate_heatmap(self, target: Iterable[Cell], grid: SimulationGrid) -> Heatmap:
        heatmap: Heatmap = Heatmap(grid.get_width(), grid.get_height())
        visited: PathfindingQueue[Cell] = PathfindingQueue()
        fixed: set[Cell] = set()

        for cell in target:
            visited.push(cell, 0)
            heatmap.set_cell(cell.get_x(), cell.get_y(), 0)

        while not visited.is_empty():
            current = visited.pop()
            if current in fixed:
                continue

            fixed.add(current)
            narrowband = self._get_narrow_band(current, grid)
            for neighbour in narrowband:
                if neighbour in fixed:
                    continue

                if  neighbour.get_state() in self._blocked:
                    heatmap.set_cell(neighbour.get_x(), neighbour.get_y(), Heatmap.INFINITY)
                    visited.mark_visited(neighbour)
                else:
                    travel_time = self._calculate_travel_time(neighbour, heatmap, fixed, grid)
                    heatmap.set_cell(neighbour.get_x(), neighbour.get_y(), travel_time)
                    visited.push(neighbour, travel_time)



        return heatmap