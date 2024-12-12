import json
from asyncio import gather

from serialization.serializable import Serializable
from simulation.core.simulation import Simulation
from utils import utils


class Serializer:
    def __init__(self, simulation: Simulation, file: str):
        self._simulation = simulation
        self._file = open(file, "w")
        self._initialize()
        pass

    def _initialize(self):
        grid = self.handle_serializable(self._simulation.get_grid())
        grid["neighbourhood"] = self._simulation.get_grid()._neighbourhood.__class__.__name__

        targets = [{
            "id": target.get_identifier(),
            "cells": [cell.get_identifier() for cell in target.get_cells()],
            "heatmap": utils.heatmap_to_base64(target.get_heatmap()),
        } for target in self._simulation.get_targets()]

        spawners = [{
            "id": spawner.get_identifier(),
            "cells": [cell.get_identifier() for cell in spawner.get_cells()],
            "spawn_delay": spawner._spawn_delay,
            "initial_delay": spawner._current_delay,
            "total_spawns": spawner._total_spawns,
            "batch_size": spawner._batch_size,
            "targeting_strategy": int(spawner._targeting_strategy),
            "targets": [target.get_identifier() for target in spawner._targets],
        } for spawner in self._simulation.get_spawners()]

        distancing = {
            "scale": self._simulation._distancing.get_scale(),
            "type": self._simulation._distancing.__class__.__name__,
        }

        simulation = {
            "time_resolution": self._simulation.get_time_resolution(),
            "grid": grid,
            "distancing": distancing,
            "targets": targets,
            "spawners": spawners,
            "social_distancing": {
                "width": self._simulation._social_distancing_generator._width,
                "height": self._simulation._social_distancing_generator._height,
            }
        }


        self._file.write(f'{{"setup": {json.dumps(simulation, indent=4)},\n"steps": [')

    def write_current_state(self):
        if self._file is None:
            return

        if self._simulation.is_done():
            self._file.write(json.dumps(self.handle_serializable(self._simulation)) + "]}")
            self._file.close()
            self._file = None
        else:
            self._file.write(json.dumps(self.handle_serializable(self._simulation)) + ",\n")


    def handle_dict(self, data: dict[str, any]) -> dict[str, any]:
        for key, value in data.items():
            if isinstance(value, Serializable):
                data[key] = self.handle_serializable(value)
            elif isinstance(value, list):
                data[key] = [self.handle_serializable(item) if isinstance(item, Serializable) else item for item in value]

        return data

    def handle_serializable(self, serializable: Serializable) -> dict[str, any]:
        data = serializable.get_serialization_data()
        return self.handle_dict(data)

    def serialize (self, data: Serializable) -> str:
        return json.dumps(self.handle_serializable(data), indent=4)