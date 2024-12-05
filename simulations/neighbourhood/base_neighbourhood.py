from abc import abstractmethod, ABC
from typing import Generator

"""
NeighbourhoodBase represents a basic algorithm which returns a list of neighbouring coordinates given grid dimensions and a radius
"""
class NeighbourhoodBase(ABC):
    def __init__(self, width: int, height: int):
        self._height = height
        self._width = width

    @abstractmethod
    def get_neighbours(self, x: int, y: int, width: int, height: int) -> Generator[tuple[int, int]]:
        pass