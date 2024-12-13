from typing import Iterable

from exceptions.simulation_error import SimulationError
from exceptions.simulation_error_codes import SimulationErrorCode
from simulation.core.cell_state import CellState
from simulation.heatmaps.djisktra_heatmap_generator import DijkstraHeatmapGenerator
from utils.utils import none_check

from simulation.core.cell import Cell
from simulation.core.cell_state import CellState
from simulation.core.position import Position
from simulation.core.spawner import Spawner
from simulation.core.target import Target
from simulation.core.waypoint import Waypoint
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.heatmaps.djisktra_heatmap_generator import DijkstraHeatmapGenerator
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.heatmap_generator_base import HeatmapGeneratorBase
from simulation.heatmaps.pathfinding_queue import PathfindingQueue
from simulation.heatmaps.social_distancing_heatmap_generator import SocialDistancingHeatmapGenerator
from simulation.neighbourhood.base_neighbourhood import NeighbourhoodBase
from simulation.core.pedestrian import Pedestrian
from simulation.core.simulation_grid import SimulationGrid
from utils.immutable_list import ImmutableList
from utils.utils import none_check

class Simulation(Serializable):
    def __init__(self, time_resolution: float, grid: SimulationGrid, distancing: DistanceBase,
                 social_distancing: SocialDistancingHeatmapGenerator, targets: list[Target], spawners: list[Spawner],
                 occupation_bias_modifier: float | None = 1.0, retargeting_threshold: float | None = -1.0, waypoint_threshold: float | None = None, waypoint_distance: int | None = None, waypoint_heatmap_generator: HeatmapGeneratorBase | None = None):
        self._pedestrians: list[Pedestrian] = list()
        self._grid: SimulationGrid = grid
        self._targets: list[Target] = targets
        self._spawners: list[Spawner] = spawners
        self._social_distancing_generator: SocialDistancingHeatmapGenerator = social_distancing
        self._distancing_heatmap: Heatmap = None
        self._distancing = distancing
        self._steps: int = 0
        self._run_time: float = 0
        self._time_resolution: float = time_resolution
        self._occupation_bias_modifier: float | None = occupation_bias_modifier
        self._retargeting_threshold: float | None = retargeting_threshold
        self._waypoint_threshold: float | None = waypoint_threshold
        self._waypoint_distance: int | None = waypoint_distance
        self._waypoint_heatmap_generator: HeatmapGeneratorBase | None = waypoint_heatmap_generator
        self._waypoints: list[Waypoint] = []
        self._waypoint_pathfinding_heatmap_generator: DijkstraHeatmapGenerator = DijkstraHeatmapGenerator(distancing, {CellState.OBSTACLE, CellState.OCCUPIED})

        waypoint_none, none_fields = none_check(waypoint_threshold=waypoint_threshold, waypoint_distance=waypoint_distance, waypoint_heatmap_generator=waypoint_heatmap_generator)
        if waypoint_none is False:
            raise SimulationError(SimulationErrorCode.VALUE_NOT_INITIALIZED, {"parameters": none_fields})

    def get_waypoints(self) -> ImmutableList[Waypoint]:
        return ImmutableList(self._waypoints)

    def get_time_resolution(self) -> float:
        return self._time_resolution

    def get_spawners(self) -> ImmutableList[Spawner]:
        return ImmutableList(self._spawners)

    def get_targets(self) -> ImmutableList[Target]:
        return ImmutableList(self._targets)

    def get_grid(self) -> SimulationGrid:
        return self._grid

    def get_max_grid_distance(self):
        max_point = Position(self.get_grid().get_width(), self.get_grid().get_height())
        min_point = Position(0, 0)
        return self._distancing.calculate_distance(min_point, max_point)

    def get_distancing_heatmap(self) -> Heatmap:
        return self._distancing_heatmap

    def get_target(self, x: int, y: int) -> Target | None:
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
        self._update_waypoints()
        self._update_pedestrians(delta)
        self._steps += 1
        self._run_time += delta

    def _remove_waypoint(self, waypoint: Waypoint):
        waypoint.get_pedestrian().clear_waypoint()
        self._waypoints.remove(waypoint)

    def _create_waypoint(self, cell: Cell, pedestrian: Pedestrian):
        waypoint = Waypoint(self._waypoint_heatmap_generator, self._grid, cell, pedestrian)
        self._waypoints.append(waypoint)
        pedestrian.set_waypoint(waypoint)

    def _remove_pedestrian(self, pedestrian: Pedestrian):
        self._pedestrians.remove(pedestrian)
        cell = self._grid.get_cell_at_pos(pedestrian)
        cell.remove_pedestrian()
        pedestrian.set_reached_target()

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

    def _get_cell_value(self, last_pos: Position, cell: Cell, heatmap: Heatmap) -> float:
        value = heatmap.get_cell_at_pos(cell)
        value += min(0, self._distancing_heatmap.get_cell_at_pos(cell) - self._social_distancing_generator.get_bias(last_pos, cell))
        if self._occupation_bias_modifier is not None:
            value += (self._occupation_bias_modifier * cell.get_pedestrian().get_occupation_bias()) if cell.is_occupied() else 0

        return value

    def _get_next_target_cell(self, heatmap: Heatmap, pos: Position, last_pos: Position) -> Cell | None:
        neighbours = self._grid.get_neighbours_at(pos)
        for cell in sorted(neighbours, key=lambda n: self._get_cell_value(last_pos, n, heatmap)):
            if self._occupation_bias_modifier is not None or cell.is_free():
                return cell

        return None

    def _get_next_pedestrian_target(self, pedestrian: Pedestrian, last_pos: Position) -> Cell | None:
        if pedestrian.is_inside_target():
            self._remove_pedestrian(pedestrian)
            return None
        elif pedestrian.has_waypoint():
            return pedestrian.get_waypoint().next_cell(pedestrian)
        else:
            return self._get_next_target_cell(pedestrian.get_target().get_heatmap(), pedestrian, last_pos)

    def _find_waypoint(self, cell: Cell, target: Iterable[Cell], depth: int = 10) -> Cell | None:
        heatmap = self._waypoint_pathfinding_heatmap_generator.generate_heatmap(target, self._grid)
        queue = PathfindingQueue()
        queue.push(cell, heatmap.get_cell_at_pos(cell))
        current: Cell = cell
        while depth > 0 and not queue.is_empty():
            current = queue.pop()
            for neighbour in self._grid.get_neighbours_at(current):
                if neighbour in queue:
                    continue

                if neighbour.is_free():
                    queue.push(neighbour, heatmap.get_cell_at_pos(neighbour))
                else:
                    queue.mark_visited(neighbour)

            depth -= 1

        return None if cell.pos_equals(current) else (current if queue.is_empty() else queue.pop())

    def _update_pedestrians(self, delta: float):
        for pedestrian in sorted(self._pedestrians, key=lambda p: p.get_current_distance()):
            pedestrian.update(delta)

            if pedestrian.has_reached_waypoint():
                self._remove_waypoint(pedestrian.get_waypoint())

            if pedestrian.can_move():
                cell = self._grid.get_cell_at_pos(pedestrian)
                cell.remove_pedestrian()
                pedestrian.move()
                pedestrian.get_targeted_cell().set_pedestrian(pedestrian)
                new_target_cell = self._get_next_pedestrian_target(pedestrian, cell)
                pedestrian.set_target_cell(new_target_cell)

            elif pedestrian.has_targeted_cell() is False:
                new_target_cell = self._get_next_pedestrian_target(pedestrian, pedestrian)
                pedestrian.set_target_cell(new_target_cell)
            elif (pedestrian.get_targeted_cell().is_occupied() and
                  self._retargeting_threshold is not None and
                  self._retargeting_threshold > pedestrian.get_current_distance() and
                  (new_target_cell := self._get_next_pedestrian_target(pedestrian, pedestrian)) and
                  new_target_cell is not None and
                  new_target_cell.is_free()):

                pedestrian.set_target_cell(new_target_cell)
            elif (pedestrian.has_waypoint() is False and
                  self._waypoint_threshold is not None and
                  self._waypoint_threshold > pedestrian.get_current_distance() and
                  (waypoint_target := self._find_waypoint(self._grid.get_cell_at_pos(pedestrian), pedestrian.get_target().get_cells())) is not None):

                self._create_waypoint(waypoint_target, pedestrian)
            else:
                pass
                # pedestrian is stuck, do nothing



    def _update_waypoints(self):
        for waypoint in self._waypoints:
            waypoint.update()

    def get_serialization_data(self) -> dict[str, any]:
        return {
            "run_time": self._run_time,
            "step": self._steps,
            "pedestrians": self._pedestrians,
            "targets": self._targets,
            "spawners": self._spawners,
            "waypoints": self._waypoints,
            "social_distancing_heatmap": utils.utils.heatmap_to_base64(self._distancing_heatmap),
        }

    def get_identifier(self) -> str:
        return "simulation"