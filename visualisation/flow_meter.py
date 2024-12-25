from typing import TYPE_CHECKING

from serialization.serializable import Serializable

if TYPE_CHECKING:
    from simulation.core.cell import Cell
    from simulation.core.simulation import Simulation


class FlowMeter:
    def __init__(self, name: str, time_span: float, cells: 'list[Cell]'):
        self._name = name
        self._flow_rate = 0
        self._time_span: float = time_span
        self._cells: 'list[Cell]' = cells
        self._seen_pedestrians: dict[int, float] = {}

    def get_initial_data(self) -> dict[str, any]:
        return {
            "name": self._name,
            "time_span": self._time_span,
            "cells": [[cell.get_x(), cell.get_y()] for cell in self._cells],
        }

    def get_name(self) -> str:
        return self._name

    def get_flow_rate(self) -> float:
        return self._flow_rate

    def update(self, simulation: 'Simulation') -> None:
        for cell in self._cells:
            pedestrian = cell.get_pedestrian()
            if pedestrian is not None and pedestrian.get_id() not in self._seen_pedestrians:
                self._seen_pedestrians[pedestrian.get_id()] = simulation.get_run_time()

        pedestrians_in_timespan = sum(1 for time in self._seen_pedestrians.values() if simulation.get_run_time() - time <= self._time_span)
        self._flow_rate = pedestrians_in_timespan / self._time_span

    def get_cells(self) -> 'list[Cell]':
        return self._cells