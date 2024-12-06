from simulation.core.cell_state import CellState
from simulation.core.simulation import Simulation
from simulation.core.simulation_grid import SimulationGrid
from simulation.core.spawner import Spawner
from simulation.core.target import Target
from simulation.heatmaps.distancing.euclidean_distance import EuclideanDistance
from simulation.heatmaps.djisktra_heatmap_generator import DijkstraHeatmapGenerator
from simulation.heatmaps.fast_marching_heatmap_generator import FastMarchingHeatmapGenerator
from simulation.heatmaps.social_distancing_heatmap import SocialDistancingHeatmapGenerator
from simulation.neighbourhood.moore_neighbourhood import MooreNeighbourhood
from visualisation.visualisation import Visualisation


def test_large():
    grid = SimulationGrid(100, 100, MooreNeighbourhood)
    for i in range(0, 90):
        grid.get_cell(49, i).set_osbtacle()
        grid.get_cell(50, i).set_osbtacle()
        grid.get_cell(51, i).set_osbtacle()

    distancing = EuclideanDistance(0.1)
    dijkstra = DijkstraHeatmapGenerator(distancing)
    target = Target("Target", [grid.get_cell(99, 0), grid.get_cell(99, 1), grid.get_cell(99, 2)], grid, dijkstra)
    spawner = Spawner("Spawner", distancing, [grid.get_cell(0, 0), grid.get_cell(0, 1), grid.get_cell(0, 2),], [target], 10, 1, 2, 0)
    social_distancing = SocialDistancingHeatmapGenerator(distancing, 3, 3)
    sim = Simulation(0.1, grid, distancing, social_distancing, [target], [spawner])
    visualisation = Visualisation(sim, 10, 30)
    visualisation.run()

def main():
    grid = SimulationGrid(10, 10, MooreNeighbourhood)
    obstacles_walls = [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (5, 9), (5, 8), (5, 7), (5, 6),
                       (5, 5), (5, 4), (5, 3)]
    obstacles_center = [(4, 3), (5, 3), (4, 5), (5, 4), (5, 5)]

    for (x, y) in obstacles_walls:
        grid.get_cell(x, y).set_osbtacle()

    distancing = EuclideanDistance()
    dijkstra = DijkstraHeatmapGenerator(distancing)
    fast_marching = FastMarchingHeatmapGenerator(distancing, 1.0, {CellState.OBSTACLE})

    target_cells = [grid.get_cell(x, y) for (x, y) in [(9, 9), (9, 8), (9, 7)]]
    target = Target("Target", target_cells, grid, fast_marching)
    target2 = Target("Target2", [grid.get_cell(0, 9), grid.get_cell(1, 9)], grid, fast_marching)

    spawner_cells = [grid.get_cell(x, y) for (x, y) in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    spawner = Spawner("Spawner", distancing, spawner_cells, [target], 20, 2, 1, 0)

    spawner_cells_2 = [grid.get_cell(x, y) for (x, y) in [(9, 0), (8, 0), (9, 1), (8, 1)]]
    spawner2 = Spawner("Spawner2", distancing, spawner_cells_2, [target2], 10, 1, 2, 0)

    social_distancing = SocialDistancingHeatmapGenerator(distancing, 3, 3)

    sim = Simulation(0.1, grid, distancing, social_distancing, [target], [spawner], 2.0)
    vis = Visualisation(sim)
    vis.run()


if __name__ == "__main__":
    main()
