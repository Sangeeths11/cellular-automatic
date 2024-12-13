import math

import pygame.font
from pygame import Surface

from visualisation.visualisation_feature import VisualisationFeatureBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.core.simulation import Simulation
    from visualisation.visualisation import Visualisation
    from visualisation.visualisation_helper import VisualisationHelper


class PedestrianVisualisationFeature(VisualisationFeatureBase):
    def __init__(self, sim: 'Simulation', vis: 'Visualisation', vis_helper: 'VisualisationHelper'):
        super().__init__(sim, vis, vis_helper)
        self._render_details = self._helper.get_cell_size() > 20
        self._render_target_line = self._helper.get_cell_size() > 30
        self._font = pygame.font.SysFont(self._font_name, self._font_size)

    def set_render_details(self, state: bool) -> None:
        self._render_details = state

    def set_render_target_line(self, state: bool) -> None:
        self._render_target_line = state

    def get_render_details(self) -> bool:
        return self._render_details

    def get_render_target_line(self) -> bool:
        return self._render_target_line

    def _describe_state(self) -> str:
        return f"Show details: {self._render_details}\nShow target line: {self._render_target_line}"

    def _render(self, surface: Surface) -> None:
        for pedestrian in self._simulation.get_pedestrians():
            spawner_color = self._visualisation.get_spawner_color(pedestrian.get_spawner())

            if pedestrian.has_targeted_cell():
                target = pedestrian.get_targeted_cell()
                target_color = self._visualisation.get_target_color(pedestrian.get_target())
                if self._render_target_line:
                    from_pos = self._helper.get_centered_pos_at(pedestrian)
                    to_pos = self._helper.get_centered_pos_at(target)
                    pygame.draw.line(surface, target_color, from_pos, to_pos, 2)

                # calculate the angle between the pedestrian and the target
                angle = math.atan2(target.get_y() - pedestrian.get_y(), target.get_x() - pedestrian.get_x())
                triangle = self._helper.get_small_triangle_at(pedestrian, angle)
                pygame.draw.polygon(surface, spawner_color, triangle)
                pygame.draw.lines(surface, target_color, True, triangle, 2)
            else:
                rect = self._helper.get_small_rect_at(pedestrian)
                pygame.draw.rect(surface, spawner_color, rect)

            if self._render_details:
                speed_info = self._font.render(f"[{pedestrian.get_id()}] {pedestrian.get_average_speed():.2f}m/s, {pedestrian.get_optimal_speed():.2f}m/s, {pedestrian.get_current_distance():.2f}m", True, self._text_color)
                text_pos = self._helper.get_x_center_pos_at(pedestrian, speed_info.get_height())
                surface.blit(speed_info, speed_info.get_rect(center=text_pos))
