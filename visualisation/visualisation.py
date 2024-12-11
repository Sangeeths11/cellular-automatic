import math
from random import random
from typing import Tuple, Type, TypeVar

import pygame
from pygame import Color, Rect, Surface
from pygame.font import Font

from simulation.core.cell_state import CellState
from simulation.core.position import Position
from simulation.core.simulation import Simulation
from visualisation.button import Button
from visualisation.features.grid_visualisation_feature import GridVisualisationFeature
from visualisation.features.path_visualisation_feature import PathVisualisationFeature
from visualisation.features.pedestrian_visualisation_feature import PedestrianVisualisationFeature
from visualisation.features.simulation_info_visualisation_feature import SimulationInfoVisualisationFeature
from visualisation.features.spawner_visualisation_feature import SpawnerVisualisationFeature
from visualisation.features.target_heatmap_visualisation_feature import TargetHeatmapVisualisationFeature
from visualisation.features.target_visualisation_feature import TargetVisualisationFeature
from visualisation.shortcut import Shortcut
from visualisation.theme import Theme, DEFAULT_THEME
from visualisation.toggle_button import ToggleButton
from visualisation.visualisation_feature import VisualisationFeatureBase
from visualisation.visualisation_helper import VisualisationHelper


class Visualisation:
    GRID_OFFSET = 200

    def __init__(self, simulation: Simulation, cell_size: int | None = None, fps: float = 30):
        pygame.init()
        simulation.update(0) # Update simulation once to get the initial state
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
        self._font = pygame.font.SysFont("Arial", int(self._cell_size * 0.75))
        self._buttons: list[Button] = []
        self._click_theme = DEFAULT_THEME
        self._on_theme = Theme.create_theme((100, 250, 30))
        self._off_theme = Theme.create_theme((250, 30, 30))
        self._max_feature_width = 0
        self._simulation_delta = 0
        self._show_feature_details = self._screen.get_width() > 800
        self._show_buttons = True
        self._init_features()

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

    def add_shortcut(self, shortcut: Shortcut, add_button: bool = False, button_text: str = None, off_text: str = None):
        button_text = button_text or shortcut.get_text()
        self._shortcuts[shortcut.get_code()] = shortcut
        if add_button:
            if shortcut.is_toggle():
                button = ToggleButton(Rect(0, 0, 100, 35), button_text, off_text or button_text, shortcut.execute, self._on_theme, self._off_theme, shortcut.get_state)
                self._buttons.append(button)
            else:
                button = Button(Rect(0, 0, 100, 35), button_text, self._click_theme, shortcut.execute)
                self._buttons.append(button)

    def _init_features(self):
        heatmap = self.add_feature(TargetHeatmapVisualisationFeature(self.simulation, self, self._helper))
        spawner = self.add_feature(SpawnerVisualisationFeature(self.simulation, self, self._helper))
        target = self.add_feature(TargetVisualisationFeature(self.simulation, self, self._helper))
        grid = self.add_feature(GridVisualisationFeature(self.simulation, self, self._helper))
        path = self.add_feature(PathVisualisationFeature(self.simulation, self, self._helper))
        pedestrian = self.add_feature(PedestrianVisualisationFeature(self.simulation, self, self._helper))
        info = self.add_feature(SimulationInfoVisualisationFeature(self.simulation, self, self._helper), False)
        self.add_shortcut(Shortcut("Toggle heatmap", pygame.K_h, 0, heatmap.set_enabled, True, heatmap.is_enabled()), True, "Heatmap {0}")
        self.add_shortcut(Shortcut("Toggle spawner", pygame.K_s, 0, spawner.set_enabled, True, spawner.is_enabled()), True, "Spawners {0}")
        self.add_shortcut(Shortcut("Toggle target", pygame.K_t, 0, target.set_enabled, True, target.is_enabled()), True, "Targets {0}")
        self.add_shortcut(Shortcut("Toggle grid", pygame.K_g, 0, grid.set_enabled, True, grid.is_enabled()), True, "Grid {0}")
        self.add_shortcut(Shortcut("Toggle pedestrian", pygame.K_p, 0, pedestrian.set_enabled, True, pedestrian.is_enabled()), True, "Pedestrians {0}")
        self.add_shortcut(Shortcut("Toggle info", pygame.K_i, 0, info.set_enabled, True, info.is_enabled()), True, "Info {0}")
        self.add_shortcut(Shortcut("Toggle social distancing", pygame.K_d, 0, heatmap.set_social_distancing, True, heatmap.get_social_distancing()), True, "Social distancing\n{0}")
        self.add_shortcut(Shortcut("Toggle obstacle repulsion", pygame.K_o, 0, heatmap.set_obstacle_repulsion, True, heatmap.get_obstacle_repulsion()), True, "Obstacle repulsion\n{0}")
        self.add_shortcut(Shortcut("Toggle route", pygame.K_r, 0, path.set_enabled, True, path.is_enabled()), True, "Pathing {0}")
        self.add_shortcut(Shortcut("Toggle grid lines", pygame.K_l, 0, grid.set_show_lines, True, grid.get_show_lines()), True, "Grid lines\n{0}")
        self.add_shortcut(Shortcut("Show object names", pygame.K_n, 0, self._set_show_names, True, False), True, "Show names\n{0}")
        self.add_shortcut(Shortcut("Show pedestrian details", pygame.K_p, pygame.KMOD_LSHIFT, pedestrian.set_render_details, True, pedestrian.get_render_details()), True, "Pedestrian details\n{0}")
        self.add_shortcut(Shortcut("Show pedestrian target cell", pygame.K_p, pygame.KMOD_LCTRL, pedestrian.set_render_target_line, True, pedestrian.get_render_target_line()), True, "Pedestrian target\n{0}")
        self.add_shortcut(Shortcut("Pause", pygame.K_SPACE, 0, self.set_pause, True, self.is_paused()), True, "Unpause", "Pause")
        self.add_shortcut(Shortcut("Next target", pygame.K_RIGHT, 0, heatmap.next_target, False), True, "Next target\nheatmap")
        self.add_shortcut(Shortcut("Previous target", pygame.K_LEFT, 0, heatmap.previous_target, False), True, "Previous target\nheatmap")
        self.add_shortcut(Shortcut("Next pedestrian", pygame.K_DOWN, 0, path.next_pedestrian, False), True, "Next pedestrian")
        self.add_shortcut(Shortcut("Previous pedestrian", pygame.K_UP, 0, path.previous_pedestrian, False), True, "Previous pedestrian")

    def _set_show_names(self, state: bool) -> None:
        for feature in self._features:
            if hasattr(feature, "set_render_names"):
                feature.set_render_names(state)

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
                self._handle_key_event(event.key, event.mod)
            elif event.type == pygame.VIDEORESIZE:
                w, h = event.dict['size']
                self._handle_resize_event(w, h)
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_move_event(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click_event(event.button, event.pos[0], event.pos[1])

    def _handle_key_event(self, key: int, mod: int) -> None:
        # handle key press events, check for shortcuts
        code = Shortcut.calculate_code(key, mod)
        if code in self._shortcuts:
            self._shortcuts[code].execute()

    def _handle_resize_event(self, width: int, height: int) -> None:
        # handle window resize, recalculate cell size and update grid
        self._cell_size = self.calculate_cell_size(width, height)
        self._max_feature_width = 0
        pygame.display.update()
        self._show_feature_details = self._screen.get_width() > 800

    def _handle_mouse_move_event(self, x: int, y: int) -> None:
        # handles hover logic for buttons
        for button in self._buttons:
            button.set_hovered(button.is_inside(x, y))

    def _handle_click_event(self, button, click_x: int, click_y: int) -> None:
        # handles click in visualisation
        if button == 1:
            if click_y < Visualisation.GRID_OFFSET:
                if self._show_buttons:
                    self._handle_button_click(click_x, click_y)
            else:
                self._handle_grid_click(click_x, click_y)

    def _handle_button_click(self, click_x: int, click_y: int) -> None:
        # handle button click logic
        if self._show_buttons:
            for button in self._buttons:
                if button.is_inside(click_x, click_y):
                    button.press()

    def _handle_grid_click(self, click_x: int, click_y: int) -> None:
        # check for clicked targets and update selected target
        x, y = self._helper.screen_to_grid(click_x, click_y)
        heatmap = self.get_feature(TargetHeatmapVisualisationFeature)
        target = self.simulation.get_target(x, y)
        if heatmap is not None and target is not None:
            heatmap.set_target(target)
            heatmap.set_enabled(True)

        # check for clicked pedestrians and update selected pedestrian
        path = self.get_feature(PathVisualisationFeature)
        pedestrian = self.simulation.get_grid().get_cell(x, y).get_pedestrian()
        if path is not None and pedestrian is not None:
            path.set_pedestrian(pedestrian)
            path.set_enabled(True)


    def update(self, delta) -> None:
        # update simulation if not paused and bookkeep time delta
        if self.is_paused() is False and self.simulation.is_done() is False:
            self._simulation_delta += delta
            if self._simulation_delta >= self.simulation.get_time_resolution():
                self.simulation.update(self._simulation_delta)
                self._simulation_delta = 0


    def render_features(self, surface) -> None:
        # render all visualisation features and their status messages
        description_x = 0
        description_y = 0
        max_description_width = 0
        pygame.draw.rect(surface, (255, 255, 255), Rect(0, 0, surface.get_width(), Visualisation.GRID_OFFSET))
        for feature in self._features:
            feature.render(surface)

            if self._show_feature_details:
                # only render if the feature is enabled if buttons are not shown since buttons already cover this information
                texts, width, height = self._helper.get_multiline_texts(self._font, feature.describe_state(self._show_buttons == False), (0, 0, 0))
                if description_y + height > Visualisation.GRID_OFFSET:
                    description_x += max_description_width + 20
                    description_y = 0
                    max_description_width = 0

                for text in texts:
                    surface.blit(text, (description_x, description_y))
                    description_y += text.get_height()

                max_description_width = max(max_description_width, width)
                description_y += 20

        self._max_feature_width = max(description_x + max_description_width, self._max_feature_width)

    def render_buttons(self, dt, surface, x, y):
        max_width = 0
        for button in self._buttons:
            button.update(dt)
            if button.get_height() + y > Visualisation.GRID_OFFSET:
                x += max_width + 10
                max_width = 0
                y = 10

            button.set_position(x, y)
            button.render(surface)
            y += button.get_height() + 10
            max_width = max(max_width, button.get_width())

    def run(self):
        dt = 0.0
        while self._running:
            self.handle_events()
            self._screen.fill((40, 40, 40))
            self.update(dt / 1000)
            self.render_features(self._screen)
            if self._show_buttons:
                self.render_buttons(dt, self._screen, self._max_feature_width + 10, 10)
            pygame.display.flip()
            dt = self._clock.tick(self._fps)

        pygame.quit()
