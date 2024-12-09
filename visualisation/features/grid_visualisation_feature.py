import pygame
from pygame import Surface

from simulation.core.cell_state import CellState
from visualisation.visualisation_feature import VisualisationFeatureBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.core.simulation import Simulation
    from visualisation.visualisation import Visualisation
    from visualisation.visualisation_helper import VisualisationHelper


class GridVisualisationFeature(VisualisationFeatureBase):
    def __init__(self, sim: 'Simulation', vis: 'Visualisation', vis_helper: 'VisualisationHelper'):
        super().__init__(sim, vis, vis_helper)
        self._show_lines = True

    def set_show_lines(self, show_lines: bool) -> None:
        self._show_lines = show_lines

    def get_show_lines(self) -> bool:
        return self._show_lines

    def _describe_state(self) -> str:
        return None

    def _render(self, surface: Surface) -> None:
        for x in range(self._simulation.get_grid().get_width()):
            for y in range(self._simulation.get_grid().get_height()):
                cell = self._simulation.get_grid().get_cell(x, y)
                cell_rect = self._helper.get_rect_at(cell)
                if cell.get_state() == CellState.OBSTACLE:
                    pygame.draw.rect(surface, (0, 0, 0), cell_rect)

                if self._show_lines:
                    pygame.draw.rect(surface, (0, 0, 0), cell_rect, 1)
