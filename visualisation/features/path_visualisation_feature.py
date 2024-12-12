import pygame.draw
from pygame import Surface

from simulation.core.position import Position
from visualisation.visualisation_feature import VisualisationFeatureBase

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.core.pedestrian import Pedestrian
    from simulation.core.simulation import Simulation
    from visualisation.visualisation import Visualisation
    from visualisation.visualisation_helper import VisualisationHelper


class PathVisualisationFeature(VisualisationFeatureBase):
    def __init__(self, sim: 'Simulation', vis: 'Visualisation', vis_helper: 'VisualisationHelper'):
        super().__init__(sim, vis, vis_helper)
        self._selected_pedestrian: Pedestrian = None
        self._selected_pedestrian_index = 0

    def next_pedestrian(self):
        pedestrians = self._simulation.get_pedestrians()
        self._selected_pedestrian_index = (self._selected_pedestrian_index + 1) % (len(pedestrians) + 1)
        self._selected_pedestrian = None if self._selected_pedestrian_index == 0 else pedestrians[self._selected_pedestrian_index - 1]

    def previous_pedestrian(self):
        pedestrians = self._simulation.get_pedestrians()
        self._selected_pedestrian_index = (self._selected_pedestrian_index - 1) % (len(pedestrians) + 1)
        self._selected_pedestrian = None if self._selected_pedestrian_index == 0 else pedestrians[self._selected_pedestrian_index - 1]

    def set_pedestrian(self, pedestrian: 'Pedestrian|None'):
        if pedestrian is None:
            self._selected_pedestrian_index = 0
            self._selected_pedestrian = None
        else:
            self._selected_pedestrian_index = self._simulation.get_pedestrians().index(pedestrian) + 1
            self._selected_pedestrian = pedestrian

    def _describe_state(self) -> str:
        return f"Selected pedestrian: {'None' if self._selected_pedestrian is None else self._selected_pedestrian.get_id()}"

    def _render(self, surface: Surface) -> None:
        if self._selected_pedestrian is not None:
            if self._selected_pedestrian.has_reached_target():
                self.set_pedestrian(None)
                return

            origin = self._helper.get_centered_pos_at(self._selected_pedestrian)
            pygame.draw.circle(surface, (255, 255, 255), origin, self._helper.get_cell_size() // 2, 2)
            heatmap = self._selected_pedestrian.get_heatmap()
            last_pos: Position = self._selected_pedestrian
            visited: set[Position] = set()
            visited.add(last_pos)
            while last_pos is not None:
                next_pos: Position = self._simulation._get_next_target_cell(heatmap, last_pos, last_pos)
                if next_pos is None or next_pos in visited:
                    break

                pygame.draw.line(surface, (255, 255, 255), self._helper.get_centered_pos_at(last_pos), self._helper.get_centered_pos_at(next_pos), 3)
                if self._selected_pedestrian.get_target().is_inside_target(next_pos):
                    break

                visited.add(next_pos)
                last_pos = next_pos
