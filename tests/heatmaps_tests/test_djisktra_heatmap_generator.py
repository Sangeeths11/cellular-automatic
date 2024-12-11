import unittest
from unittest.mock import Mock

from simulation.core.cell_state import CellState
from simulation.heatmaps.distancing.euclidean_distance import EuclideanDistance
from simulation.heatmaps.djisktra_heatmap_generator import DijkstraHeatmapGenerator
from simulation.core.cell import Cell
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.neighbourhood.moore_neighbourhood import MooreNeighbourhood


class TestDijkstraHeatmapGenerator(unittest.TestCase):
    def setUp(self):
        self.distancing = Mock(spec=DistanceBase)
        self.grid = Mock(spec=SimulationGrid)
        self.cells = [Mock(spec=Cell) for _ in range(3)]
        self.heatmap_generator = DijkstraHeatmapGenerator(self.distancing)

        for i, cell in enumerate(self.cells):
            cell.get_x.return_value = i
            cell.get_y.return_value = i

    def test_initialization(self):
        """Tests initialization of the DijkstraHeatmapGenerator."""
        self.assertEqual(self.heatmap_generator._distancing, self.distancing)

    def test_generate_heatmap(self):
        """Tests the generate_heatmap method."""
        self.grid.get_width.return_value = 5
        self.grid.get_height.return_value = 5
        self.grid.get_cells.return_value = self.cells
        self.grid.get_neighbours_at.return_value = []

        heatmap = self.heatmap_generator.generate_heatmap(self.cells, self.grid)

        self.assertIsInstance(heatmap, Heatmap)
        self.assertEqual(heatmap.get_width(), 5)
        self.assertEqual(heatmap.get_height(), 5)
        for cell in self.cells:
            heatmap.set_cell_at_pos(cell, 0)
            self.assertEqual(heatmap.get_cell_at_pos(cell), 0)

    def test_call_generate_heatmap__generates__expected_values_of_dijkstra(self):
        """Tests the generate_heatmap method to see if dijkstra algorithm is correctly implemented."""
        # Arrange
        grid = SimulationGrid(3, 3, MooreNeighbourhood)
        distance = EuclideanDistance(1)
        generator = DijkstraHeatmapGenerator(distance)

        # Act
        heatmap = generator.generate_heatmap([grid.get_cell(1, 1)], grid)

        # Assert
        expected: list[float] = [
            1.4, 1.0, 1.4,
            1.0, 0.0, 1.0,
            1.4, 1.0, 1.4
        ]

        for i, value in enumerate(heatmap.get_cells()):
            self.assertAlmostEqual(value, expected[i], places=1)

    def test_call_generate_heatmap__generates__expected_values_of_dijkstra__with_obstacle(self):
        """Tests the generate_heatmap method to see if dijkstra algorithm is correctly implemented."""
        # Arrange
        grid = SimulationGrid(3, 3, MooreNeighbourhood)
        distance = EuclideanDistance(1)
        generator = DijkstraHeatmapGenerator(distance, {CellState.OBSTACLE})

        grid.get_cell(1, 0).set_osbtacle()

        # Act
        heatmap = generator.generate_heatmap([grid.get_cell(1, 1)], grid)

        # Assert
        expected: list[float] = [
            1.4, float('inf'), 1.4,
            1.0, 0.0, 1.0,
            1.4, 1.0, 1.4
        ]

        for i, value in enumerate(heatmap.get_cells()):
            self.assertAlmostEqual(value, expected[i], places=1)

    def test_call_generate_heatmap__ignores_obstacle__when_not_in_block_list(self):
        """Tests the generate_heatmap method to see if dijkstra algorithm is correctly implemented."""
        # Arrange
        grid = SimulationGrid(3, 3, MooreNeighbourhood)
        distance = EuclideanDistance(1)
        generator = DijkstraHeatmapGenerator(distance, {})

        grid.get_cell(1, 0).set_osbtacle()

        # Act
        heatmap = generator.generate_heatmap([grid.get_cell(1, 1)], grid)

        # Assert
        expected: list[float] = [
            1.4, 1.0, 1.4,
            1.0, 0.0, 1.0,
            1.4, 1.0, 1.4
        ]

        for i, value in enumerate(heatmap.get_cells()):
            self.assertAlmostEqual(value, expected[i], places=1)


if __name__ == '__main__':
    unittest.main()