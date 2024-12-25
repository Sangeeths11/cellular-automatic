import pygame
from pygame import Surface

from typing import TYPE_CHECKING
from visualisation.visualisation_feature import VisualisationFeatureBase

if TYPE_CHECKING:
    from simulation.core.simulation import Simulation
    from visualisation.visualisation import Visualisation
    from visualisation.visualisation_helper import VisualisationHelper


class FlowMetersVisualisation(VisualisationFeatureBase):
    def __init__(self, sim: 'Simulation', vis: 'Visualisation', vis_helper: 'VisualisationHelper'):
        super().__init__(sim, vis, vis_helper)

    def _describe_state(self) -> str:
        if self._visualisation.get_flow_meters() is None:
            return "No Flow Meters"

        return "\n".join([f"{flow_meter.get_name()}: {flow_meter.get_flow_rate()}" for flow_meter in self._visualisation.get_flow_meters()])

    def _render(self, surface: Surface) -> None:
        flow_meters = self._visualisation.get_flow_meters()
        if flow_meters is not None:
            for flow_meter in flow_meters:
                for cell in flow_meter.get_cells():
                    cell_rect = self._helper.get_rect_at(cell)
                    pygame.draw.rect(surface, (200, 200, 200), cell_rect, 1)
                    #self._render_text(surface, cell_rect, f"{flow_meter.get_name()}: {flow_meter.get_flow_rate()}", self._small_font_size)

