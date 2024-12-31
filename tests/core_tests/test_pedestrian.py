import unittest
from unittest.mock import Mock
from simulation.core.pedestrian import Pedestrian
from simulation.core.position import Position
from simulation.core.cell import Cell
from simulation.core.target import Target
from simulation.core.spawner import Spawner
from simulation.heatmaps.distancing.base_distance import DistanceBase
from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode

class TestPedestrian(unittest.TestCase):
    def setUp(self):
        self.distancing = Mock(spec=DistanceBase)
        self.distancing.calculate_distance.return_value = 1.0

        self.spawner = Mock(spec=Spawner)
        self.target = Mock(spec=Target)
        self.target.is_inside_target.return_value = False

        self.real_cell = Cell(1, 2)
        self.cell = Mock(spec=Cell, wraps=self.real_cell)
        self.cell.is_free.return_value = True

        self.pedestrian = Pedestrian(
            x=0,
            y=0,
            speed=1.5,
            spawner=self.spawner,
            target=self.target,
            distancing=self.distancing
        )
    
    def test_initialization(self):
        """Tests the correct initialization of a Pedestrian."""
        self.assertEqual(self.pedestrian.get_x(), 0)
        self.assertEqual(self.pedestrian.get_y(), 0)
        self.assertEqual(self.pedestrian.get_optimal_speed(), 1.5)
        self.assertEqual(self.pedestrian.get_current_distance(), float('inf'))
        self.assertFalse(self.pedestrian.has_reached_target())

    def test_set_reached_target(self):
        """Tests the methods set_reached_target and has_reached_target."""
        self.pedestrian.set_reached_target()
        self.assertTrue(self.pedestrian.has_reached_target())

    def test_set_target_cell_success(self):
        """Tests successful setting of a target cell."""
        self.pedestrian.set_target_cell(self.cell)
        self.assertEqual(self.pedestrian.get_targeted_cell(), self.cell)
        self.assertEqual(self.pedestrian.get_current_distance(), 1.0)

    def test_set_target_cell_none(self):
        """Tests setting the target cell to None."""
        self.pedestrian.set_target_cell(None)
        self.assertIsNone(self.pedestrian.get_targeted_cell())
        self.assertEqual(self.pedestrian.get_current_distance(), float('-inf'))

    def test_set_target_cell_already_in_cell(self):
        """Tests that an exception is raised when the target cell is the current position."""
        cell = Cell(0, 0)
        with self.assertRaises(SimulationError) as context:
            self.pedestrian.set_target_cell(cell)
        self.assertEqual(context.exception.get_code(), SimulationErrorCode.ALREADY_IN_CELL.value[0])

    def test_can_move_true(self):
        """Tests that can_move returns True when the pedestrian can move."""
        self.pedestrian.set_target_cell(self.cell)
        self.pedestrian._current_distance = -0.1  # Simulate time has passed
        self.cell.is_free.return_value = True
        self.assertTrue(self.pedestrian.can_move())

    def test_can_move_false(self):
        """Tests that can_move returns False when the pedestrian cannot move."""
        self.pedestrian.set_target_cell(self.cell)
        self.pedestrian._current_distance = 0.5
        self.cell.is_free.return_value = True
        self.assertFalse(self.pedestrian.can_move())

    def test_move_success(self):
        """Tests successful movement of the pedestrian."""
        self.pedestrian.set_target_cell(self.cell)
        self.pedestrian._current_distance = -0.1
        self.cell.is_free.return_value = True
        self.pedestrian.move()
        self.assertEqual(self.pedestrian.get_x(), 1)
        self.assertEqual(self.pedestrian.get_y(), 2)
        self.assertEqual(self.pedestrian._total_distance_moved, 1.0)
        self.assertEqual(self.pedestrian._distance_to_target, float('inf'))

    def test_move_failure(self):
        """Tests that an exception is raised when the pedestrian cannot move."""
        self.pedestrian.set_target_cell(self.cell)
        self.pedestrian._current_distance = 0.5
        with self.assertRaises(SimulationError) as context:
            self.pedestrian.move()
        self.assertEqual(context.exception.get_code(), SimulationErrorCode.CANNOT_MOVE.value[0])

    def test_update(self):
        """Tests the update method."""
        self.pedestrian._current_distance = 1.0
        self.pedestrian.update(0.5)
        self.assertEqual(self.pedestrian._current_distance, 0.25)
        self.assertEqual(self.pedestrian._time_alive, 0.5)

    def test_is_inside_target(self):
        """Tests the is_inside_target method."""
        self.target.is_inside_target.return_value = True
        self.assertTrue(self.pedestrian.is_inside_target())

    def test_getter_methods(self):
        """Tests the getter methods."""
        self.assertEqual(self.pedestrian.get_spawner(), self.spawner)
        self.assertEqual(self.pedestrian.get_target(), self.target)
        self.assertIsNotNone(self.pedestrian.get_id())

if __name__ == '__main__':
    unittest.main()