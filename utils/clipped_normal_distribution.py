import numpy as np

class ClippedNormalDistribution:
    """
    Helper class which randomly samples an absolute value from a normal distribution and clips the value to a given range.
    """
    def __init__(self, mean: float, sigma:float, min:float, max:float):
        """
        :param mean: mean of the normal distribution
        :param sigma: standard deviation of the normal distribution
        :param min: minimum value of the clipped range
        :param max: maximum value of the clipped range
        """
        self._mean: float = mean
        self._sigma: float = sigma
        self._min: float = min
        self._max:float = max

    def sample(self) -> float:
        """
        Samples a value from the normal distribution and clips it to the given range
        :return: positive value clipped to the given range
        """
        value = np.random.normal(self._mean, self._sigma)
        return np.clip(abs(value), self._min, self._max)