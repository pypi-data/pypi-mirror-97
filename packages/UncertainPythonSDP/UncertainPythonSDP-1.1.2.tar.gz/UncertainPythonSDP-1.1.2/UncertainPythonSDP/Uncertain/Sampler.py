import numpy as np
from Uncertain.MarkovChainMonteCarloSampler import MarkovChainMonteCarloSampler


class Sampler():
    def __init__(self):
        self.model = None

    def create(self, source):
        """[Create samples using the MCMC sampler]

        Args:
            source ([obj]): [Object of any distribution class]
        """
        model = MarkovChainMonteCarloSampler(source)
        dist = model.mcmc_sampler()
        self.model = dist

    def take(self, samples):
        """[Randomly pick n samples from a 1-D array like dsitribution.]

        Args:
            samples ([int]): [number of random samples to pick]

        Returns:
            [ndarray]: [n samples picked from the distribution.]
        """
        return np.random.choice(self.model, samples)
