from abc import abstractmethod, ABC

from simulation.core.position import Position


class DistanceBase(ABC):
    def __init__(self, scale: float = 1.0):
        self._scale = scale
        pass

    @abstractmethod
    def _calculate_distance(self, pos1: Position, pos2: Position) -> float:
        pass

    def get_scale(self) -> float:
        return self._scale

    def calculate_distance(self,  pos1: Position, pos2: Position) -> float:
        return self._calculate_distance(pos1, pos2) * self._scale