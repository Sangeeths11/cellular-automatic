import math
from random import random
from typing import Tuple, Type, TypeVar

import pygame
from pygame import Color, Rect, Surface
from pygame.font import Font

from simulation.core.cell_state import CellState
from simulation.core.position import Position
from simulation.core.simulation import Simulation
from visualisation.features.grid_visualisation_feature import GridVisualisationFeature
from visualisation.features.path_visualisation_feature import PathVisualisationFeature
from visualisation.features.pedestrian_visualisation_feature import PedestrianVisualisationFeature
from visualisation.features.simulation_info_visualisation_feature import SimulationInfoVisualisationFeature
from visualisation.features.spawner_visualisation_feature import SpawnerVisualisationFeature
from visualisation.features.target_heatmap_visualisation_feature import TargetHeatmapVisualisationFeature
from visualisation.features.target_visualisation_feature import TargetVisualisationFeature
from visualisation.shortcut import Shortcut
from visualisation.visualisation_feature import VisualisationFeatureBase
from visualisation.visualisation_helper import VisualisationHelper


class Visualisation:
    GRID_OFFSET = 200

    def __init__(self, simulation: Simulation, cell_size: int | None = None, fps: float = 30):
        pygame.init()
        self.simulation = simulation
        if cell_size is None:
            info = pygame.display.Info()
            w, h = info.current_w, info.current_h
            cell_size = math.ceil(self.calculate_cell_size(w, h) * 0.9)

        self._cell_size: int = cell_size
        self._screen = pygame.display.set_mode((simulation.get_grid().get_width() * cell_size, Visualisation.GRID_OFFSET + simulation.get_grid().get_height() * cell_size), pygame.RESIZABLE)
        pygame.display.set_caption("Simulation Visualisation")
        self._clock = pygame.time.Clock()
        self._is_paused = False
        self._running = True
        self._fps = fps
        self._spawner_colors = {spawner: VisualisationHelper.get_random_color() for spawner in simulation.get_spawners()}
        self._target_colors = {target: VisualisationHelper.get_random_color() for target in simulation.get_targets()}
        self._helper = VisualisationHelper(self)
        self._shortcuts: dict[int, Shortcut] = {}
        self._features: list[VisualisationFeatureBase] = []
        self._init_features()
        self._font = pygame.font.SysFont("Arial", 20)

    TFeature = TypeVar('TFeature', bound=VisualisationFeatureBase)

    def get_cell_size(self) -> int:
        return self._cell_size

    def is_paused(self) -> bool:
        return self._is_paused

    def set_pause(self, pause: bool) -> None:
        self._is_paused = pause

    def calculate_cell_size(self, width: int, height: int) -> int:
        return min(width // self.simulation.get_grid().get_width(), (height - Visualisation.GRID_OFFSET) // self.simulation.get_grid().get_height())


    def get_feature(self, type: Type[TFeature]) -> TFeature | None:
        for feature in self._features:
            if isinstance(feature, type):
                return feature

        return None

    def add_feature[T](self, feature: T, enabled: bool = True) -> T:
        self._features.append(feature)
        feature.set_enabled(enabled)
        return feature

    def add_shortcut(self, shortcut: Shortcut):
        self._shortcuts[shortcut.get_code()] = shortcut

    def _init_features(self):
        heatmap = self.add_feature(TargetHeatmapVisualisationFeature(self.simulation, self, self._helper))
        spawner = self.add_feature(SpawnerVisualisationFeature(self.simulation, self, self._helper))
        target = self.add_feature(TargetVisualisationFeature(self.simulation, self, self._helper))
        grid = self.add_feature(GridVisualisationFeature(self.simulation, self, self._helper))
        path = self.add_feature(PathVisualisationFeature(self.simulation, self, self._helper))
        pedestrian = self.add_feature(PedestrianVisualisationFeature(self.simulation, self, self._helper))
        info = self.add_feature(SimulationInfoVisualisationFeature(self.simulation, self, self._helper))
        self.add_shortcut(Shortcut("Toggle heatmap", pygame.K_h, 0, heatmap.set_enabled, True, heatmap.is_enabled()))
        self.add_shortcut(Shortcut("Toggle spawner", pygame.K_s, 0, spawner.set_enabled, True, spawner.is_enabled()))
        self.add_shortcut(Shortcut("Toggle target", pygame.K_t, 0, target.set_enabled, True, target.is_enabled()))
        self.add_shortcut(Shortcut("Toggle grid", pygame.K_g, 0, grid.set_enabled, True, grid.is_enabled()))
        self.add_shortcut(Shortcut("Toggle pedestrian", pygame.K_p, 0, pedestrian.set_enabled, True, pedestrian.is_enabled()))
        self.add_shortcut(Shortcut("Toggle info", pygame.K_i, 0, info.set_enabled, True, info.is_enabled()))
        self.add_shortcut(Shortcut("Toggle social distancing", pygame.K_d, 0, heatmap.set_social_distancing, True, heatmap.get_social_distancing()))
        self.add_shortcut(Shortcut("Toggle route", pygame.K_r, 0, path.set_enabled, True, path.is_enabled()))
        self.add_shortcut(Shortcut("Toggle grid lines", pygame.K_l, 0, grid.set_show_lines, True, grid.get_show_lines()))
        self.add_shortcut(Shortcut("Pause", pygame.K_SPACE, 0, self.set_pause, True, self.is_paused()))
        self.add_shortcut(Shortcut("Next target", pygame.K_RIGHT, 0, heatmap.next_target, False))
        self.add_shortcut(Shortcut("Previous target", pygame.K_LEFT, 0, heatmap.previous_target, False))
        self.add_shortcut(Shortcut("Next pedestrian", pygame.K_DOWN, 0, path.next_pedestrian, False))
        self.add_shortcut(Shortcut("Previous pedestrian", pygame.K_UP, 0, path.previous_pedestrian, False))

    def get_target_color(self, target):
        return self._target_colors[target]

    def get_spawner_color(self, spawner):
        return self._spawner_colors[spawner]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self._running = False

            if event.type == pygame.KEYDOWN:
                code = Shortcut.calculate_code(event.key, event.mod)
                if code in self._shortcuts:
                    self._shortcuts[code].execute()

            elif event.type == pygame.VIDEORESIZE:
                w, h = event.dict['size']
                self._cell_size = self.calculate_cell_size(w, h)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = self._helper.screen_to_grid(*event.pos)
                    heatmap = self.get_feature(TargetHeatmapVisualisationFeature)
                    target = self.simulation.get_target(x, y)
                    if heatmap is not None and target is not None:
                        heatmap.set_target(target)
                        heatmap.set_enabled(True)

                    path = self.get_feature(PathVisualisationFeature)
                    pedestrian = self.simulation.get_grid().get_cell(x, y).get_pedestrian()
                    if path is not None and pedestrian is not None:
                        path.set_pedestrian(pedestrian)
                        path.set_enabled(True)



    def update(self, delta):
        if self.is_paused() is False and self.simulation.is_done() is False:
            self.simulation.update(delta)

    def get_multiline_texts(self, font: Font, text: str, color: Tuple) -> Tuple[list[Surface], int, int]:
        lines = text.split("\n")
        max_width = 0
        total_height = 0
        surfaces = []
        for i, line in enumerate(lines):
            text = font.render(line, True, color)
            surfaces.append(text)
            total_height += text.get_height()
            max_width = max(max_width, text.get_width())

        return surfaces, max_width, total_height

    def render_features(self, surface):
        description_x = 0
        description_y = 0
        max_description_width = 0
        pygame.draw.rect(surface, (255, 255, 255), Rect(0, 0, surface.get_width(), Visualisation.GRID_OFFSET))
        for feature in self._features:
            feature.render(surface)
            texts, width, height = self.get_multiline_texts(self._font, feature.describe_state(), (0, 0, 0))
            if description_y + height > Visualisation.GRID_OFFSET:
                description_x += max_description_width + 20
                description_y = 0
                max_description_width = 0

            for text in texts:
                surface.blit(text, (description_x, description_y))
                description_y += text.get_height()

            max_description_width = max(max_description_width, width)
            description_y += 20

    def run(self):
        dt = 0.0
        while self._running:
            self.handle_events()
            self._screen.fill((40, 40, 40))
            self.update(dt / 1000)
            self.render_features(self._screen)
            pygame.display.flip()
            dt = self._clock.tick(self._fps)

        pygame.quit()
