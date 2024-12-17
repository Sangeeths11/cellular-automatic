from src.dtoModule.tileDTO import TileDTO

class Grid():

    def __init__(self) -> None:
        #TODO: Find a smart way to initilaize the grid
        self.tiles: list[list] = [[]]

    def getTiles(self) -> list[list]:
        return self.tiles
    
    def simulate(self):
        #TODO: Create a smart way to step in time
        pass

    def updateTileValues(self) -> None:
        #TODO: Find a way to update the TileValues
        pass

