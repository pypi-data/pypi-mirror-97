import numba as nb
import numpy as np


@nb.njit(fastmath=True)
def zeros(max_dim):
    return np.zeros(max_dim, )


@nb.njit(fastmath=True)
def concat(vec1, vec2):
    return np.vstack((vec1, vec2))


@nb.njit(fastmath=True)
def ones(max_dim):
    return np.ones(max_dim, )

