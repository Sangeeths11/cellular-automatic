from abc import ABC, abstractmethod
from typing import Type

from pygame import Surface

from typing import TYPE_CHECKING
from visualisation.visualisation_helper import VisualisationHelper

if TYPE_CHECKING:
    from simulation.core.simulation import Simulation
    from visualisation.visualisation import Visualisation



class VisualisationFeatureBase(ABC):
    """
    Base class for visualisation features. Visualisation features are used to generate visualisations based on the given grid
    :param sim: the simulation the visualisation should be generated for
    """
    def __init__(self, sim: 'Simulation', vis: 'Visualisation', vis_helper: VisualisationHelper):
        self._is_enabled = False
        self._simulation = sim
        self._visualisation = vis
        self._helper: VisualisationHelper = vis_helper
        self._text_color = (255, 255, 255)
        self._font_name = "Arial"
        self._mono_font_name = "Consolas"
        self._small_font_size = min(int(self._helper.get_cell_size() * 0.35), 12)
        self._font_size = min(int(self._helper.get_cell_size() * 0.75), 18)
        pass

    def enable(self) -> None:
        """
        Enables the visualisation feature
        """
        self._is_enabled = True

    def disable(self) -> None:
        """
        Disables the visualisation feature
        """
        self._is_enabled = False

    def set_enabled(self, enabled: bool) -> None:
        """
        Sets the state of the visualisation feature
        :param enabled: the state of the visualisation feature
        """
        self._is_enabled = enabled

    def is_enabled(self) -> bool:
        """
        Returns whether the visualisation feature is enabled
        :return: whether the visualisation feature is enabled
        """
        return self._is_enabled

    def render(self, surface: Surface) -> None:
        """
        Generates visualisation based on the given grid
        :param surface: the surface the visualisation should be rendered onto
        """
        if self.is_enabled():
            self._render(surface)

    def describe_state(self, include_enabled: bool = True) -> str:
        """
        Describes the state of the visualisation feature
        :param include_enabled: whether to include if the feature is enabled in the description as the first line
        :return: a string describing the state of the visualisation feature
        """
        description = f"{self.__class__.__name__} is enabled: {self.is_enabled()}" if include_enabled else self.__class__.__name__
        state_description = self._describe_state()
        if state_description:
            description += f"\n{state_description}"

        return description

    @abstractmethod
    def _describe_state(self) -> str:
        """
        Describes the state of the visualisation feature
        :return: a string describing the state of the visualisation feature
        """
        pass

    @abstractmethod
    def _render(self, surface: Surface) -> None:
        pass