from abc import ABC


class Position(ABC):
    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_position(self) -> tuple[int, int]:
        return self._x, self._y

    def pos_equals(self, other: object) -> bool:
        return isinstance(other, Position) and self.get_x() == other.get_x() and self.get_y() == other.get_y()

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return False
        return self._x == other.get_x() and self._y == other.get_y()

    def __hash__(self) -> int:
        return hash((self._x, self._y))

    def __str__(self) -> str:
        return f"({self._x}, {self._y})"