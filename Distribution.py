# Distribution needed in simulation

import random

class RandomDist:
    # RandomDist is a base abstract class to build a Random distribution.
    # This class contains an abstract method for building a random generator
    # Inherited class must implement this method

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def random(self):
        """
        This class is an abstract method for implementation class
        should return a random value
        :return:
        """
        pass


class NormalDist(RandomDist):
    def __init__(self, mu: float, sigma: float, low: float, high: float):
        """
        To use this class we must provide mu (mean), sigma (standard deviation), low value, and high value
        :param mu: mean, in which the normal gaussian will have most distribution
        :param sigma: a standard deviation for a random normal distribution parameter
        :param low: the lowest value this random generator must provide
        :param high: the highest value this random generator must provide
        """
        RandomDist.__init__(self, "Normal")
        self._mu = mu
        self._sigma = sigma
        self._low = low
        self._high = high

    def random(self):
        """
        This will return a random gaussian generator by checking the low value and highest value
        :return:
        """
        while True:
            x = random.gauss(self._mu, self._sigma)
            if self._low <= x <= self._high:
                return x


class GaussianDiscrete(NormalDist):
    """
    A random Gaussian Discrete generator
    This will include all the feature that gaussian has but will return a discrete value using round
    """

    def __init__(self, mu: float, sigma: float, low: float, high: float):
        """
        To use this class we must provide mu (mean), sigma (standard deviation), low value, and high value
        :param mu: mean, in which the normal gaussian will have most distribution
        :param sigma: a standard deviation for a random gaussian parameter
        :param low: the lowest value this random generator must provide
        :param high: the highest value this random generator must provide
        """
        NormalDist.__init__(self, mu, sigma, low, high)
        RandomDist.__init__(self, "GaussianDiscrete")

    def random(self):
        return round(NormalDist.random(self))
