import numpy as np


class ZeroDummyEncoder:

    def __init__(self, dim):
        self._dim = dim
        self._shape = (dim,)
        self._type = "float32"

    def encode(self, data):
        return np.zeros(self._dim)

    def shape(self):
        return self._shape

    def type(self):
        return self._type

    def dim(self):
        return self._dim


class NoneEncoder:

    def __init__(self):
        self._dim = 0
        self._shape = (0,)
        self._type = "str"

    def encode(self, data):
        return data

    def shape(self):
        return self._shape

    def type(self):
        return self._type

    def dim(self):
        return self._dim
