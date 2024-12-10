import unittest
from unittest.mock import Mock
from simulation.core.simulation_grid import SimulationGrid
from simulation.core.cell import Cell
from simulation.core.position import Position
from simulation.neighbourhood.base_neighbourhood import NeighbourhoodBase
from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode

class MockNeighbourhood(NeighbourhoodBase):
    def get_neighbours(self, x, y, width=1, height=1):
        # Return a fixed set of neighbour coordinates for testing
        neighbours = []
        if x > 0:
            neighbours.append((x - 1, y))
        if x < self._width - 1:
            neighbours.append((x + 1, y))
        if y > 0:
            neighbours.append((x, y - 1))
        if y < self._height - 1:
            neighbours.append((x, y + 1))
        return neighbours

class TestSimulationGrid(unittest.TestCase):
    def setUp(self):
        self.width = 5
        self.height = 5
        self.grid = SimulationGrid(self.width, self.height, MockNeighbourhood)

    def test_initialization(self):
        """Tests grid initialization."""
        self.assertEqual(self.grid.get_width(), self.width)
        self.assertEqual(self.grid.get_height(), self.height)
        cells = self.grid.get_cells()
        self.assertEqual(len(cells), self.width * self.height)
        for cell in cells:
            self.assertIsInstance(cell, Cell)

    def test_get_cell_valid(self):
        """Tests get_cell with valid coordinates."""
        cell = self.grid.get_cell(2, 2)
        self.assertEqual(cell.get_x(), 2)
        self.assertEqual(cell.get_y(), 2)

    def test_get_cell_invalid(self):
        """Tests get_cell with invalid coordinates."""
        with self.assertRaises(SimulationError) as context:
            self.grid.get_cell(-1, 0)
        self.assertEqual(context.exception.get_code(), SimulationErrorCode.INVALID_COORDINATES.value[0])

    def test_get_cell_at_pos_valid(self):
        """Tests get_cell_at_pos with a valid position."""
        pos = Position(1, 1)
        cell = self.grid.get_cell_at_pos(pos)
        self.assertEqual(cell.get_x(), 1)
        self.assertEqual(cell.get_y(), 1)

    def test_get_cell_at_pos_invalid(self):
        """Tests get_cell_at_pos with an invalid position."""
        pos = Position(5, 5)
        with self.assertRaises(SimulationError) as context:
            self.grid.get_cell_at_pos(pos)
        self.assertEqual(context.exception.get_code(), SimulationErrorCode.INVALID_COORDINATES.value[0])

    def test_get_neighbours(self):
        """Tests get_neighbours method."""
        neighbours = list(self.grid.get_neighbours(2, 2))
        expected_positions = [(1, 2), (3, 2), (2, 1), (2, 3)]
        self.assertEqual(len(neighbours), len(expected_positions))
        for neighbour in neighbours:
            self.assertIsInstance(neighbour, Cell)
            self.assertIn((neighbour.get_x(), neighbour.get_y()), expected_positions)

    def test_get_neighbours_at(self):
        """Tests get_neighbours_at method."""
        pos = Position(2, 2)
        neighbours = list(self.grid.get_neighbours_at(pos))
        expected_positions = [(1, 2), (3, 2), (2, 1), (2, 3)]
        self.assertEqual(len(neighbours), len(expected_positions))
        for neighbour in neighbours:
            self.assertIsInstance(neighbour, Cell)
            self.assertIn((neighbour.get_x(), neighbour.get_y()), expected_positions)

if __name__ == '__main__':
    unittest.main()