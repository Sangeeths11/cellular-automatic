from collections.abc import Callable

from pygame import Rect

from visualisation.button import Button
from visualisation.theme import Theme


class ToggleButton(Button):
    def __init__(self, min_size: Rect, on_format: str, off_format: str, action: Callable, on_theme: Theme, off_theme: Theme, state_getter: Callable[[],bool]):
        super().__init__(min_size, "", on_theme, action)
        self._on_theme = on_theme
        self._off_theme = off_theme
        self._state_getter: Callable[[], bool] = state_getter
        self._on_format = on_format
        self._off_format = off_format
        self._last_state = None
        self._update_state()

    def _update_state(self) -> None:
        state = self._state_getter()
        if state != self._last_state:
            self._last_state = state
            self._theme = self._on_theme if state else self._off_theme
            self.set_text((self._on_format if state else self._off_format).format("On" if state else "Off"))

    def update(self, delta: float) -> None:
        super().update(delta)
        self._update_state()

    def press(self) -> None:
        super().press()
        self._update_state()