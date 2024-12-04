from enum import Enum

class ErrorCodeDataMixin:
    error_code: int
    message: str

class SimulationErrorCode(ErrorCodeDataMixin, Enum):
    ExampleError = 1, "Example ErrorCode"
    NOT_IMPLEMENTED_IN_SIMULATION = 2, "A Function in the simulation is not implemented"
    LENGTH_OF_GRID_INVALID = 3, "The length of the grid has to be more than 0 and of type int"
    INVALID_COORDINATES = 4, "The accessed coordinates are outside of the grid"
    PEDESTRIAN_HEAT_MAP_CALCULATION_FAILED = 5, "The calculation of the pedestrian heat map failed"
    PEDESTRIAN_HEAT_MAP_NOT_FOUND = 6, "The Pedestrian Heat Map could not be found."
    CELL_OCCUPIED = 7, "The cell is already occupied with another pedestrian"
    CELL_BLOCKED = 8, "This cell is blocked by an obstacle and cannot be entered"
    CELL_NOT_OCCUPIED = 9, "Tried to unoccupy a cell that is not occupied"
    VALUE_NOT_INITIALIZED = 10, "The value has not been initialized yet, this mostly occurs when the first simulation step has not been executed"
    ALREADY_IN_CELL = 11, "The pedestrian is already in the cell and can't target it"
    CANNOT_MOVE = 12, "Move was called but the pedestrian can't move"
