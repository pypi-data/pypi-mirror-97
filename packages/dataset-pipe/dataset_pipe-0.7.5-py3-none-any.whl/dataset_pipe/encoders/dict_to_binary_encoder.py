import math
import numpy as np
from collections import defaultdict
from dataset_pipe.encoders.math.ops import zeros


class DictToBinaryEncoder:

    def __init__(self, value2idx_dict, post_process=None, normalize=False, append_none_idx=True):

        self.append_none_idx = append_none_idx
        self.post_process = post_process
        self.normalize = normalize
        if '<none>' not in value2idx_dict:
            value2idx_dict['<none>'] = max(value2idx_dict.values()) + 1

        self.value2idx = value2idx_dict
        self.idx2value = defaultdict(list)
        for value, idx in self.value2idx.items():
            self.idx2value[idx].append(value)
        self._dim = max(self.idx2value.keys()) + 1
        self._shape = (self._dim,)
        self._type = "float32"

    def encode(self, data):
        if not isinstance(data, list):
            raise ValueError("Data must be list. {} {} given".format(type(data), data))

        vector = zeros(self._dim)
        boosted_vector = zeros(self._dim)
        boosted_vector_base = zeros(self._dim)
        is_empty = True
        for item in data:
            if item in self.value2idx:
                idx = self.value2idx[item]
                vector[idx] = 1.0

                if self.post_process:
                    aux = self.post_process.process_item(item)
                    base = math.log(aux, 2) if aux != 0 else 0
                    boosted_vector[idx] = 1 / base if base != 0 else 1
                    boosted_vector_base[idx] = 1

                is_empty = False

        if is_empty and self.append_none_idx:
            idx = self.value2idx['<none>']
            vector[idx] = 1.0
        elif self.post_process:
            vector = self.post_process.process_vector(boosted_vector, boosted_vector_base)
        elif self.normalize:
            vector = vector / np.sum(vector)

        return vector

    def _decode(self, vector, threshold=.5):
        if not isinstance(vector, np.ndarray) and not isinstance(vector, list):
            raise ValueError("Decoded data must be np.ndarray. {} {} given".format(type(vector), vector))

        for p, v in enumerate(vector):
            if v >= threshold:
                yield self.idx2value[p], vector[p]

    def decode(self, vector, threshold=.5):
        return list(self._decode( vector, threshold))

    def shape(self):
        return self._shape

    def type(self):
        return self._type

    def dim(self):
        return self._dim
