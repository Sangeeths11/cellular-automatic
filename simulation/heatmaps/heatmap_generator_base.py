from abc import ABC, abstractmethod
from typing import Iterable

from simulation.core.cell import Cell
from simulation.core.grid_base import GridBase
from simulation.core.simulation_grid import SimulationGrid
from simulation.heatmaps.heatmap import Heatmap


class HeatmapGeneratorBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate_heatmap(self, target: Iterable[Cell], grid: SimulationGrid) -> Heatmap:
        pass