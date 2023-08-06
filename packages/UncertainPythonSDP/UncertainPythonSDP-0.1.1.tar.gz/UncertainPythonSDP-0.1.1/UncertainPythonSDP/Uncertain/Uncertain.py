import numpy as np
from Uncertain.MarkovChainMonteCarloSampler import MarkovChainMonteCarloSampler
from Uncertain.Flip import Flip


class Operator():
    """[Class that implements operation overloading
    Implemented operators : '+','-','*','/'
                            '<','>','<=','>=']
    """

    def __init__(self, val):
        self.val = val.get_support()

    def __str__(self):
        return "({0},{1})".format(self.val)

    def __add__(self, other):
        self_val = np.array(self.val)
        other_val = np.array(other.val)
        lst = list(self_val + other_val)
        mcmc = MarkovChainMonteCarloSampler(lst)
        lst = mcmc.mcmc_sampler()
        return lst

    def __sub__(self, other):
        self_val = np.array(self.val)
        other_val = np.array(other.val)
        lst = list(self_val - other_val)
        mcmc = MarkovChainMonteCarloSampler(lst)
        lst = mcmc.mcmc_sampler()
        return lst

    def __mul__(self, other):
        self_val = np.array(self.val)
        other_val = np.array(other.val)
        lst = list(self_val * other_val)
        mcmc = MarkovChainMonteCarloSampler(lst)
        lst = mcmc.mcmc_sampler()
        return lst

    def __truediv__(self, other):
        self_val = np.array(self.val)
        other_val = np.array(other.val)
        lst = list(self_val / other_val)
        mcmc = MarkovChainMonteCarloSampler(lst)
        lst = mcmc.mcmc_sampler()
        return lst

    def __lt__(self, other):
        self_val = np.array(self.val)
        other_val = np.array(other.val)
        zeros_holder = np.zeros(len(self.val))
        lst = self_val < other_val
        dist = list(zeros_holder + lst)
        prob = dist.count(1) / len(dist)
        lst = Flip(prob, len(dist))
        lst = lst.get_support()
        return lst

    def __le__(self, other):
        self_val = np.array(self.val)
        other_val = np.array(other.val)
        zeros_holder = np.zeros(len(self.val))
        lst = self_val <= other_val
        dist = list(zeros_holder + lst)
        prob = dist.count(1) / len(dist)
        lst = Flip(prob, len(dist))
        lst = lst.get_support()
        return lst

    def __gt__(self, other):
        self_val = np.array(self.val)
        other_val = np.array(other.val)
        zeros_holder = np.zeros(len(self.val))
        lst = self_val > other_val
        dist = list(zeros_holder + lst)
        prob = dist.count(1) / len(dist)
        lst = Flip(prob, len(dist))
        lst = lst.get_support()
        return lst

    def __ge__(self, other):
        self_val = np.array(self.val)
        other_val = np.array(other.val)
        zeros_holder = np.zeros(len(self.val))
        lst = self_val >= other_val
        dist = list(zeros_holder + lst)
        prob = dist.count(1) / len(dist)
        lst = Flip(prob, len(dist))
        lst = lst.get_support()
        return lst
