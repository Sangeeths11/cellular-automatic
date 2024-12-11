import pygame
from pygame import Surface

from simulation.core.position import Position
from simulation.core.target import Target
from visualisation.visualisation_feature import VisualisationFeatureBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.core.simulation import Simulation
    from visualisation.visualisation import Visualisation
    from visualisation.visualisation_helper import VisualisationHelper


class TargetHeatmapVisualisationFeature(VisualisationFeatureBase):
    def __init__(self, sim: 'Simulation', vis: 'Visualisation', vis_helper: 'VisualisationHelper'):
        super().__init__(sim, vis, vis_helper)
        self._selected_target_index = 0
        self._selected_target = None
        self._font = pygame.font.SysFont(self._font_name, self._small_font_size)
        self._show_social_distancing = True
        self._max_social_distancing_value = sim._social_distancing_generator.get_max_value()
        self._max_obstacle_repulsion_value = sim._obstacle_repulsion_heatmap_generator.get_max_value() if sim._obstacle_repulsion_heatmap_generator is not None else 0
        self._max_heatmap_value: float = 0.0
        self._max_repulsion_value: float = 0.0
        self._render_details = self._helper.get_cell_size() > 10
        self._show_obstacle_repulsion = sim._obstacle_repulsion_heatmap_generator is not None
        self._update_max_heatmap_values()

    def next_target(self):
        self._selected_target_index = (self._selected_target_index + 1) % (len(self._simulation.get_targets()) + 1)
        self._selected_target = None if self._selected_target_index == 0 else self._simulation.get_targets()[self._selected_target_index-1]

    def previous_target(self):
        self._selected_target_index = (self._selected_target_index - 1) % (len(self._simulation.get_targets()) + 1)
        self._selected_target = None if self._selected_target_index == 0 else self._simulation.get_targets()[self._selected_target_index-1]

    def set_target(self, target: 'Target'):
        if target is None:
            self._selected_target_index = 0
            self._selected_target = None
        else:
            self._selected_target_index = self._simulation.get_targets().index(target) + 1
            self._selected_target = target

    def _update_max_heatmap_values(self):
        self._max_heatmap_value = self._simulation.get_max_grid_distance()
        self._max_repulsion_value = 0.0
        if self._show_social_distancing:
            self._max_heatmap_value += self._max_social_distancing_value
            self._max_repulsion_value += self._max_social_distancing_value

        if self._show_obstacle_repulsion:
            self._max_heatmap_value += self._max_obstacle_repulsion_value
            self._max_repulsion_value += self._max_obstacle_repulsion_value

    def set_obstacle_repulsion(self, value: bool):
        self._show_obstacle_repulsion = value
        self._update_max_heatmap_values()

    def get_obstacle_repulsion(self) -> bool:
        return self._show_obstacle_repulsion

    def set_social_distancing(self, value: bool):
        self._show_social_distancing = value
        self._update_max_heatmap_values()

    def get_social_distancing(self) -> bool:
        return self._show_social_distancing

    def _describe_state(self) -> str:
        return f"Selected target: {'None' if self._selected_target is None else self._selected_target.get_name()}\nShow social distancing: {self._show_social_distancing}"

    def _render(self, surface: Surface) -> None:
        heatmap = self._selected_target.get_heatmap() if self._selected_target is not None else None
        social_distancing_heatmap = self._simulation.get_social_distancing_heatmap()
        obstacle_repulsion_heatmap = self._simulation.get_obstacle_repulsion_heatmap()

        for x in range(self._simulation.get_grid().get_width()):
            for y in range(self._simulation.get_grid().get_height()):
                value = heatmap.get_cell(x, y) if heatmap is not None else 0

                min_r = 0
                if self._show_social_distancing:
                    social_distance = social_distancing_heatmap.get_cell(x, y)
                    min_r = min(200, int(social_distance/(self._max_repulsion_value / 2) * 200))
                    value += social_distance

                if self._show_obstacle_repulsion and self._simulation._obstacle_repulsion_heatmap_generator is not None:
                    obstacle_repulsion = obstacle_repulsion_heatmap.get_cell(x, y)
                    min_r = min(200, min_r + int(obstacle_repulsion / (self._max_repulsion_value / 2) * 200))
                    value += obstacle_repulsion

                # bias = self._simulation._social_distancing_generator.get_bias(self._simulation._grid.get_cell(x, y), self._simulation.get_pedestrians()[0])
                # value -= bias

                ratio = min(max(value, 0), self._max_heatmap_value) / self._max_heatmap_value
                color = self._helper.mix_colors((255, 200, 0), (min_r, 100, 255), ratio)
                rect = self._helper.get_rect(x, y)
                pygame.draw.rect(surface, color, rect)
                if self._render_details:
                    value_text = self._font.render(f"{value:.2f}", True, (40, 40, 40))
                    text_pos = self._helper.get_centered_pos(x, y)
                    surface.blit(value_text, value_text.get_rect(center=text_pos))

        if self._selected_target is not None:
            min_x, min_y, max_x, max_y = float('inf'), float('inf'), 0, 0
            for cell in self._selected_target.get_cells():
                min_x = min(min_x, cell.get_x())
                min_y = min(min_y, cell.get_y())
                max_x = max(max_x, cell.get_x())
                max_y = max(max_y, cell.get_y())

            pygame.draw.rect(surface, (255, 255, 255), self._helper.get_rect_with_size(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1), 2)