from enum import Enum
from dataclasses import dataclass, field

class ErrorCodeDataMixin:
    errorcode: int
    message: str

class SimulationErrorCodes(ErrorCodeDataMixin, Enum):
    ExampleError = 1, "Example ErrorCode"
    NOT_IMPLEMENTED_IN_SIMULATION = 2, "A Function in the simulation is not implemented"
    LENGTH_OF_GRID_INVALID = 3, "The legth of the grid has to be more than 0 and of type int"
    POINT_NOT_ON_GRID = 4, "The requested point is outside of the simulated grid."

if __name__ == "__main__":
    example = SimulationErrorCodes.ExampleError
    print(example.value)