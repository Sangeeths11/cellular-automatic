import pygame
from pygame import Surface

from typing import TYPE_CHECKING

from pygame.font import SysFont

from visualisation.visualisation_feature import VisualisationFeatureBase

if TYPE_CHECKING:
    from simulation.core.simulation import Simulation
    from visualisation.visualisation import Visualisation
    from visualisation.visualisation_helper import VisualisationHelper


class FlowMetersVisualisation(VisualisationFeatureBase):
    def __init__(self, sim: 'Simulation', vis: 'Visualisation', vis_helper: 'VisualisationHelper'):
        super().__init__(sim, vis, vis_helper)
        self._small_font = SysFont(self._font_name, self._small_font_size)
        self._render_names = self._helper.get_cell_size() > 40

    def set_render_names(self, render_names: bool) -> None:
        self._render_names = render_names

    def get_render_names(self) -> bool:
        return self._render_names


    def _describe_state(self) -> str:
        if self._visualisation.get_flow_meters() is None:
            return "No Flow Meters"

        return f"\nShow names: {self._render_names}\n".join([f"{flow_meter.get_name()}: {flow_meter.get_flow_rate()}" for flow_meter in self._visualisation.get_flow_meters()])

    def _render(self, surface: Surface) -> None:
        flow_meters = self._visualisation.get_flow_meters()
        if flow_meters is not None:
            for flow_meter in flow_meters:
                for cell in flow_meter.get_cells():
                    cell_rect = self._helper.get_rect_at(cell)
                    pygame.draw.rect(surface, (200, 200, 200), cell_rect, 1)

                    if self._render_names:
                        name = self._small_font.render(f"{flow_meter.get_name()}: {flow_meter.get_flow_rate():.3f}", True, self._text_color)
                        text_pos = self._helper.get_x_center_pos_at(cell, name.get_height())
                        surface.blit(name, name.get_rect(center=text_pos))

