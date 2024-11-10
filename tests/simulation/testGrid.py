import unittest
from src.simulation.grid import Grid
from src.enums.tileStatus import TileStatus
from src.simulation.tile import Tile

class SimulationExceptionTest(unittest.TestCase):

    def test_gridWith10x10Tile_setsTiles(self):
        # ARRANGE
        length: int = 10
        width: int = 10

        # ACT
        grid = Grid(length, width)

        # ASSERT
        self.assertEqual(length, len(grid.getTiles()))
        for row in grid.getTiles():
            self.assertEqual(width, len(row))
            for tile in row:
                self.assertEqual(TileStatus.FREE, tile.getTileDTO().getTileStatus())

        
if __name__ == "__main__":
    unittest.main()