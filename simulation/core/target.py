from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from simulation.core.cell_state import CellState
from simulation.core.position import Position



from typing import TYPE_CHECKING

from utils.immutable_list import ImmutableList

if TYPE_CHECKING:
    from simulation.core.simulation_grid import SimulationGrid
    from simulation.core.cell import Cell
    from simulation.heatmaps.heatmap import Heatmap
    from simulation.heatmaps.heatmap_generator_base import HeatmapGeneratorBase

class Target:
    def __init__(self, name: str, cells: 'list[Cell]', grid: 'SimulationGrid', heatmap_generator: 'HeatmapGeneratorBase'):
        self._name: str = name
        self._cells: 'list[Cell]' = cells
        self._heatmap_generator: 'HeatmapGeneratorBase' = heatmap_generator
        self._grid: 'SimulationGrid' = grid
        self._heatmap: 'Heatmap'|None = None
        self._exit_count: int = 0
        self._is_static_heatmap: bool = CellState.OCCUPIED not in heatmap_generator.get_blocked()

    def get_name(self) -> str:
        return self._name

    def get_cells(self) -> ImmutableList['Cell']:
        return ImmutableList(self._cells)

    def get_heatmap(self) -> 'Heatmap':
        if self._heatmap is None:
            raise SimulationError(SimulationErrorCode.VALUE_NOT_INITIALIZED, {"value": "heatmap"})

        return self._heatmap

    def update_heatmap(self) -> None:
        if self._is_static_heatmap is False or self._heatmap is None:
            self._heatmap = self._heatmap_generator.generate_heatmap(self._cells, self._grid)

    def increment_exit_count(self) -> None:
        self._exit_count += 1

    def get_exit_count(self) -> int:
        return self._exit_count

    def is_coordinate_inside_target(self, x: int, y: int) -> bool:
        for cell in self._cells:
            if cell.get_x() == x and cell.get_y() == y:
                return True

    def is_inside_target(self, pos: Position) -> bool:
        for cell in self._cells:
            if pos.pos_equals(cell):
                return True

        return False