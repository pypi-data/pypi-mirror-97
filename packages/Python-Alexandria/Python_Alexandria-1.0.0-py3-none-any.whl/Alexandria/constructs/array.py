import numpy as np
from math import ceil


def find_nearest_entry(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]


def min_multiple_under(x, base):
    """
    :param x: Maximum value
    :param base: Base
    :return: Minimum multiple of Base larger than x
    """
    return base*ceil(x/base)


