from typing import Generator

from simulation.neighbourhood.base_neighbourhood import NeighbourhoodBase


class NeumannNeighbourhood(NeighbourhoodBase):
    """
    NeumannNeighbourhood represents a neighbourhood which returns all neighbours in cardinal directions around the given cell
    """
    def get_neighbours(self, x: int, y: int, width: int, height: int) -> Generator[tuple[int, int]]:
        for i in range(x - width, x + width + 1):
            if i != x:
                yield i, y

        for j in range(y - height, y + height + 1):
            if j != y:
                yield x, j