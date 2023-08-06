from dataset_pipe.encoders.math.ops import zeros


class OneHotEncoder:

    def __init__(self, dim):
        self._dim = dim
        self._shape = (dim,)
        self._type = "float32"

    def encode(self, data):
        if not isinstance(data, int):
            raise ValueError("Param data must be integer. {} given fo type {}".format(data, type(data)))

        """
        Data  is a list of category ids on each level,
        e.g. 12
        Return dense one hot encoded vector
        """
        vector = zeros(self._shape)
        vector[data] = 1.0
        return vector

    def shape(self):
        return self._shape

    def type(self):
        return self._type

    def dim(self):
        return self._dim
