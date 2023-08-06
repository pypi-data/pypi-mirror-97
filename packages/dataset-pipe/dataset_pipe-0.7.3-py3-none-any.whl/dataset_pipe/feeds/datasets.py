import tensorflow as tf
from collections import OrderedDict

from dataset_pipe.encoder_list import EncoderList
from dataset_pipe.feeds.base import BaseDataSet
from dataset_pipe.generator import XGenerator, XYGenerator
from dataset_pipe.readers.csv_reader import csv_reader
from dataset_pipe.readers.file_reader import file_reader
from dataset_pipe.readers.json_reader import json_reader


class XYDataset(BaseDataSet):

    def __init__(self, content, custom_reader=None):

        self.generator = None
        self.shapes = None

        if content == 'json':
            reader = json_reader
        elif content == 'csv':
            reader = csv_reader
        elif content == 'file':
            reader = file_reader
        elif custom_reader is None:
            raise ValueError(
                "Unknown or not supported content type. If you want to use custom reader set custom reader param.")
        else:
            reader = custom_reader

        super().__init__(reader)

    def _get_reader(self, file, skip=None):

        def _data_reader(dataset_file):
            record = 0
            while True:
                for data in self.reader(dataset_file):

                    if skip:
                        record += 1
                        if record < skip:
                            continue

                    if self.map_lambda:
                        # yields data via filter
                        filtered_data = self.map_lambda(data)

                        # skip not mapped values
                        if filtered_data is None:
                            continue

                        if not isinstance(filtered_data, tuple) or len(filtered_data) != 2:
                            raise ValueError("Filter function must return tuple with 2 arguments: input and output")

                        x, y = filtered_data

                        if self._processor is None:
                            yield OrderedDict(x), OrderedDict(y)
                        else:
                            for _x, _y in self._processor(x, y):
                                yield _x, _y
                    else:
                        yield data

        return _data_reader(file)

    def __call__(self, *args, **kwargs):

        file = args[0]

        if self.generator is None:
            raise ValueError(
                "Encoding is not set. Use encode method to set encoding.  If you want to debug data call debug method.")

        self.generator.set_data_reader(self._get_reader(file))

        dataset = tf.data.Dataset.from_generator(
            self.generator,
            output_types=self.generator.types(),
            output_shapes=self.generator.shapes()
        ).repeat().prefetch(-1)

        return dataset, self.shapes

    def encode(self, input: dict, output=None):
        if output is None:
            output = {}
        self.generator = XYGenerator(
            input_encoders=EncoderList(OrderedDict(input)),
            output_encoders=EncoderList(OrderedDict(output))
        )
        self.shapes = self.generator.shapes()

        return self

    def debug(self, data):
        return self._get_reader(data)


class XDataset(BaseDataSet):

    def __init__(self):

        self.generator = None
        self.shapes = None

        def _reader(source):
            for x in source:

                if self.map_lambda:
                    # yields data via filter
                    x = self.map_lambda(x)

                    # skip not mapped values
                    if x is None:
                        continue

                    if self._processor is None:
                        yield OrderedDict(x)
                    else:
                        for _x in self._processor(x):
                            if isinstance(_x, OrderedDict):
                                yield _x
                            else:
                                yield OrderedDict(_x)
                else:

                    yield x

        super().__init__(_reader)

    def encode(self, input: dict):
        self.generator = XGenerator(
            input_encoders=EncoderList(OrderedDict(input))
        )
        self.shapes = self.generator.shapes()

        return self

    def __call__(self, *args, **kwargs):

        """
            Returns encoded data and its shape
        """

        data = args[0]

        if self.generator is None:
            raise ValueError(
                "Encoding is not set. Use encode method to set encoding. If you want to debug data call debug method.")

        self.generator.set_data_reader(self.reader(data))

        dataset = tf.data.Dataset.from_generator(
            self.generator,
            output_types=self.generator.types()
        ).prefetch(-1)

        # batch and return list
        return list(dataset.batch(len(args[0]))), self.shapes

    def debug(self, data):
        return self.reader(data)
