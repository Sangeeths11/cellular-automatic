import math

from simulation.core.position import Position
from simulation.heatmaps.distancing.base_distance import DistanceBase


class EuclideanDistance(DistanceBase):
    def _calculate_distance(self, pos1: Position, pos2: Position) -> float:
        return math.sqrt(math.pow (pos1.get_x() - pos2.get_x(), 2) + math.pow(pos1.get_y() - pos2.get_y(), 2))
