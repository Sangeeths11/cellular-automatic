

class TileValueDTO():

    def __init__(self, x: int, y: int, value: float = float("inf")) -> None:
        self.x = x
        self.y = y
        self.value = value

    def getX(self) -> int:
        return self.x

    def setX(self, x) -> None:
        self.x = x

    def getY(self) -> int:
        return self.y

    def setY(self, y) -> None:
        self.y = y