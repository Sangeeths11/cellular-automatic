import unittest
from simulation.core.cell_state import CellState

class TestCellState(unittest.TestCase):
    def test_cell_state_values_exist(self):
        """Test that all expected CellState values exist"""
        self.assertTrue(hasattr(CellState, 'FREE'))
        self.assertTrue(hasattr(CellState, 'OCCUPIED'))
        self.assertTrue(hasattr(CellState, 'OBSTACLE'))

    def test_cell_state_values(self):
        """Test that CellState values are unique"""
        self.assertNotEqual(CellState.FREE, CellState.OCCUPIED)
        self.assertNotEqual(CellState.FREE, CellState.OBSTACLE)
        self.assertNotEqual(CellState.OCCUPIED, CellState.OBSTACLE)

    def test_cell_state_type(self):
        """Test that CellState is an Enum"""
        self.assertTrue(isinstance(CellState.FREE, CellState))
        self.assertTrue(isinstance(CellState.OCCUPIED, CellState))
        self.assertTrue(isinstance(CellState.OBSTACLE, CellState))

    def test_cell_state_comparison(self):
        """Test that CellState values can be compared"""
        states = [CellState.FREE, CellState.OCCUPIED, CellState.OBSTACLE]
        for state in states:
            self.assertEqual(state, state)
            
if __name__ == '__main__':
    unittest.main()