import unittest

from src.exceptions.simulationException import SimulationException
from src.exceptions.simulationErrorCodes import SimulationErrorCodes

class SimulationExceptionTest(unittest.TestCase):

    def test_setsMessage(self):
        # ARRANGE
        simulationException = SimulationException(SimulationErrorCodes.ExampleError)

        # ACT / ASSERT
        self.assertEqual("Example ErrorCode", simulationException.getMessage())
        self.assertEqual(1, simulationException.getCode())

if __name__ == "__main__":
    unittest.main()