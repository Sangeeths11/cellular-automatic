from os import supports_fd

import pygame.font
from pygame import Surface

from visualisation.visualisation_feature import VisualisationFeatureBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.core.simulation import Simulation
    from visualisation.visualisation import Visualisation
    from visualisation.visualisation_helper import VisualisationHelper


class SimulationInfoVisualisationFeature(VisualisationFeatureBase):
    def __init__(self, sim: 'Simulation', vis: 'Visualisation', vis_helper: 'VisualisationHelper'):
        super().__init__(sim, vis, vis_helper)
        self._font_size = 20
        self._font = pygame.font.SysFont(self._font_name, self._helper.get_cell_size(), bold=True)

    def _describe_state(self) -> str:
        return f"Step: {self._simulation.get_steps()}\nTime: {self._simulation.get_run_time():.2f}s\nPedestrians: {len(self._simulation.get_pedestrians())}\nIs paused: {self._visualisation.is_paused()}"

    def _translate(self, pos: tuple[int, int], x: int, y: int) -> tuple[int, int]:
        return pos[0] + x, pos[1] + y

    def _next_line(self, pos: tuple[int, int]) -> tuple[int, int]:
        return pos[0], pos[1] + self._font_size

    def _render(self, surface: Surface) -> None:
        pos = self._translate(self._helper.get_top_left(), 10, 10)
        steps = self._font.render(f"Step: {self._simulation.get_steps()}", True, self._text_color)
        surface.blit(steps, pos)
        run_time = self._font.render(f"Time: {self._simulation.get_run_time():.2f}s", True, self._text_color)
        surface.blit(run_time, pos := self._translate(pos, 0, steps.get_height()))
        ped_count = self._font.render(f"Pedestrians: {len(self._simulation.get_pedestrians())}", True, self._text_color)
        surface.blit(ped_count, pos := self._translate(pos, 0, run_time.get_height()))
        paused = self._font.render(f"Is paused: {self._visualisation.is_paused()}", True, self._text_color)
        surface.blit(paused, pos := self._translate(pos, 0, ped_count.get_height()))
