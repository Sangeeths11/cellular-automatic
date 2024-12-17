import unittest
from unittest.mock import Mock

from simulation.heatmaps.distancing.euclidean_distance import EuclideanDistance
from simulation.heatmaps.fast_marching_heatmap_generator import FastMarchingHeatmapGenerator
from simulation.core.cell import Cell
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.core.cell_state import CellState
from simulation.neighbourhood.moore_neighbourhood import MooreNeighbourhood


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

    def test_generate_heatmap__generates__expected_values_of_fast_marching(self):
        """Tests the implementation of the Fast Marching Method. Comparing it to the values of CDS307 Slides of day 4 page 19"""
        # Arrange
        grid = SimulationGrid(3, 3, MooreNeighbourhood)
        distance = EuclideanDistance(1.0)
        generator = FastMarchingHeatmapGenerator(distance)

        # Act
        heatmap = generator.generate_heatmap([grid.get_cell(0, 2)], grid)

        # Assert
        expected = [
            2.0, 2.2, 2.9,
            1.0, 1.7, 2.2,
            0.0, 1.0, 2.0
        ]

        for i, value in enumerate(heatmap.get_cells()):
            self.assertAlmostEqual(value, expected[i], places=1)


if __name__ == '__main__':
    unittest.main()