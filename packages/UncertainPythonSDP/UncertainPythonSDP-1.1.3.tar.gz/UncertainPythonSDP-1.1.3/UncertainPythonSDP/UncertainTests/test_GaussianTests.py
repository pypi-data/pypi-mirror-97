import numpy as np 
import random
import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from Uncertain.Gaussian import Gaussian
from Uncertain.Sampler import Sampler
from Uncertain.Extensions import Extensions 
from Uncertain.Uncertaint import Operator 

def test_gaussian_sample():
    x = Gaussian(5.0, 2.0)
    x = x.get_support()
    sampler = Sampler()
    sampler.create(x)
    for i in sampler.take(100):
        assert(i >= -3 and i <= 13)

def test_gaussian_mean():
    sum_value = 0.0
    x = Gaussian(5.0,1.0)
    x = x.get_support()
    sampler = Sampler()
    sampler.create(x)
    for i in sampler.take(100):
        sum_value += i
    sum_value /= 100
    assert(sum_value >= 4.6 and sum_value <= 5.4)

def test_gaussian_bnn_sample():
    x = Gaussian(1.0, 1.0)
    y = Gaussian(4.0, 1.0)
    z = Operator(x) + Operator(y)
    sampler = Sampler()
    sampler.create(z)
    for i in sampler.take(100):
        assert(i >=-3.0 and i <= 13.0) 

def test_gaussian_bnn_mean():
    x = Gaussian(1.0, 1.0)
    y = Gaussian(4.0, 1.0)
    z = Operator(x) + Operator(y)
    sum = 0.0
    sampler = Sampler()
    sampler.create(z)
    for i in sampler.take(100):
        sum = sum + i
    sum = sum / 100.0
    assert(sum >= 4.11 and sum <= 5.89)

def test_gaussian_bernoulli_mean():
    x = Gaussian(1.0, 1.0)
    y = Gaussian(3.0, 2.0)
    z = Operator(x) > Operator(y)
    sampler = Sampler()
    sampler.create(z)
    k = 0
    for i in sampler.take(100):
        if i < 0:
            k = k + 1
    assert (k >= 13 and k < 52)
    
def test_gaussian_bernoulli_conditional():
    x = Gaussian(1.0, 1.0)
    y = Gaussian(4.0, 2.0)
    extns = Extensions()
    z1 = Operator(x) > Operator(y)
    z2 = Operator(y) < Operator(x)
    z3 = Operator(y) > Operator(x)
    z4 = Operator(x) < Operator(y)
    if extns.pr(z1):
        print("X > Y evaluates true, incorrectly")
        assert True 
    if extns.pr(z2):
        print("Y < X evaluates true, incorrectly")
        assert True
    if extns.pr(z3):
        print("Y > X evaluates false, incorrectly")
        assert True
    if extns.pr(z4):
        print("X < Y evaluates false, incorrectly")
        assert True
