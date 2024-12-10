import unittest
from simulation.heatmaps.distancing.euclidean_distance import EuclideanDistance
from simulation.core.position import Position

class TestEuclideanDistance(unittest.TestCase):
    def setUp(self):
        self.distance = EuclideanDistance(scale=2.0)
        self.pos1 = Position(0, 0)
        self.pos2 = Position(3, 4)

    def test_initialization(self):
        """Tests initialization and get_scale method."""
        self.assertEqual(self.distance.get_scale(), 2.0)

    def test_calculate_distance(self):
        """Tests the calculate_distance method."""
        expected_distance = 5.0 * 2.0  # Euclidean distance (3, 4) scaled by 2.0
        self.assertEqual(self.distance.calculate_distance(self.pos1, self.pos2), expected_distance)

if __name__ == '__main__':
    unittest.main()