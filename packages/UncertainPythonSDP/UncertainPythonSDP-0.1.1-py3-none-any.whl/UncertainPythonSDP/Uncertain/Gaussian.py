
import numpy as np
import random
import sys


class Gaussian():
    def __init__(self, mu, std):
        self.mean = mu
        self.std = std
        self.SAMPLES = 1000

    def get_samples(self):
        """[Creates random gaussian samples with mean and
            standard deviation. Uses

            numpy.random.normal(mean,std,num_samples)

            function.]
        """
        return np.random.normal(self.mean, self.std, self.SAMPLES)

    def get_support(self):
        """[Fucniton to return the gaussiann samples created.]

        Returns:
            [1-D numpy array]: [Gaussian samples]
        """
        samples = self.get_samples()
        return samples
