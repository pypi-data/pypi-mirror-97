from os import error
from Uncertain.Sampler import Sampler
import numpy as np
import scipy as sp


class Extensions():
    def __init__(self):
        self.NUMM_SAMPLES = 10
        self.PROB = 0.5
        self.ALPHA = 0.5
        self.EPSILON = 0.03
        self.MAX_SAMPLES = 1
        self.INITIAL_SAMPLE_SIZE = 1
        self.SAMPLE_SIZE_STEP = 1

    def pr(self, source):
        """[Implements wald's likelihood ratio test.]

        Args:
            source ([list]): [distribution samples]

        Returns:
            [bool]: [returns True or False]
        """

        H_0 = self.PROB - self.EPSILON
        H_1 = self.PROB + self.EPSILON
        beta = self.ALPHA
        a = np.log(beta / (1 - self.ALPHA))
        b = np.log((1 - beta) / self.ALPHA)
        k = 0

        w_sum = 0.0
        w_sum_true = 0.0
        s = Sampler()
        s.create(source)
        li = s.take(10)
        count = 0.0
        for i in li:
            if i >= 0.5:
                count = count + 1
        count = count / len(li)
        num_samples = 0
        while (num_samples < self.INITIAL_SAMPLE_SIZE):
            if li[num_samples] > 0.5:
                k = k + 1
                w_sum_true = w_sum_true + count
            w_sum = w_sum + count
            num_samples += 1
        test = None
        while (self.NUMM_SAMPLES <= self.MAX_SAMPLES):
            log_likelihood = w_sum_true * \
                np.log(H_1 / H_0) + (w_sum - w_sum_true) * np.log((1 - H_1) / (1 - H_0))

            if (log_likelihood >= b):
                test = True
            elif (log_likelihood <= a):
                test = False
            else:
                i = 0
                while (i < self.SAMPLE_SIZE_STEP):
                    count = 0.0
                    li = s.Take(10)
                    for it in li:
                        if it >= 0.5:
                            count = count + 1
                    count = count / len(li)

                    if li[i] > 0.5:
                        k = k + 1
                        w_sum_true = w_sum_true + count
                    w_sum = w_sum + count
                    i = i + 1
                    self.NUMM_SAMPLES += self.SAMPLE_SIZE_STEP
            test = False

        return test
