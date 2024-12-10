import unittest
from unittest.mock import Mock
from simulation.heatmaps.social_distancing_heatmap_generator import SocialDistancingHeatmapGenerator
from simulation.core.cell import Cell
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.core.cell_state import CellState

class TestSocialDistancingHeatmapGenerator(unittest.TestCase):
    def setUp(self):
        self.distancing = Mock(spec=DistanceBase)
        self.grid = Mock(spec=SimulationGrid)
        self.cells = [Mock(spec=Cell) for _ in range(3)]
        self.heatmap_generator = SocialDistancingHeatmapGenerator(self.distancing, width=3.0, height=3.0)

        for i, cell in enumerate(self.cells):
            cell.get_x.return_value = i
            cell.get_y.return_value = i
            cell.get_state.return_value = CellState.FREE

    def test_initialization(self):
        """Tests initialization of the SocialDistancingHeatmapGenerator."""
        self.assertEqual(self.heatmap_generator._distancing, self.distancing)
        self.assertEqual(self.heatmap_generator._width, 3.0)
        self.assertEqual(self.heatmap_generator._height, 3.0)
        self.assertEqual(self.heatmap_generator._blocked, {CellState.OCCUPIED})

    def test_generate_heatmap(self):
        """Tests the generate_heatmap method."""
        self.grid.get_width.return_value = 5
        self.grid.get_height.return_value = 5
        self.grid.get_cells.return_value = self.cells
        self.grid.get_neighbours_at.side_effect = lambda pos: [
            cell for cell in self.cells if cell.get_x() != pos.get_x() or cell.get_y() != pos.get_y()
        ]

        heatmap = self.heatmap_generator.generate_heatmap(self.cells, self.grid)

        self.assertIsInstance(heatmap, Heatmap)
        self.assertEqual(heatmap.get_width(), 5)
        self.assertEqual(heatmap.get_height(), 5)
        for cell in self.cells:
            self.assertEqual(heatmap.get_cell_at_pos(cell), 0)

if __name__ == '__main__':
    unittest.main()