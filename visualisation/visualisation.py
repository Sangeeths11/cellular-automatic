import math

import pygame
from simulation.core.cell_state import CellState
from simulation.core.position import Position
from simulation.core.simulation import Simulation


class Visualisation:
    GRID_OFFSET = 110

    def __init__(self, simulation: Simulation, cell_size: int = 80, fps: float = 30):
        pygame.init()
        self.screen = pygame.display.set_mode((simulation.get_grid().get_width() * cell_size,
                                               Visualisation.GRID_OFFSET + simulation.get_grid().get_height() * cell_size))
        pygame.display.set_caption("Simulation Visualisation")
        self.simulation = simulation
        self.cell_size = cell_size
        self.clock = pygame.time.Clock()
        self.running = True
        self._fps = fps
        self._max_heatmap_value = simulation._social_distancing_generator.get_max_value() + math.sqrt(
            simulation.get_grid().get_width() ** 2 + simulation.get_grid().get_height() ** 2)
        self._selected_target = None # simulation.get_targets()[0]
        self._include_social_distancing = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = self._screen_to_grid(*event.pos)
                    self._selected_target = self.simulation.get_target_at(x, y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self._include_social_distancing = not self._include_social_distancing

    def _mix_colors(self, color1, color2, ratio):
        return tuple(int(c1 * ratio + c2 * (1 - ratio)) for c1, c2 in zip(color1, color2))

    def _screen_to_grid(self, x, y):
        return x // self.cell_size, (y - Visualisation.GRID_OFFSET) // self.cell_size

    def _get_rect(self, pos: Position):
        return self._get_rect_at(pos.get_x(), pos.get_y())

    def _get_rect_at(self, x: int, y: int):
        return pygame.Rect(x * self.cell_size, y * self.cell_size + Visualisation.GRID_OFFSET, self.cell_size,
                           self.cell_size)

    def _get_small_rect(self, pos: Position):
        return pygame.Rect(pos.get_x() * self.cell_size + self.cell_size // 4,
                           pos.get_y() * self.cell_size + Visualisation.GRID_OFFSET + self.cell_size // 4,
                           self.cell_size // 2, self.cell_size // 2)

    def _get_center_pos_at(self, x: int, y: int):
        half_size = self.cell_size // 2
        return x * self.cell_size + half_size, y * self.cell_size + half_size + Visualisation.GRID_OFFSET

    def _get_center_pos(self, pos: Position):
        return self._get_center_pos_at(pos.get_x(), pos.get_y())

    def _get_x_center_pos(self, pos: Position, y_offset=0):
        return pos.get_x() * self.cell_size + self.cell_size // 2, pos.get_y() * self.cell_size + Visualisation.GRID_OFFSET + y_offset

    def render_grid(self):
        for x in range(self.simulation.get_grid().get_width()):
            for y in range(self.simulation.get_grid().get_height()):
                cell = self.simulation.get_grid().get_cell(x, y)
                cell_rect = self._get_rect(cell)
                if cell.get_state() == CellState.OBSTACLE:
                    pygame.draw.rect(self.screen, (0, 0, 0), cell_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), cell_rect, 1)

    def render_pedestrians(self):
        font = pygame.font.Font(None, 20)
        for pedestrian in self.simulation.get_pedestrians():
            rect = self._get_small_rect(pedestrian)
            pygame.draw.rect(self.screen, (0, 0, 255), rect)
            speed_info = font.render(f"[{pedestrian.get_id()}] {pedestrian.get_average_speed():.2f}m/s, {pedestrian.get_optimal_speed():.2f}m/s", True, (0, 0, 0))
            text_pos = self._get_x_center_pos(pedestrian, speed_info.get_height())
            self.screen.blit(speed_info, speed_info.get_rect(center=text_pos))


    def render_info(self):
        font = pygame.font.Font(None, 20)
        steps = font.render(f"Step: {self.simulation.get_steps()}", True, (0, 0, 0))
        self.screen.blit(steps, (10, 10))
        run_time = font.render(f"Time: {self.simulation.get_run_time():.2f}s", True, (0, 0, 0))
        self.screen.blit(run_time, (10, 30))
        ped_count = font.render(f"Pedestrians: {len(self.simulation.get_pedestrians())}", True, (0, 0, 0))
        self.screen.blit(ped_count, (10, 50))
        selected_target = font.render(f"Selected target: { self._selected_target.get_name() if self._selected_target is not None else 'None'}", True, (0, 0, 0))
        self.screen.blit(selected_target, (10, 70))
        social_distancing = font.render(f"Show Social distancing: {'On' if self._include_social_distancing else 'Off'}", True, (0, 0, 0))
        self.screen.blit(social_distancing, (10, 90))


    def render_spawners(self):
        half_size = self.cell_size // 2
        font = pygame.font.Font(None, 20)
        for spawner in self.simulation.get_spawners():
            name = font.render(spawner.get_name(), True, (0, 0, 0))
            for cell in spawner.get_cells():
                cell_rect = self._get_small_rect(cell)
                pygame.draw.rect(self.screen, (0, 255, 0), cell_rect)
                text_pos = self._get_x_center_pos(cell, name.get_height())
                self.screen.blit(name, name.get_rect(center=text_pos))

    def render_targets(self):
        half_size = self.cell_size // 2
        font = pygame.font.Font(None, 20)
        for target in self.simulation.get_targets():
            name = font.render(target.get_name(), True, (0, 0, 0))
            for cell in target.get_cells():
                cell_rect = self._get_small_rect(cell)
                pygame.draw.rect(self.screen, (255, 0, 0), cell_rect)
                text_pos = self._get_x_center_pos(cell, name.get_height())
                self.screen.blit(name, name.get_rect(center=text_pos))

    def render_heatmap(self):
        heatmap = self._selected_target.get_heatmap() if self._selected_target is not None else None
        font = pygame.font.Font(None, 20)
        social_distancing_heatmap = self.simulation.get_distancing_heatmap()

        for x in range(self.simulation.get_grid().get_width()):
            for y in range(self.simulation.get_grid().get_height()):
                value = heatmap.get_cell(x, y) if heatmap is not None else 0

                if self._include_social_distancing:
                    value += social_distancing_heatmap.get_cell(x, y)

                ratio = min(value, self._max_heatmap_value) / self._max_heatmap_value
                color = self._mix_colors((255, 200, 0), (0, 100, 255), ratio)
                rect = self._get_rect_at(x, y)
                pygame.draw.rect(self.screen, color, rect)
                value_text = font.render(f"{value:.2f}", True, (40, 40, 40))
                text_pos = self._get_center_pos_at(x, y)
                self.screen.blit(value_text, value_text.get_rect(center=text_pos))

    def update(self, delta):
        if self.simulation.is_done() is False:
            self.simulation.update(delta)

    def run(self):
        dt = 0.0
        while self.running:
            self.handle_events()
            self.screen.fill((255, 255, 255))
            self.update(dt / 1000)
            self.render_info()
            self.render_heatmap()
            self.render_grid()
            self.render_spawners()
            self.render_targets()
            self.render_pedestrians()
            pygame.display.flip()
            dt = self.clock.tick(self._fps)

        pygame.quit()
