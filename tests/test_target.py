import unittest
from unittest.mock import Mock
from simulation.core.target import Target
from simulation.core.cell import Cell
from simulation.core.position import Position
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.heatmap_generator_base import HeatmapGeneratorBase
from simulation.heatmaps.heatmap import Heatmap
from utils.immutable_list import ImmutableList

class TestTarget(unittest.TestCase):
    def setUp(self):
        self.name = "TestTarget"
        self.cells = [Mock(spec=Cell) for _ in range(3)]
        self.grid = Mock(spec=SimulationGrid)
        self.heatmap_generator = Mock(spec=HeatmapGeneratorBase)
        self.heatmap = Mock(spec=Heatmap)

        self.heatmap_generator.generate_heatmap.return_value = self.heatmap

        self.target = Target(
            name=self.name,
            cells=self.cells,
            grid=self.grid,
            heatmap_generator=self.heatmap_generator
        )

    def test_initialization(self):
        """Tests the initialization of the Target."""
        self.assertEqual(self.target.get_name(), self.name)
        self.assertEqual(list(self.target.get_cells()), self.cells)
        self.assertEqual(self.target._grid, self.grid)
        self.assertEqual(self.target._heatmap_generator, self.heatmap_generator)
        self.assertIsNone(self.target._heatmap)
        self.assertEqual(self.target._exit_count, 0)
    
    def test_get_name(self):
        """Tests the get_name method."""
        self.assertEqual(self.target.get_name(), self.name)
    
    def test_get_cells(self):
        """Tests the get_cells method."""
        cells = self.target.get_cells()
        self.assertIsInstance(cells, ImmutableList)
        self.assertEqual(list(cells), self.cells)
    
    def test_generate_heatmap(self):
        """Tests the generate_heatmap method."""
        self.target.update_heatmap()
        self.heatmap_generator.generate_heatmap.assert_called_once_with(self.cells, self.grid)
        self.assertEqual(self.target.get_heatmap(), self.heatmap)
    
    def test_get_heatmap_without_generation(self):
        """Tests get_heatmap method before heatmap is generated."""
        with self.assertRaises(Exception):
            self.target.get_heatmap()
    
    def test_is_inside_target(self):
        """Tests the is_inside_target method."""
        positions = [Position(x, y) for x, y in [(1, 1), (2, 2), (3, 3)]]
        for cell, pos in zip(self.cells, positions):
            cell.get_position.return_value = pos

        position_inside = positions[0]
        position_outside = Position(4, 4)

        self.assertTrue(self.target.is_inside_target(position_inside))
        self.assertFalse(self.target.is_inside_target(position_outside))
    
    def test_get_exit_count(self):
        """Tests the get_exit_count method."""
        self.assertEqual(self.target.get_exit_count(), 0)
        self.target._exit_count = 5
        self.assertEqual(self.target.get_exit_count(), 5)
    
    def test_increment_exit_count(self):
        """Tests the increment_exit_count method."""
        self.assertEqual(self.target.get_exit_count(), 0)
        self.target.increment_exit_count()
        self.assertEqual(self.target.get_exit_count(), 1)
        self.target.increment_exit_count()
        self.assertEqual(self.target.get_exit_count(), 2)

if __name__ == '__main__':
    unittest.main()