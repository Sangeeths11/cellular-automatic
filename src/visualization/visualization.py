import pygame
import numpy as np
from enum import Enum
from src.enums.tileStatus import TileStatus

class Visualization:
    def __init__(self, data, tile_size=80, fps=5):
        pygame.init()
        self.data = data
        self.time_steps, self.length, self.width = data.shape
        self.tile_size = tile_size
        self.screen = pygame.display.set_mode((self.width * tile_size, self.length * tile_size))
        pygame.display.set_caption("Cellular Automaton: Crowd Flow")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_time = 0
        self.fps = fps
        self.colors = {
            TileStatus.FREE: (255, 255, 255),  # white
            TileStatus.BLOCKED: (0, 0, 0),    # black
            TileStatus.PEDESTRIAN: (0, 0, 255),  # blue
            TileStatus.SOURCE: (0, 255, 0),   # green
            TileStatus.DESTINATION: (255, 0, 0)  # red
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw_grid(self):
        for y in range(self.length):
            for x in range(self.width):
                value = self.data[self.current_time, y, x]
                color = self.colors.get(TileStatus(value), (128, 128, 128))
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                )
                pygame.draw.rect(
                    self.screen,
                    (200, 200, 200),
                    pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size),
                    1  # Edge thickness
                )

    def update(self):
        self.current_time += 1
        if self.current_time >= self.time_steps:
            self.running = False

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            pygame.display.flip()
            self.update()
            self.clock.tick(self.fps)

        pygame.quit()