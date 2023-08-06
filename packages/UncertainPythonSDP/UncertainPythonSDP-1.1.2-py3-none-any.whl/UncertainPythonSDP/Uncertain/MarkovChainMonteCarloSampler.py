import numpy as np
import random
import sys


class MarkovChainMonteCarloSampler():

    def __init__(self, source):
        self.source = source
        self.iterations = 5000

    def prior(self, x):
        """[This fucnitons checks for
        log doesn't return negative values.]

        Args:
            x ([list]): [parameters of the distribution]

        Returns:
            [int]: [returns 0 or 1]
        """
        if(x[1] <= 0):
            return 0
        return 1

    def transition_model(self, x):
        """[Defines how the current parameter value
        moves to new parameter value.]

        Args:
            x ([list]): [Current parameters]

        Returns:
            [list]: [new parameters]
        """
        return [x[0], np.random.normal(x[1], 0.5, (1,))[0]]

    def likelihood(self, x, data):
        """[Computes the likelihood of the data
        given the parameters.]

        Args:
            x ([list]): [parameters]
            data ([list]): [data sampled from a distribution.]

        Returns:
            [float]: [likelihood]
        """
        return np.sum(-np.log(x[1] * np.sqrt(2 * np.pi)) -
                      ((data - x[0])**2) / (2 * x[1]**2))

    def accept(self, oldTrace, trace):
        """[Defines whether to accept or reject a sample.]

        Args:
            oldTrace ([list]): [old parameters]
            trace ([list]): [new parameters]

        Returns:
            [bool]: [new parameters accepted or not]
        """
        if trace > oldTrace:
            return True
        else:
            accept = np.random.uniform(0, 1)
            return (accept < (np.exp(trace - oldTrace)))

    def mcmc_sampler(self):
        """[Implements metropolis hastings algorithm.]

        Returns:
            [ndarray]: [New distribution using learned parameters.]
        """
        obs_mean = np.mean(self.source)
        x = [obs_mean, 0.1]
        accepted = []
        rejected = []
        for i in range(self.iterations):
            x_new = self.transition_model(x)
            x_lik = self.likelihood(x, self.source)
            x_new_lik = self.likelihood(x_new, self.source)
            oldtrace = x_lik + np.log(self.prior(x))
            newtrace = x_new_lik + np.log(self.prior(x_new))
            if (self.accept(oldtrace, newtrace)):
                x = x_new
                accepted.append(x_new)
            else:
                rejected.append(x_new)
        mean = accepted[0][0]
        std = accepted[-1][-1]
        new_dist = np.random.normal(mean, std, 100)
        return new_dist
