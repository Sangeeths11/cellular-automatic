import math
from typing import Tuple, List

import numpy as np
from pygame import Color, Surface, Rect
from pygame.font import Font

from simulation.core.position import Position
import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from visualisation.visualisation import Visualisation


class VisualisationHelper:
    CURRENT_COLOR_ANGLE = 0

    def __init__(self, vis: 'Visualisation'):
        self._vis = vis

    def get_cell_size(self):
        return self._vis.get_cell_size()

    def get_grid_top_offset(self):
        return self._vis.GRID_OFFSET

    def get_grid_left_offset(self):
        return 0

    def _transform_offset(self, pos: Tuple) -> Tuple:
        return pos[0] + self.get_grid_left_offset(), pos[1] + self.get_grid_top_offset(), *pos[2:]

    @staticmethod
    def hsl_to_rgb(hsl: Tuple[float, float, float]) -> Tuple[int, int, int]:
        color = Color(0)
        color.hsla = np.clip(hsl[0], 0, 360), np.clip(hsl[1], 0, 100), np.clip(hsl[2], 0, 100), 100
        return color.r, color.g, color.b

    @staticmethod
    def rgb_to_hsl(color: Tuple[int, int, int]) -> Tuple[float, float, float]:
        color = Color(color)
        return color.hsla[0], color.hsla[1], color.hsla[2]

    @staticmethod
    def translate_polygon_result(func):
        def wrapper(*args):
            self = args[0]
            return [self._transform_offset(point) for point in func(*args)]

        return wrapper

    @staticmethod
    def translate_rect_result(func):
        def wrapper(*args):
            self = args[0]
            return self._transform_offset(func(*args))

        return wrapper

    @staticmethod
    def get_random_color() -> (int, int, int):
        angle = VisualisationHelper.CURRENT_COLOR_ANGLE
        VisualisationHelper.CURRENT_COLOR_ANGLE += 23
        color = Color(0)
        color.hsla = angle, 100, 50, 100
        return color.r, color.g, color.b

    @staticmethod
    def rotate(point: Tuple[float, float], origin: Tuple[float, float], angle: float) -> Tuple[float, float]:
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

    @staticmethod
    def mix_colors(color1, color2, ratio):
        return tuple(int(c1 * ratio + c2 * (1 - ratio)) for c1, c2 in zip(color1, color2))

    def screen_to_grid(self, x, y):
        return x // self.get_cell_size(), (y - self.get_grid_top_offset()) // self.get_cell_size()

    def get_rect_at(self, pos: Position) -> pygame.Rect:
        return self.get_rect(pos.get_x(), pos.get_y())

    @translate_rect_result
    def get_rect(self, x: int, y: int) -> pygame.Rect:
        cell_size = self.get_cell_size()
        return pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)

    @translate_rect_result
    def get_rect_with_size(self, x: int, y: int, width: int, height: int) -> pygame.Rect:
        cell_size = self.get_cell_size()
        return pygame.Rect(x * cell_size, y * cell_size, width * cell_size, height * cell_size)

    def get_small_rect_at(self, pos: Position) -> pygame.Rect:
        return self.get_small_rect(pos.get_x(), pos.get_y())

    @translate_rect_result
    def get_small_rect(self, x: int, y: int) -> pygame.Rect:
        cell_size = self.get_cell_size()
        cell_size_half = self.get_cell_size() // 2
        cell_size_fourth = self.get_cell_size() // 4
        return pygame.Rect(x * cell_size + cell_size_fourth, y * cell_size + cell_size_fourth, cell_size_half,
                           cell_size_half)

    def get_centered_pos_at(self, pos: Position) -> Tuple[int, int]:
        return self.get_centered_pos(pos.get_x(), pos.get_y())

    @translate_rect_result
    def get_centered_pos(self, x: int, y: int) -> Tuple[int, int]:
        cell_size = self.get_cell_size()
        cell_size_half = self.get_cell_size() // 2
        return x * cell_size + cell_size_half, y * cell_size + cell_size_half

    def get_x_center_pos_at(self, pos: Position, y_offset=0) -> Tuple[int, int]:
        return self.get_x_centered_pos(pos.get_x(), pos.get_y(), y_offset)

    @translate_rect_result
    def get_x_centered_pos(self, x: int, y: int, y_offset=0) -> Tuple[int, int]:
        cell_size = self.get_cell_size()
        cell_size_half = self.get_cell_size() // 2
        return x * cell_size + cell_size_half, y * cell_size + y_offset

    def get_y_centered_pos_at(self, pos: Position, x_offset=0):
        return self.get_y_centered_pos(pos.get_x(), pos.get_y(), x_offset)

    @translate_rect_result
    def get_y_centered_pos(self, x: int, y: int, x_offset=0) -> Tuple[int, int]:
        cell_size = self.get_cell_size()
        cell_size_half = self.get_cell_size() // 2
        return x * cell_size + x_offset, y * cell_size + cell_size_half

    def get_small_triangle_at(self, pos: Position, rotation: float = 0.0) -> List[Tuple[float, float]]:
        return self.get_small_triangle(pos.get_x(), pos.get_y(), rotation)

    @translate_polygon_result
    def get_small_triangle(self, x: int, y: int, rotation: float = 0.0) -> list[tuple[float, float]]:
        cell_size = self.get_cell_size()
        cell_half_size = cell_size // 2
        cell_fourth_size = cell_size // 4
        origin = (x * cell_size + cell_half_size, y * cell_size + cell_half_size)
        left = x * cell_size
        bottom = y * cell_size + cell_fourth_size + cell_half_size
        top = y * cell_size
        a = (left + cell_fourth_size, bottom)
        b = (left + cell_fourth_size + cell_half_size, bottom)
        c = (left + cell_half_size, top + cell_fourth_size)

        triangle = [a, b, c]
        return [VisualisationHelper.rotate(point, origin, rotation + math.pi / 2) for point in triangle]

    @translate_rect_result
    def get_top_left(self):
        return (0, 0)

    @staticmethod
    def get_multiline_texts(font: Font, text: str, color: Tuple) -> Tuple[list[Surface], int, int]:
        lines = text.split("\n")
        max_width = 0
        total_height = 0
        surfaces = []
        for line in lines:
            text = font.render(line, True, color)
            surfaces.append(text)
            total_height += text.get_height()
            max_width = max(max_width, text.get_width())

        return surfaces, max_width, total_height

    @staticmethod
    def render_multiline_text(surface: Surface, rect: Rect, font: Font, text: str, color: Tuple, center_x: bool = False, center_y: bool = False):
        lines, max_width, total_height = VisualisationHelper.get_multiline_texts(font, text, color)
        off_y = (rect.height - total_height) // 2 if center_y else 0
        for line in lines:
            off_x = (max_width - line.get_width()) // 2 if center_x else 0
            surface.blit(line, (rect.x + off_x, rect.y + off_y))
            off_y += line.get_height()

    @staticmethod
    def render_multiline_text_to_surface(font: Font, text: str, color: Tuple, center_x: bool = False) -> Surface:
        lines, max_width, total_height = VisualisationHelper.get_multiline_texts(font, text, color)
        surface = Surface((max_width, total_height), pygame.SRCALPHA)
        off_y = 0
        for line in lines:
            off_x = (max_width - line.get_width()) // 2 if center_x else 0
            surface.blit(line, (off_x, off_y))
            off_y += line.get_height()

        return surface