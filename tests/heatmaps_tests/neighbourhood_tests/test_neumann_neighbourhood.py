import unittest
from simulation.neighbourhood.neumann_neighbourhood import NeumannNeighbourhood

class TestNeumannNeighbourhood(unittest.TestCase):
    def setUp(self):
        self.width = 5
        self.height = 5
        self.neighbourhood = NeumannNeighbourhood(self.width, self.height)

    def test_get_neighbours(self):
        """Tests the get_neighbours method."""
        x, y = 2, 2
        neighbours = list(self.neighbourhood.get_neighbours(x, y, 1, 1))
        expected_neighbours = [
            (1, 2), (3, 2),
            (2, 1), (2, 3)
        ]
        self.assertEqual(sorted(neighbours), sorted(expected_neighbours))

    # Grid bound checking only appears in SimulationGrid, Neighbourhood is grid size agnostic
    # def test_get_neighbours_edge(self):
    #     """Tests the get_neighbours method at the edge of the grid."""
    #     x, y = 0, 0
    #     neighbours = list(self.neighbourhood.get_neighbours(x, y, 1, 1))
    #     expected_neighbours = [
    #         (1, 0), (0, 1)
    #     ]
    #     self.assertEqual(sorted(neighbours), sorted(expected_neighbours))
    #
    # def test_get_neighbours_corner(self):
    #     """Tests the get_neighbours method at the corner of the grid."""
    #     x, y = 4, 4
    #     neighbours = list(self.neighbourhood.get_neighbours(x, y, 1, 1))
    #     expected_neighbours = [
    #         (3, 4), (4, 3)
    #     ]
    #     self.assertEqual(sorted(neighbours), sorted(expected_neighbours))

if __name__ == '__main__':
    unittest.main()