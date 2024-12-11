import unittest
from unittest.mock import Mock
from simulation.heatmaps.fast_marching_heatmap_generator import FastMarchingHeatmapGenerator
from simulation.core.cell import Cell
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.core.cell_state import CellState

class TestFastMarchingHeatmapGenerator(unittest.TestCase):
    def setUp(self):
        self.distancing = Mock(spec=DistanceBase)
        self.grid = Mock(spec=SimulationGrid)
        self.cells = [Mock(spec=Cell) for _ in range(3)]
        self.heatmap_generator = FastMarchingHeatmapGenerator(self.distancing)

        for i, cell in enumerate(self.cells):
            cell.get_x.return_value = i
            cell.get_y.return_value = i
            cell.get_state.return_value = CellState.FREE

    def test_initialization(self):
        """Tests initialization of the FastMarchingHeatmapGenerator."""
        self.assertEqual(self.heatmap_generator._distancing, self.distancing)
        self.assertEqual(self.heatmap_generator._blocked, {CellState.OBSTACLE})

    def test_generate_heatmap(self):
        """Tests the generate_heatmap method."""
        self.grid.get_width.return_value = 3
        self.grid.get_height.return_value = 3
        self.grid.get_cells.return_value = self.cells

        self.grid.get_neighbours_at.side_effect = lambda pos: [
            cell for cell in self.cells if cell.get_x() != pos.get_x() or cell.get_y() != pos.get_y()
        ]

        self.cells[1].get_state.return_value = CellState.OBSTACLE

        heatmap = self.heatmap_generator.generate_heatmap(self.cells, self.grid)

        expected_grid = [
            [0, 1, 2],
            [1, float('inf'), 3],
            [2, 3, 4]
        ]

        for y in range(3):
            for x in range(3):
                self.assertEqual(heatmap.get_cell(x, y), expected_grid[y][x], f"Mismatch at ({x}, {y})")

if __name__ == '__main__':
    unittest.main()