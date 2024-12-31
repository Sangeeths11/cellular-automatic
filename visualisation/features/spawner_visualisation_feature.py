import pygame
from pygame import Surface


from visualisation.visualisation_feature import VisualisationFeatureBase
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulation.core.simulation import Simulation
    from visualisation.visualisation import Visualisation
    from visualisation.visualisation_helper import VisualisationHelper


class SpawnerVisualisationFeature(VisualisationFeatureBase):
    def __init__(self, sim: 'Simulation', vis: 'Visualisation', vis_helper: 'VisualisationHelper'):
        super().__init__(sim, vis, vis_helper)
        self._font = pygame.font.SysFont(self._font_name, self._font_size)
        self._render_names = self._helper.get_cell_size() > 40

    def get_render_names(self) -> bool:
        return self._render_names

    def set_render_names(self, state: bool) -> None:
        self._render_names = state

    def _describe_state(self) -> str:
        return f"Show names: {self._render_names}"

    def _render(self, surface: Surface) -> None:
        for spawner in self._simulation.get_spawners():
            color = self._visualisation.get_spawner_color(spawner)
            for cell in spawner.get_cells():
                cell_rect = self._helper.get_small_rect_at(cell)
                pygame.draw.rect(surface, color, cell_rect)
                if self._render_names:
                    name = self._font.render(spawner.get_name(), True, self._text_color)
                    text_pos = self._helper.get_x_center_pos_at(cell, name.get_height())
                    surface.blit(name, name.get_rect(center=text_pos))
