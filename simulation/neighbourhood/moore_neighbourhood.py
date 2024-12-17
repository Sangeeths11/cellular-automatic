from typing import Generator

from simulation.neighbourhood.base_neighbourhood import NeighbourhoodBase


class MooreNeighbourhood(NeighbourhoodBase):
    """
    MooreNeighbourhood represents a neighbourhood which returns all neighbours in a rectangle defined by width and height around the given cell
    """
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

    def get_neighbours(self, x: int, y: int, width: int, height: int) -> Generator[tuple[int, int]]:
        for i in range(x - width, x + width + 1):
            for j in range(y - height, y + height + 1):
                if i == x and j == y:
                    continue

                if i < 0 or i >= self._width or j < 0 or j >= self._height:
                    continue

                yield i, j
