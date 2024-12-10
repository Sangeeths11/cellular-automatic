import unittest
from unittest.mock import Mock
from simulation.core.cell import Cell
from simulation.core.cell_state import CellState
from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode

class TestCell(unittest.TestCase):
    def setUp(self):
        self.cell = Cell(1, 2)

    def test_initialization(self):
        """Tests the initialization of the cell with the default state."""
        self.assertEqual(self.cell.get_state(), CellState.FREE)
        self.assertIsNone(self.cell.get_pedestrian())

    def test_set_obstacle(self):
        """Tests setting the cell to OBSTACLE."""
        self.cell.set_osbtacle()
        self.assertEqual(self.cell.get_state(), CellState.OBSTACLE)

    def test_set_pedestrian_success(self):
        """Tests successfully placing a pedestrian in a free cell."""
        pedestrian = Mock()
        self.cell.set_pedestrian(pedestrian)
        self.assertEqual(self.cell.get_state(), CellState.OCCUPIED)
        self.assertEqual(self.cell.get_pedestrian(), pedestrian)

    def test_set_pedestrian_obstacle(self):
        """Tests that placing a pedestrian in an obstacle cell raises an exception."""
        self.cell.set_osbtacle()
        pedestrian = Mock()
        with self.assertRaises(SimulationError) as context:
            self.cell.set_pedestrian(pedestrian)
        self.assertEqual(context.exception.get_code(), SimulationErrorCode.CELL_BLOCKED)

    def test_eq_method(self):
        """Tests the equality method of the cell."""
        other_cell = Cell(1, 2)
        different_cell = Cell(2, 3)
        self.assertEqual(self.cell, other_cell)
        self.assertNotEqual(self.cell, different_cell)

    def test_hash_method(self):
        """Tests the hash method of the cell."""
        cell_set = {self.cell, Cell(1, 2), Cell(2, 3)}
        self.assertIn(Cell(1, 2), cell_set)
        self.assertIn(Cell(2, 3), cell_set)
        self.assertEqual(len(cell_set), 2)

    def test_remove_pedestrian_success(self):
        """Tests successfully removing a pedestrian from an occupied cell."""
        pedestrian = Mock()
        self.cell.set_pedestrian(pedestrian)
        self.cell.remove_pedestrian()
        self.assertEqual(self.cell.get_state(), CellState.FREE)
        self.assertIsNone(self.cell.get_pedestrian())

    def test_remove_pedestrian_not_occupied(self):
        """Tests that removing a pedestrian from a free cell raises an exception."""
        with self.assertRaises(SimulationError) as context:
            self.cell.remove_pedestrian()
        self.assertEqual(context.exception.get_code(), SimulationErrorCode.CELL_NOT_OCCUPIED)

    def test_is_free(self):
        """Tests the is_free method."""
        self.assertTrue(self.cell.is_free())
        pedestrian = Mock()
        self.cell.set_pedestrian(pedestrian)
        self.assertFalse(self.cell.is_free())

    def test_is_occupied(self):
        """Tests the is_occupied method."""
        self.assertFalse(self.cell.is_occupied())
        pedestrian = Mock()
        self.cell.set_pedestrian(pedestrian)
        self.assertTrue(self.cell.is_occupied())

    def test_get_pedestrian(self):
        """Tests the get_pedestrian method."""
        self.assertIsNone(self.cell.get_pedestrian())
        pedestrian = Mock()
        self.cell.set_pedestrian(pedestrian)
        self.assertEqual(self.cell.get_pedestrian(), pedestrian)

if __name__ == '__main__':
    unittest.main()
