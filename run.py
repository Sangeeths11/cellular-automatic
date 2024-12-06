from simulation.core.simulation import Simulation
from simulation.core.simulation_grid import SimulationGrid
from simulation.core.spawner import Spawner
from simulation.core.target import Target
from simulation.heatmaps.social_distancing_heatmap_generator import SocialDistancingHeatmapGenerator
from visualisation.visualisation import Visualisation
from simulationConfig.config_loader import SimulationConfigLoader


def main():
    simulation_config = SimulationConfigLoader.load_config("simulationConfig\\simulation_config.json")

    neighbourhood_class = SimulationConfigLoader.get_neighbourhood_class(simulation_config["grid"]["neighbourhood"])
    grid = SimulationGrid(simulation_config["grid"]["width"], simulation_config["grid"]["height"], neighbourhood_class)
    
    for obstacle in simulation_config["obstacles"]:
        for (x, y) in obstacle["cells"]:
            grid.get_cell(x, y).set_osbtacle() 

    distance_class = SimulationConfigLoader.get_distance_class(simulation_config["distancing"]["type"])
    distancing = distance_class(simulation_config["distancing"]["scale"])

    target_mapping = {}
    for target_config in simulation_config["targets"]:
        target_cells = [grid.get_cell(x, y) for (x, y) in target_config["cells"]]
        blocked_states = SimulationConfigLoader.get_cell_states(target_config["cellstate"])
        heatmap_generator = SimulationConfigLoader.create_heatmap_generator(target_config["heatmap_generator"], distancing, blocked_states)
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