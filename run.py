from simulation.core.simulation import Simulation
from simulation.core.simulation_grid import SimulationGrid
from simulation.core.spawner import Spawner
from simulation.core.target import Target
from simulation.heatmaps.distancing.euclidean_distance import EuclideanDistance
from simulation.heatmaps.djisktra_heatmap_generator import DijkstraHeatmapGenerator
from simulation.heatmaps.social_distancing_heatmap import SocialDistancingHeatmapGenerator
from simulation.neighbourhood.moore_neighbourhood import MooreNeighbourhood
from visualisation.visualisation import Visualisation


def main():
    grid = SimulationGrid(20, 20, MooreNeighbourhood)
    for (x, y) in [(4,3),(5,3),(4,5),(5,4),(5,5)]:
        grid.get_cell(x, y).set_osbtacle()

    distancing = EuclideanDistance()
    dijkstra = DijkstraHeatmapGenerator(distancing)
    target_cells = [grid.get_cell(x, y) for (x, y) in [(9,9), (9,8), (9,7)]]
    target = Target("Target", target_cells, grid, dijkstra)
    target2 = Target("Target2", [grid.get_cell(0, 9), grid.get_cell(1, 9)], grid, dijkstra)

    spawner_cells = [grid.get_cell(x, y) for (x, y) in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    spawner = Spawner("Spawner", distancing, spawner_cells, [target], 10, 1, 2, 0)

    spawner_cells_2 = [grid.get_cell(x, y) for (x, y) in [(9, 0), (8, 0), (9, 1), (8, 1)]]
    spawner2 = Spawner("Spawner2", distancing, spawner_cells_2, [target2], 10, 1, 2, 0)

    social_distancing = SocialDistancingHeatmapGenerator(distancing, 3, 3)

    sim = Simulation(0.1, grid, distancing, social_distancing, [target, target2], [spawner, spawner2])
    vis = Visualisation(sim)
    vis.run()

if __name__ == "__main__":
    main()