import numpy as np
from scipy.interpolate import UnivariateSpline

from math.algorithms import largest_prime_factor


def derivative(x, y):
    n = largest_prime_factor(len(x))
    _x = x[0::n]
    _y = y[0::n]
    return UnivariateSpline(_x, _y).derivative()(x)