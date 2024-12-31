from collections.abc import Callable
from typing import Tuple

import pygame
from pygame import Rect, Surface

from visualisation.theme import Theme, DEFAULT_THEME
from visualisation.visualisation_helper import VisualisationHelper


class Button:
    def __init__(self, min_size: Rect, text: str, theme: Theme = DEFAULT_THEME, action: Callable = None):
        self._min_size: Rect = min_size
        self._bounds: Rect = min_size.copy()
        self._theme: Theme = theme
        self._millis_since_pressed = 0
        self._action: Callable = action
        self._is_hovered = False
        self._text: str = None
        self._rendered_text: Surface = None
        self.set_text(text)

    def update(self, delta_time: float) -> None:
        if self._millis_since_pressed > 0:
            self._millis_since_pressed -= delta_time

    def is_pressed(self) -> bool:
        return self._millis_since_pressed > 0

    def press(self) -> None:
        self._millis_since_pressed = 250
        if self._action is not None:
            self._action()

    def is_hovered(self) -> bool:
        return self._is_hovered

    def set_hovered(self, hovered: bool) -> None:
        self._is_hovered = hovered

    def set_text(self, text: str) -> None:
        if text != self._text:
            self._rendered_text = VisualisationHelper.render_multiline_text_to_surface(self._theme.font, text, self._theme.foreground, True)
            #self._rendered_text = self._theme.font.render(text, True, self._theme.foreground)
            self._text = text
            self._bounds.update(self._bounds.left, self._bounds.top, max(self._min_size.width, self._rendered_text.get_width()) + self._theme.padding.get_horizontal(), max(self._min_size.height, self._rendered_text.get_height()) + self._theme.padding.get_vertical())

    def set_action(self, action) -> None:
        self._action = action

    def set_theme(self, theme: Theme) -> None:
        self._theme = theme

    def is_inside(self, x: int, y: int) -> bool:
        return self._bounds.collidepoint(x, y)

    def get_width(self) -> int:
        return self._bounds.width

    def get_height(self) -> int:
        return self._bounds.height

    def get_size(self) -> Tuple[int, int]:
        return self._bounds.width, self._bounds.height

    def set_position(self, x: int, y: int) -> None:
        self._bounds.update(x, y, self._bounds.width, self._bounds.height)

    def get_bounds(self) -> Rect:
        return self._bounds

    def render(self, surface) -> None:
        color = self._theme.pressed_color if self.is_pressed() else self._theme.hover_color if self.is_hovered() else self._theme.color
        pygame.draw.rect(surface, color, self._bounds)
        center = self._bounds.center
        text_pos = self._rendered_text.get_rect(center=center)
        surface.blit(self._rendered_text, text_pos)

