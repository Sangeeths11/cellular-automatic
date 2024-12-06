import json
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

def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)
    
def create_heatmap_generator(generator_name, distancing):
    if generator_name == "FastMarchingHeatmapGenerator":
        return FastMarchingHeatmapGenerator(distancing, {CellState.OBSTACLE})
    elif generator_name == "DijkstraHeatmapGenerator":
        return DijkstraHeatmapGenerator(distancing)
    raise ValueError(f"Unsupported heatmap generator: {generator_name}")

def get_neighbourhood_class(neighbourhood_name):
    """Map the neighbourhood name from JSON to the actual class."""
    neighbourhood_mapping = {
        "MooreNeighbourhood": MooreNeighbourhood,
    }
    if neighbourhood_name in neighbourhood_mapping:
        return neighbourhood_mapping[neighbourhood_name]
    raise ValueError(f"Unsupported neighbourhood type: {neighbourhood_name}")

def test_large():
    grid = SimulationGrid(100, 100, MooreNeighbourhood)
    for i in range(0, 80):
        grid.get_cell(49, i).set_osbtacle()
        grid.get_cell(50, i).set_osbtacle()
        grid.get_cell(51, i).set_osbtacle()

    for i in range(10, 52):
        grid.get_cell(i, 79).set_osbtacle()
        grid.get_cell(i, 80).set_osbtacle()
        grid.get_cell(i, 81).set_osbtacle()

    for i in range(25, 75):
        grid.get_cell(i, 49).set_osbtacle()
        grid.get_cell(i, 50).set_osbtacle()
        grid.get_cell(i, 51).set_osbtacle()

    for i in range(40, 82):
        grid.get_cell(10, i).set_osbtacle()
        grid.get_cell(11, i).set_osbtacle()
        grid.get_cell(12, i).set_osbtacle()

    distancing = EuclideanDistance(0.1)
    fast_marching = FastMarchingHeatmapGenerator(distancing, {CellState.OBSTACLE})
    dijkstra = DijkstraHeatmapGenerator(distancing)
    target = Target("Target", [grid.get_cell(52, 0), grid.get_cell(52, 1), grid.get_cell(52, 2)], grid, fast_marching)
    spawner = Spawner("Spawner", distancing, [grid.get_cell(0, 0), grid.get_cell(0, 1), grid.get_cell(0, 2), grid.get_cell(0, 3), grid.get_cell(0, 4), grid.get_cell(0, 5), grid.get_cell(0, 6)], [target], 100, 2, 1, 0)
    social_distancing = SocialDistancingHeatmapGenerator(distancing, 3, 3, {CellState.OCCUPIED}, 0.1)
    sim = Simulation(0.1, grid, distancing, social_distancing, [target], [spawner], None, -1.0)
    visualisation = Visualisation(sim, 10, 30)
    visualisation.run()

def main():
    simulation_config = load_config("simulation_config.json")

    neighbourhood_class = get_neighbourhood_class(simulation_config["grid"]["neighbourhood"])
    grid = SimulationGrid(simulation_config["grid"]["width"], simulation_config["grid"]["height"], neighbourhood_class)
    
    for (x, y) in simulation_config["obstacles"]["walls"]:
        grid.get_cell(x, y).set_osbtacle()

    distancing = EuclideanDistance(1.0)

    target_mapping = {}
    for target_config in simulation_config["targets"]:
        target_cells = [grid.get_cell(x, y) for (x, y) in target_config["cells"]]
        heatmap_generator = create_heatmap_generator(target_config["heatmap_generator"], distancing)
        target_obj = Target(target_config["name"], target_cells, grid, heatmap_generator)
        target_mapping[target_config["name"]] = target_obj

    
    spawners = []
    for spawner_config in simulation_config["spawners"]:
        spawner_cells = [grid.get_cell(x, y) for (x, y) in spawner_config["cells"]]
        spawner_targets = [target_mapping[name] for name in spawner_config["targets"]]
        spawners.append(Spawner(
            spawner_config["name"], distancing, spawner_cells, spawner_targets,
            spawner_config["total_spawns"], spawner_config["batch_size"],
            spawner_config["spawn_delay"], spawner_config["initial_delay"]
        ))

    social_distancing = SocialDistancingHeatmapGenerator(
        distancing,
        simulation_config["social_distancing"]["width"],
        simulation_config["social_distancing"]["height"]
    )

    sim = Simulation(
        simulation_config["simulation"]["time_resolution"],
        grid,
        distancing,
        social_distancing,
        list(target_mapping.values()),
        spawners,
        simulation_config["simulation"].get("occupation_bias_modifier", 1.0),
        simulation_config["simulation"].get("retargeting_threshold", -1.0)
    )
    vis = Visualisation(sim)
    vis.run()


if __name__ == "__main__":
    main()
