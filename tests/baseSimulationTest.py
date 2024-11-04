import unittest
from src.simulation.baseSimulation import BaseSimulation
from src.exceptions.simulationException import SimulationException

class SimulationExceptionTest(unittest.TestCase):

    def test_simulateStep_throws(self):
        # ARRANGE
        baseSilumlation = BaseSimulation(None)

        # ACT
        self.assertRaises(SimulationException, baseSilumlation.simulateStep)

        
if __name__ == "__main__":
    unittest.main()