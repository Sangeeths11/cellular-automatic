import unittest

from src.exceptions.simulationException import SimulationException

class SimulationExceptionTest(unittest.TestCase):

    def test_setsMessage(self):
        # ARRANGE
        message = "ErrorMessage"
        simulationException = SimulationException(message)

        # ACT
        retrivedMessage = simulationException.getMessage()

        # ASSERT
        self.assertEqual(message, retrivedMessage)

if __name__ == "__main__":
    unittest.main()