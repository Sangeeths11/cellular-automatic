import numpy as np
from src.userSimulation import exampleSimulation
from src.visualization.visualization import Visualization

def main():
    exampleSimulation.run()
    data = np.load('data\\exampleSimulation.npy', allow_pickle=True)
    visualization = Visualization(data)
    visualization.run()
    

if __name__ == "__main__":
    main() 