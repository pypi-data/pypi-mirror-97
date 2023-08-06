import numpy as np
from dataset_pipe.encoders.math.ops import zeros


class SparseWord2IdxEncoder:

    def __init__(self, word2idx, width, no_word_idx=None):
        self.no_word_idx = no_word_idx
        self.word2idx = word2idx
        self.width = width
        self._dim = 1
        self._shape = (width, 1)
        self._type = "float32"

    def encode(self, data):
        if not isinstance(data, list):
            raise ValueError("Param data must be list. {} given fo type {}".format(data, type(data)))

        vector = []
        for word in data[:self.width]:
            if word in self.word2idx:
                vector.append(self.word2idx[word])
            elif self.no_word_idx:
                vector.append(self.no_word_idx)

        vector = np.array(vector)
        z = zeros(self.width)
        z[:vector.shape[0]] = vector
        return np.expand_dims(z, axis=-1)

    def shape(self):
        return self._shape

    def type(self):
        return self._type

    def dim(self):
        return self._dim
