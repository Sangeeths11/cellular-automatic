from simulation.core.cell import Cell
from simulation.core.position import Position
from simulation.core.spawner import Spawner
from simulation.core.target import Target
from simulation.heatmaps.distancing.base_distance import DistanceBase
from simulation.heatmaps.heatmap import Heatmap
from simulation.heatmaps.heatmap_generator_base import HeatmapGeneratorBase
from simulation.heatmaps.repulsion_heatmap_generator import RepulsionHeatmapGenerator
from simulation.neighbourhood.base_neighbourhood import NeighbourhoodBase
from simulation.core.pedestrian import Pedestrian
from simulation.core.simulation_grid import SimulationGrid
from utils.immutable_list import ImmutableList


class Simulation:
    def __init__(self, time_resolution: float, grid: SimulationGrid, distancing: DistanceBase, social_distancing: RepulsionHeatmapGenerator, obstacle_repulsion: RepulsionHeatmapGenerator, targets: list[Target], spawners: list[Spawner], occupation_bias_modifier: float | None = 1.0, retargeting_threshold: float | None = -1.0, last_position_bias: float | None = None):
        self._pedestrians: list[Pedestrian] = list()
        self._grid: SimulationGrid = grid
        self._targets: list[Target] = targets
        self._spawners: list[Spawner] = spawners
        self._social_distancing_generator: RepulsionHeatmapGenerator = social_distancing
        self._distancing_heatmap: Heatmap = None
        self._distancing = distancing
        self._steps: int = 0
        self._run_time: float = 0
        self._time_resolution: float = time_resolution
        self._occupation_bias_modifier: float | None = occupation_bias_modifier
        self._retargeting_threshold: float | None = retargeting_threshold
        self._obstacle_repulsion_heatmap_generator: RepulsionHeatmapGenerator = obstacle_repulsion
        self._obstacle_repulsion_heatmap: Heatmap = None
        self._last_position_bias: float|None = last_position_bias

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

    def get_social_distancing_heatmap(self) -> Heatmap:
        return self._distancing_heatmap

    def get_obstacle_repulsion_heatmap(self):
        return self._obstacle_repulsion_heatmap

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
        self._update_repulsion_heatmaps()
        self._update_targets()
        self._update_pedestrians(delta)
        self._steps += 1
        self._run_time += delta

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

    def _update_repulsion_heatmaps(self):
        pedestrian_cells = [self._grid.get_cell_at_pos(pedestrian) for pedestrian in self._pedestrians]
        self._distancing_heatmap = self._social_distancing_generator.generate_heatmap(pedestrian_cells, self._grid)
        if self._obstacle_repulsion_heatmap is None: # only needs to be generated once since obstacles don't move
            self._obstacle_repulsion_heatmap = self._obstacle_repulsion_heatmap_generator.generate_heatmap(self._grid.get_cells(), self._grid) if self._obstacle_repulsion_heatmap_generator is not None else Heatmap(self._grid.get_width(), self._grid.get_height(), 0.0)

    def _update_targets(self):
        for target in self._targets:
            target.update_heatmap()

    def _get_cell_value(self, last_pos: Position, path: ImmutableList[Position], cell: Cell, heatmap: Heatmap) -> float:
        value = heatmap.get_cell_at_pos(cell)
        value += self._obstacle_repulsion_heatmap.get_cell_at_pos(cell)
        value += min(0, self._distancing_heatmap.get_cell_at_pos(cell) - self._social_distancing_generator.get_bias(last_pos, cell))
        if self._occupation_bias_modifier is not None:
            value += (self._occupation_bias_modifier * cell.get_pedestrian().get_occupation_bias()) if cell.is_occupied() else 0

        if self._last_position_bias is not None and path is not None and any(p.pos_equals(cell) for p in path):
            value += self._last_position_bias

        return value

    def _get_next_target_cell(self, heatmap: Heatmap, pos: Position, last_pos: Position, path: ImmutableList[Position] = None) -> Cell | None:
        neighbours = self._grid.get_neighbours_at(pos)
        neighbours = sorted(neighbours, key=lambda n: self._get_cell_value(last_pos, path, n, heatmap))
        for cell in neighbours:
            if self._occupation_bias_modifier is not None or cell.is_free():
                return cell

        return None

    def _get_next_pedestrian_target(self, pedestrian: Pedestrian, last_pos: Position) -> Cell | None:
        if pedestrian.is_inside_target():
            self._remove_pedestrian(pedestrian)
            return None
        else:
            return self._get_next_target_cell(pedestrian.get_target().get_heatmap(), pedestrian, last_pos, pedestrian.get_path())

    def _update_pedestrians(self, delta: float):
        for pedestrian in sorted(self._pedestrians, key=lambda p: p.get_current_distance()):
            pedestrian.update(delta)
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

                # if the target cell is occupied, try to find a new target cell to avoid deadlocks
            elif pedestrian.get_targeted_cell().is_occupied() and self._retargeting_threshold is not None and self._retargeting_threshold > pedestrian.get_current_distance():
                new_target_cell = self._get_next_pedestrian_target(pedestrian, pedestrian)
                pedestrian.set_target_cell(new_target_cell)

