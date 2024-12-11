import unittest
from collections.abc import generator
from unittest.mock import Mock

from simulation.core.pedestrian import Pedestrian
from simulation.heatmaps.distancing.euclidean_distance import EuclideanDistance
from simulation.heatmaps.repulsion_heatmap_generator import RepulsionHeatmapGenerator
from simulation.core.cell import Cell
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.core.cell_state import CellState
from simulation.neighbourhood.moore_neighbourhood import MooreNeighbourhood


class TestSocialDistancingHeatmapGenerator(unittest.TestCase):
    def setUp(self):
        self.distancing = Mock(spec=DistanceBase)
        self.grid = Mock(spec=SimulationGrid)
        self.cells = [Mock(spec=Cell) for _ in range(3)]
        self.heatmap_generator = RepulsionHeatmapGenerator(self.distancing, width=3.0, height=3.0)

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

    def test_generate_heatmap__generates__expected_heatmap_values(self):
        """Tests if social distancing algorithm works as expected."""
        # Arrange
        distancing = EuclideanDistance(1.0)
        grid = SimulationGrid(3, 3, MooreNeighbourhood)
        pedestrian = Mock(spec=Pedestrian)
        grid.get_cell(0,0).set_pedestrian(pedestrian)
        generator = RepulsionHeatmapGenerator(distancing, 3, 3, {CellState.OCCUPIED})

        # Act
        heatmap = generator.generate_heatmap([grid.get_cell(0,0)], grid)

        # Assert
        # Setup expected with manually calculating the formula from the document CDS307-Aufgabe-Zellularautomat.pdf page 2
        # w = h = 3
        # up_d = h * exp(1/((d/w)^2 - 1)) if abs(d) < w else 0 (minus got omitted since a positive heatmap value means higher repulsion)
        expected = [
          1.103, 0.973, 0.495,
          0.973, 0.829, 0.316,
          0.495, 0.316, 0.000
        ]

        for i, value in enumerate(heatmap.get_cells()):
            self.assertAlmostEqual(value, expected[i], 2)

    def test_generate_heatmap__only_ignores_cells__not_in_blocked_list(self):
        """Tests if the heatmap generator ignores cells that are not in the blocked list."""
        # Arrange
        distancing = EuclideanDistance(1.0)
        grid = SimulationGrid(3, 3, MooreNeighbourhood)
        pedestrian = Mock(spec=Pedestrian)
        grid.get_cell(0,0).set_pedestrian(pedestrian)
        generator = RepulsionHeatmapGenerator(distancing, 3, 3, {})

        # Act
        heatmap = generator.generate_heatmap([grid.get_cell(0,0)], grid)

        # Assert
        for value in heatmap.get_cells():
            self.assertGreaterEqual(value, 0.0)

if __name__ == '__main__':
    unittest.main()