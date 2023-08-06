import numpy as np
from dataset_pipe.encoders.math.ops import zeros


class BinaryEncoder:

    def __init__(self, dim, repeat_output=0):
        self.repeat_output = repeat_output
        self._dim = dim
        self._shape = (dim,)
        self._type = "float32"

    def encode(self, data):
        if not isinstance(data, list):
            raise ValueError("Param data must be list. {} given fo type {}".format(data, type(data)))

        vector = zeros(self._shape)
        for bit in data:
            vector[bit] = 1.0

        if self.repeat_output > 0:
            return np.repeat(np.array([vector]), self.repeat_output, axis=0)
        return vector

    def shape(self):
        return self._shape

    def type(self):
        return self._type

    def dim(self):
        return self._dim

