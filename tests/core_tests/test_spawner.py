import unittest
from unittest.mock import Mock, patch
from simulation.core.spawner import Spawner
from simulation.core.cell import Cell
from simulation.core.target import Target
from simulation.heatmaps.distancing.base_distance import DistanceBase
from utils.immutable_list import ImmutableList

class TestSpawner(unittest.TestCase):
    def setUp(self):
        self.cells = [Mock(spec=Cell) for _ in range(5)]
        self.targets = [Mock(spec=Target) for _ in range(2)]
        self.distancing = Mock(spec=DistanceBase)
        self.spawner = Spawner(
            name="TestSpawner",
            distancing=self.distancing,
            cells=self.cells,
            targets=self.targets,
            total_spawns=10,
            batch_size=2,
            spawn_delay=1.0,
            initial_delay=0.0
        )

    def test_initialization(self):
        """Test spawner initialization."""
        self.assertEqual(self.spawner.get_name(), "TestSpawner")
        self.assertEqual(self.spawner.get_cells()._data, self.cells)
        self.assertEqual(self.spawner._total_spawns, 10)
        self.assertEqual(self.spawner._batch_size, 2)
        self.assertEqual(self.spawner._spawn_delay, 1.0)
        self.assertEqual(self.spawner._current_delay, 0.0)
        self.assertEqual(self.spawner._distancing, self.distancing)
        self.assertEqual(self.spawner._targets, self.targets)

    def test_get_name(self):
        """Test get_name method."""
        self.assertEqual(self.spawner.get_name(), "TestSpawner")

    def test_get_cells(self):
        """Test get_cells method."""
        self.assertEqual(list(self.spawner.get_cells()), self.cells)

    def test_can_spawn_initial(self):
        """Test can_spawn initially."""
        self.assertTrue(self.spawner.can_spawn())

    def test_is_done_initial(self):
        """Test is_done initially."""
        self.assertFalse(self.spawner.is_done())

    def test_can_spawn_after_delay(self):
        """Test can_spawn after increasing delay."""
        self.spawner._current_delay = 1.0
        self.assertFalse(self.spawner.can_spawn())
        self.spawner._current_delay = 0.0
        self.assertTrue(self.spawner.can_spawn())

    def test_is_done_after_spawns(self):
        """Test is_done after all spawns are done."""
        self.spawner._total_spawns = 0
        self.assertTrue(self.spawner.is_done())

    def test_update_spawning(self):
        """Test update method when spawning occurs."""
        pedestrians = list(self.spawner.update(1.0))
        self.assertEqual(len(pedestrians), 2)
        self.assertEqual(self.spawner._current_delay, 1.0)
        self.assertEqual(self.spawner._total_spawns, 8)

    @patch.object(Spawner, 'spawn')
    def test_update_no_spawn_due_to_delay(self, mock_spawn):
        """Test update method when spawn delay hasn't elapsed."""
        self.spawner._current_delay = 0.5
        pedestrians = list(self.spawner.update(0.4))
        mock_spawn.assert_not_called()
        self.assertEqual(pedestrians, [])
        # compare with .5 - .4 = because of floating point error (0.0999999999999998)
        self.assertEqual(self.spawner._current_delay, 0.5 - 0.4)

    @patch.object(Spawner, 'spawn')
    def test_update_no_spawn_due_to_total_spawns(self, mock_spawn):
        """Test update method when total_spawns reached zero."""
        self.spawner._total_spawns = 0
        pedestrians = list(self.spawner.update(1.0))
        mock_spawn.assert_not_called()
        self.assertEqual(pedestrians, [])
        self.assertTrue(self.spawner.is_done())

    def test_update_with_none_total_spawns(self):
        """Test update when total_spawns is None (infinite spawns)."""
        self.spawner._total_spawns = None
        with patch.object(Spawner, 'spawn', return_value=[Mock(), Mock()]) as mock_spawn:
            pedestrians = list(self.spawner.update(1.0))
            mock_spawn.assert_called_once()
            self.assertEqual(len(pedestrians), 2)
            self.assertIsNone(self.spawner._total_spawns)

if __name__ == '__main__':
    unittest.main()