from typing import Tuple

import pygame
from pygame.font import Font

from visualisation.visualisation_helper import VisualisationHelper


class Padding(Tuple[int, int, int, int]):
    def __new__(cls, top: int, right: int, bottom: int, left: int):
        return super().__new__(cls, (top, right, bottom, left))

    def get_left(self) -> int:
        return self[3]

    def get_right(self) -> int:
        return self[1]

    def get_top(self) -> int:
        return self[0]

    def get_bottom(self) -> int:
        return self[2]

    def get_horizontal(self) -> int:
        return self[1] + self[3]

    def get_vertical(self) -> int:
        return self[0] + self[2]


class Theme:
    def __init__(self, color: Tuple[int, int, int], hover_color: Tuple[int, int, int], active_color: Tuple[int, int, int], pressed_color: Tuple[int, int, int], foreground: Tuple[int, int, int], background: Tuple[int, int, int], font: Font = None, padding: Padding = None):
        self.color: Tuple[int, int, int] = color
        self.hover_color: Tuple[int, int, int] = hover_color
        self.active_color: Tuple[int, int, int] = active_color
        self.pressed_color: Tuple[int, int, int] = pressed_color
        self.foreground: Tuple[int, int, int] = foreground
        self.background: Tuple[int, int, int] = background
        pygame.font.init()
        self.font: Font = font or pygame.font.SysFont("Arial", 12)
        self.padding: Padding = padding or Padding(5, 5, 5, 5)

    @classmethod
    def create_theme(cls, base_color: Tuple[int, int, int], font: Font = None, padding: Padding = None) -> 'Theme':
        hsl = VisualisationHelper.rgb_to_hsl(base_color)
        if hsl[2] < 0.5:
            hover_color = VisualisationHelper.hsl_to_rgb((hsl[0], hsl[1] * 0.8, hsl[2] * 1.2))
            active_color = VisualisationHelper.hsl_to_rgb((hsl[0], hsl[1] * 0.7, hsl[2] * 1.3))
            pressed_color = VisualisationHelper.hsl_to_rgb((hsl[0], hsl[1] * 0.6, hsl[2] * 1.4))
            return cls(base_color, hover_color, active_color, pressed_color, (250, 250, 250), (20, 20, 20), font, padding)
        else:
            hover_color = VisualisationHelper.hsl_to_rgb((hsl[0], hsl[1] * 0.8, hsl[2] * 0.8))
            active_color = VisualisationHelper.hsl_to_rgb((hsl[0], hsl[1] * 0.7, hsl[2] * 0.7))
            pressed_color = VisualisationHelper.hsl_to_rgb((hsl[0], hsl[1] * 0.6, hsl[2] * 0.6))
            return cls(base_color, hover_color, active_color, pressed_color, (20, 20, 20), (250, 250, 250), font, padding)


DEFAULT_THEME = Theme.create_theme((100, 149, 237))
