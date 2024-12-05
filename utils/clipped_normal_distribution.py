import numpy as np

class ClippedNormalDistribution:
    def __init__(self, mean: float, sigma:float, min:float, max:float):
        self._mean: float = mean
        self._sigma: float = sigma
        self._min: float = min
        self._max:float = max

    def sample(self) -> float:
        value = np.random.normal(self._mean, self._sigma)
        return np.clip(abs(value), self._min, self._max)