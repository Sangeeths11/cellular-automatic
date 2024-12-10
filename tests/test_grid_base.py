import unittest
from typing import TypeVar
from abc import ABC

from simulation.core.grid_base import GridBase
from simulation.core.cell import Cell
from simulation.core.position import Position
from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode

T = TypeVar('T')

class MockGrid(GridBase[Cell], ABC):
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self.cells = [self._init_cell(x, y) for y in range(height) for x in range(width)]
    
    def _init_cell(self, x: int, y: int) -> Cell:
        return Cell(x, y)
    
    def _get_cell_index(self, x: int, y: int) -> int:
        return y * self._width + x

class TestGridBase(unittest.TestCase):
    def setUp(self):
        self.width = 5
        self.height = 5
        self.grid = MockGrid(self.width, self.height)
    
    def test_is_in_bounds_true(self):
        """Tests whether is_in_bounds returns True for coordinates within bounds."""
        self.assertTrue(self.grid.is_in_bounds(0, 0))
        self.assertTrue(self.grid.is_in_bounds(4, 4))
        self.assertTrue(self.grid.is_in_bounds(2, 3))
    
    def test_is_in_bounds_false(self):
        """Tests whether is_in_bounds returns False for coordinates outside the bounds."""
        self.assertFalse(self.grid.is_in_bounds(-1, 0))
        self.assertFalse(self.grid.is_in_bounds(0, -1))
        self.assertFalse(self.grid.is_in_bounds(5, 5))
        self.assertFalse(self.grid.is_in_bounds(6, 2))
    
    def test_check_bounds_inside(self):
        """Tests that check_bounds does not raise an exception for valid coordinates."""
        try:
            self.grid.check_bounds(2, 2)
        except SimulationError:
            self.fail("check_bounds raised a SimulationError for valid coordinates.")
    
    def test_check_bounds_outside(self):
        """Tests that check_bounds raises a SimulationError for invalid coordinates."""
        with self.assertRaises(SimulationError) as context:
            self.grid.check_bounds(5, 5)
        self.assertEqual(context.exception.get_code(), SimulationErrorCode.INVALID_COORDINATES)
        self.assertEqual(context.exception.details, {"x": 5, "y": 5})
    
    def test_get_cell_valid(self):
        """Tests whether get_cell returns the correct cell for valid coordinates."""
        cell = self.grid.get_cell(1, 1)
        self.assertIsInstance(cell, Cell)
        self.assertEqual(cell.get_x(), 1)
        self.assertEqual(cell.get_y(), 1)
    
    def test_get_cell_invalid(self):
        """Tests whether get_cell raises a SimulationError for invalid coordinates."""
        with self.assertRaises(SimulationError) as context:
            self.grid.get_cell(-1, 0)
        self.assertEqual(context.exception.get_code(), SimulationErrorCode.INVALID_COORDINATES)
    
    def test_get_cell_at_pos_valid(self):
        """Tests whether get_cell_at_pos returns the correct cell for a valid position."""
        pos = Position(3, 3)
        cell = self.grid.get_cell_at_pos(pos)
        self.assertIsInstance(cell, Cell)
        self.assertEqual(cell.get_x(), 3)
        self.assertEqual(cell.get_y(), 3)
    
    def test_get_cell_at_pos_invalid(self):
        """Tests whether get_cell_at_pos raises a SimulationError for an invalid position."""
        pos = Position(5, 5)
        with self.assertRaises(SimulationError) as context:
            self.grid.get_cell_at_pos(pos)
        self.assertEqual(context.exception.get_code(), SimulationErrorCode.INVALID_COORDINATES)
    
    def test_contains_with_cell(self):
        """Tests the __contains__ method with a Cell."""
        cell = self.grid.get_cell(2, 2)
        self.assertIn(cell, self.grid)
        other_cell = Cell(2, 2)
        self.assertIn(other_cell, self.grid)
        non_existent_cell = Cell(5, 5)
        self.assertNotIn(non_existent_cell, self.grid)
    
    def test_contains_with_position(self):
        """Tests the __contains__ method with a Position."""
        pos_inside = Position(1, 1)
        pos_outside = Position(5, 5)
        self.assertIn(pos_inside, self.grid)
        self.assertNotIn(pos_outside, self.grid)
    
    def test_contains_with_tuple(self):
        """Tests the __contains__ method with a tuple."""
        self.assertIn((0, 0), self.grid)
        self.assertIn((4, 4), self.grid)
        self.assertNotIn((5, 5), self.grid)
    
    def test_contains_with_invalid_type(self):
        """Tests the __contains__ method with an invalid type."""
        self.assertNotIn("invalid", self.grid)
        self.assertNotIn(123, self.grid)

if __name__ == '__main__':
    unittest.main()
