import numpy as np


class Flip:
    def __init__(self, prob, dist_len):
        self.prob = prob
        self.dist_len = dist_len

    def get_samples(self):
        """
        Function to check the probability of flip

        Returns:
            1-D numppy array : array of samples
        """
        lst = []
        for i in range(self.dist_len):
            random_prob = np.random.uniform(0.0, 1.0)
            lst.append(int(random_prob < self.prob))
        return lst

    def get_support(self):
        """
         Function to return the flip samples

        Returns:
            1-D numpy array: array of samples
        """
        samples = self.get_samples()
        return samples
