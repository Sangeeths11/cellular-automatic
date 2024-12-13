import pygame
from pygame import Surface

from visualisation.visualisation_feature import VisualisationFeatureBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.core.simulation import Simulation
    from visualisation.visualisation import Visualisation
    from visualisation.visualisation_helper import VisualisationHelper


class WaypointVisualisationFeature(VisualisationFeatureBase):
    def __init__(self, sim: 'Simulation', vis: 'Visualisation', vis_helper: 'VisualisationHelper'):
        super().__init__(sim, vis, vis_helper)
        self._show_pedestrian_line = True

    def set_show_pedestrian_line(self, show_pedestrian_line: bool) -> None:
        self._show_pedestrian_line = show_pedestrian_line

    def get_show_pedestrian_line(self) -> bool:
        return self._show_pedestrian_line

    def _describe_state(self) -> str:
        pass

    def _render(self, surface: Surface) -> None:
        for waypoint in self._simulation.get_waypoints():
            color = (120, 30, 220)
            center_pos = self._helper.get_centered_pos_at(waypoint.get_cell())
            pygame.draw.circle(surface, color, center_pos, self._helper.get_cell_size() // 6)
            pygame.draw.circle(surface, color, center_pos, self._helper.get_cell_size() // 4, 3)

            if self._show_pedestrian_line:
                pedestrian = waypoint.get_pedestrian()
                if pedestrian is not None:
                    pygame.draw.line(surface, color, center_pos, self._helper.get_centered_pos_at(pedestrian), 3)


