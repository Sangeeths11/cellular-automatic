from simulation.core.cell_state import CellState
from simulation.core.position import Position
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.heatmap_generator_base import HeatmapGeneratorBase

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation.core.pedestrian import Pedestrian
    from simulation.core.cell import Cell

class Waypoint:
    def __init__(self, heatmap_generator: HeatmapGeneratorBase, grid: SimulationGrid, cell: 'Cell', pedestrian: 'Pedestrian'):
        self._heatmap_generator = heatmap_generator
        self._heatmap: Heatmap = None
        self._is_static_heatmap = CellState.OCCUPIED in heatmap_generator.get_blocked()
        self._grid: SimulationGrid = grid
        self._cell = cell
        self._pedestrian: 'Pedestrian' = pedestrian
        self.update()

    def get_pedestrian(self) -> 'Pedestrian':
        return self._pedestrian

    def get_heatmap(self) -> Heatmap:
        return self._heatmap

    def update(self):
        if not self._is_static_heatmap and self._heatmap is None:
            self._heatmap = self._heatmap_generator.generate_heatmap([self._cell], self._grid)

    def get_cell(self) -> 'Cell':
        return self._cell

    def next_cell(self, current: Position) -> 'Cell|None':
        for cell in sorted(self._grid.get_neighbours_at(current), key=lambda x: self._heatmap.get_cell_at_pos(x)):
            if cell.is_free():
                return cell

        return None

    def is_inside_waypoint(self, pos: Position):
        return self._cell.pos_equals(pos)