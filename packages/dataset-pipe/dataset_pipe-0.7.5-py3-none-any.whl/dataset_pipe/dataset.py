import numpy as np
from collections.abc import Iterable


class Iterator:

    def __init__(self, iterator):
        if not isinstance(iterator, Iterable):
            raise ValueError('Passed object is not Iterable.')
        self._generator = iterator

    def __iter__(self):
        return self._generator.__iter__()


class Repeat(Iterator):

    def __iter__(self):
        while True:
            for x in self._generator:
                yield x


class Batch(Iterator):

    def __init__(self, batch, iterator):
        self._batch = batch
        super().__init__(iterator)

    def __iter__(self):
        parameter_x_buffer, parameter_y_buffer = [], []
        c = 0
        _iterator = iter(self._generator)
        for x, y in _iterator:
            c += 1

            if not isinstance(x, tuple):
                raise ValueError("X must be tuple. Tuple indicate how many input parameters there are.")

            if not isinstance(y, tuple):
                raise ValueError("Y must be tuple. Tuple indicate how many output parameters there are.")

            if not parameter_x_buffer:
                parameter_x_buffer = [[] for _ in range(len(x))]

            if not parameter_y_buffer:
                parameter_y_buffer = [[] for _ in range(len(y))]

            for i, _x in enumerate(x):
                parameter_x_buffer[i].append(_x)
            for i, _y in enumerate(y):
                parameter_y_buffer[i].append(_y)

            if c % self._batch == 0:
                parameter_x_buffer = [np.array(x) for x in parameter_x_buffer]
                parameter_y_buffer = [np.array(y) for y in parameter_y_buffer]

                yield parameter_x_buffer, parameter_y_buffer
                parameter_x_buffer, parameter_y_buffer = [], []


class Dataset(Iterator):

    def __init__(self, iterator):
        super().__init__(iterator)

    def repeat(self):
        return Dataset(Repeat(self._generator))

    def batch(self, batch):
        return Dataset(Batch(batch, self._generator))

    # def __next__(self):
    #     return self._generator.__next__()
