import json
from simulation.core.cell_state import CellState
from simulation.heatmaps.distancing.euclidean_distance import EuclideanDistance
from simulation.heatmaps.djisktra_heatmap_generator import DijkstraHeatmapGenerator
from simulation.heatmaps.fast_marching_heatmap_generator import FastMarchingHeatmapGenerator
from simulation.neighbourhood.moore_neighbourhood import MooreNeighbourhood


class SimulationConfigLoader:
    """Utility class to load and process simulation configuration."""

    @staticmethod
    def load_config(config_file):
        """Load the JSON configuration from a file."""
        with open(config_file, 'r') as file:
            return json.load(file)

    @staticmethod
    def create_heatmap_generator(generator_name, distancing, blocked_states):
        """Create the appropriate heatmap generator based on configuration."""
        if generator_name == "FastMarchingHeatmapGenerator":
            return FastMarchingHeatmapGenerator(distancing, blocked_states)
        elif generator_name == "DijkstraHeatmapGenerator":
            return DijkstraHeatmapGenerator(distancing)
        raise ValueError(f"Unsupported heatmap generator: {generator_name}")

    @staticmethod
    def get_neighbourhood_class(neighbourhood_name):
        """Map the neighbourhood name from JSON to the actual class."""
        neighbourhood_mapping = {
            "MooreNeighbourhood": MooreNeighbourhood,
        }
        if neighbourhood_name in neighbourhood_mapping:
            return neighbourhood_mapping[neighbourhood_name]
        raise ValueError(f"Unsupported neighbourhood type: {neighbourhood_name}")

    @staticmethod
    def get_distance_class(distance_name):
        """Map the distance name from JSON to the actual class."""
        distance_mapping = {
            "EuclideanDistance": EuclideanDistance
        }
        if distance_name in distance_mapping:
            return distance_mapping[distance_name]
        raise ValueError(f"Unsupported distance type: {distance_name}")

    @staticmethod
    def get_cell_states(cellstate_names):
        """Map the cell state names from JSON to the actual CellState objects."""
        try:
            return {CellState[state_name] for state_name in cellstate_names}
        except KeyError as e:
            raise ValueError(
                f"Invalid cellstate name: {e.args[0]}. Ensure it matches the CellState enum."
            ) from e
