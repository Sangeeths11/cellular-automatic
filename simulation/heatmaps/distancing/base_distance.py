from abc import abstractmethod, ABC

from simulation.core.position import Position


class DistanceBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def calculate_distance(self, pos1: Position, pos2: Position) -> float:
        pass