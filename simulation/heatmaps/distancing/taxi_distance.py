from simulation.core.position import Position
from simulation.heatmaps.distancing.base_distance import DistanceBase


class TaxiDistance(DistanceBase):
    def _calculate_distance(self, pos1: Position, pos2: Position) -> float:
        return abs(pos1.get_x() - pos2.get_x()) + abs(pos1.get_y() - pos2.get_y())