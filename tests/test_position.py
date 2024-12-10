import unittest
from simulation.core.position import Position

class ConcretePosition(Position):
    pass

class TestPosition(unittest.TestCase):
    def setUp(self):
        self.position = ConcretePosition(1, 2)
        self.same_position = ConcretePosition(1, 2)
        self.different_position = ConcretePosition(3, 4)

    def test_initialization(self):
        """Tests initialization and getters."""
        self.assertEqual(self.position.get_x(), 1)
        self.assertEqual(self.position.get_y(), 2)
        self.assertEqual(self.position.get_position(), (1, 2))

    def test_equality(self):
        """Tests the __eq__ and __ne__ methods."""
        self.assertEqual(self.position, self.same_position)
        self.assertNotEqual(self.position, self.different_position)
        self.assertFalse(self.position == (1, 2))

    def test_equals_method(self):
        """Tests the equals method."""
        self.assertTrue(self.position.pos_equals(self.same_position))
        self.assertFalse(self.position.pos_equals(self.different_position))
        self.assertFalse(self.position.pos_equals((1, 2)))

    def test_hash(self):
        """Tests the __hash__ method."""
        self.assertEqual(hash(self.position), hash(self.same_position))
        self.assertNotEqual(hash(self.position), hash(self.different_position))

    def test_str(self):
        """Tests the __str__ method."""
        self.assertEqual(str(self.position), "(1, 2)")

if __name__ == '__main__':
    unittest.main()