from simulation.core.cell import Cell
from simulation.core.spawner import Spawner
from simulation.core.target import Target
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.heatmap_generator_base import HeatmapGeneratorBase
from simulation.heatmaps.social_distancing_heatmap import SocialDistancingHeatmapGenerator
from simulation.neighbourhood.base_neighbourhood import NeighbourhoodBase
from simulation.core.pedestrian import Pedestrian
from simulation.core.simulation_grid import SimulationGrid
from utils.immutable_list import ImmutableList


class Simulation:
    def __init__(self, time_resolution: float, grid: SimulationGrid, distancing: DistanceBase, social_distancing: SocialDistancingHeatmapGenerator, targets: list[Target], spawners: list[Spawner]):
        self._pedestrians: list[Pedestrian] = list()
        self._grid: SimulationGrid = grid
        self._targets: list[Target] = targets
        self._spawners: list[Spawner] = spawners
        self._social_distancing_generator: SocialDistancingHeatmapGenerator = social_distancing
        self._distancing_heatmap: Heatmap = None
        self._steps: int = 0
        self._run_time: float = 0
        self._time_resolution: float = time_resolution

    def get_spawners(self) -> ImmutableList[Spawner]:
        return ImmutableList(self._spawners)

    def get_targets(self) -> ImmutableList[Target]:
        return ImmutableList(self._targets)

    def get_grid(self) -> SimulationGrid:
        return self._grid

    def get_distancing_heatmap(self) -> Heatmap:
        return self._distancing_heatmap

    def get_target_at(self, x: int, y: int) -> Target | None:
        for target in self._targets:
            if target.is_coordinate_inside_target(x, y):
                return target
        return None

    def get_pedestrians(self) -> ImmutableList[Pedestrian]:
        return ImmutableList(self._pedestrians)

    def get_steps(self) -> int:
        return self._steps

    def get_run_time(self) -> float:
        return self._run_time

    def is_done(self) -> bool:
        return all(spawner.is_done() for spawner in self._spawners) and len(self._pedestrians) == 0

    def update(self, delta: float = None):
        delta = delta or self._time_resolution
        self._update_spawners(delta)
        self._update_distancing_heatmap()
        self._update_targets()
        self._update_pedestrians(delta)
        self._steps += 1
        self._run_time += delta

    def _remove_pedestrian(self, pedestrian: Pedestrian):
        self._pedestrians.remove(pedestrian)
        cell = self._grid.get_cell_at_pos(pedestrian)
        cell.remove_pedestrian()

    def _add_pedestrian(self, pedestrian: Pedestrian):
        cell = self._grid.get_cell_at_pos(pedestrian)
        cell.set_pedestrian(pedestrian)
        self._pedestrians.append(pedestrian)

    def _update_spawners(self, delta: float):
        for spawner in self._spawners:
            for pedestrian in spawner.update(delta):
                self._add_pedestrian(pedestrian)

    def _update_distancing_heatmap(self):
        pedestrian_cells = [self._grid.get_cell_at_pos(pedestrian) for pedestrian in self._pedestrians]
        self._distancing_heatmap = self._social_distancing_generator.generate_heatmap(pedestrian_cells,
                                                                                      self._grid)

    def _update_targets(self):
        for target in self._targets:
            target.update_heatmap()

    def _get_pedestrian_target_cell(self, pedestrian: Pedestrian) -> Cell | None:
        if pedestrian.is_inside_target():
            pedestrian.get_target().increment_exit_count()
            self._remove_pedestrian(pedestrian)
            return None
        else:
            heatmap = pedestrian.get_heatmap()
            neighbours = self._grid.get_neighbours_at(pedestrian)

            # TODO: move lambda to separate function
            # TODO: instead of ignoring occupied cells, try to add a penalty to them
            for cell in sorted(neighbours, key=lambda n: heatmap.get_cell_at_pos(n) + self._distancing_heatmap.get_cell_at_pos(n) - self._social_distancing_generator.get_bias(pedestrian, n)):
                if cell.is_free():
                    return cell

            return None

    def _update_pedestrians(self, delta: float):
        for pedestrian in sorted(self._pedestrians, key=lambda p: p.get_current_distance()):
            pedestrian.update(delta)
            if pedestrian.can_move():
                cell = self._grid.get_cell_at_pos(pedestrian)
                cell.remove_pedestrian()
                pedestrian.move()
                new_target_cell = self._get_pedestrian_target_cell(pedestrian)
                pedestrian.set_target_cell(new_target_cell)
            elif pedestrian.has_target() is False:
                new_target_cell = self._get_pedestrian_target_cell(pedestrian)
                pedestrian.set_target_cell(new_target_cell)

