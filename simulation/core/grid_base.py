from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Sequence, Generator

from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from simulation.core.cell import Cell
from simulation.core.cell_state import CellState
from simulation.core.position import Position
from utils.immutable_list import ImmutableList


class GridBase[T](ABC):
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self.cells: list[T] = [self._init_cell(*self._get_cell_coordinate(i)) for i in range(width * height)]

    @abstractmethod
    def _init_cell(self, x: int, y: int) -> T:
        pass

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_cells(self) -> ImmutableList[Cell]:
        return ImmutableList(self.cells)

    def _get_cell_index(self, x: int, y: int) -> int:
        return y * self._width + x

    def _get_cell_coordinate(self, index: int) -> tuple[int, int]:
        return index % self._width, index // self._width


    def is_in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self._width and 0 <= y < self._height

    """
    Raises a SimulationError if the given coordinates are out of bounds.
    """
    def check_bounds(self, x: int, y: int) -> None:
        if not self.is_in_bounds(x, y):
            raise SimulationError(SimulationErrorCode.INVALID_COORDINATES, {"x": x, "y": y})

    def get_cell(self, x: int, y: int) -> T:
        self.check_bounds(x, y)
        return self.cells[self._get_cell_index(x, y)]

    def get_cell_at_pos(self, pos: Position):
        return self.get_cell(pos.get_x(), pos.get_y())

    def __contains__(self, item):
        if isinstance(item, Cell):
            return item in self.cells
        elif isinstance(item, Position):
            return self.is_in_bounds(item.get_x(), item.get_y())
        elif isinstance(item, tuple) and len(item) == 2:
            return self.is_in_bounds(*item)
        else:
            return False