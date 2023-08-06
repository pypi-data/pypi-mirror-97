import threading
import types
from dataset_pipe.dataset import Dataset
from dataset_pipe.encoder_list import EncoderList
import dataset_pipe.utils.method as method


class BaseGenerator:

    def __init__(self):
        self._data = None

    @staticmethod
    def _validate(data, param_name):
        if not isinstance(data, dict):
            raise ValueError(f'Param {param_name} must be dict.')
        for name, encoder in data.items():
            required_methods = ['dim', 'type', 'shape', 'encode']
            if not method.has_all(encoder, required_methods):
                missing_methods = method.get_missing(encoder, required_methods)
                raise ValueError(
                    f'Encoder mapped to {param_name}.{name} implement all {required_methods} methods. Method {missing_methods} missing.')

    def dataset(self):
        return Dataset(self)

    def set_data_reader(self, reader):
        if not isinstance(reader, types.GeneratorType):
            raise ValueError("Reader param is not generator")

        self._data = reader


class XYGenerator(BaseGenerator):

    def __init__(self, input_encoders: EncoderList, output_encoders: EncoderList):

        super().__init__()

        if not isinstance(input_encoders, EncoderList) and input_encoders is not None:
            raise ValueError("Param input_encoders must be EncoderList or None")
        if not isinstance(output_encoders, EncoderList) and output_encoders is not None:
            raise ValueError("Param output_encoders must be EncoderList or None")

        if input_encoders:
            self._validate(input_encoders, 'input_encoders')
        if output_encoders:
            self._validate(output_encoders, 'output_encoders')

        self._input_encoders = input_encoders
        self._output_encoders = output_encoders
        self.lock = threading.Lock()

    # def __iter__(self):
    #     return self

    def __iter__(self):

        if not self._data:
            raise ValueError("Data reader is not set. Use set_data_reader method to set reader.")

        with self.lock:
            if self._input_encoders and self._output_encoders:
                for x, y in self._data:
                    x = self._input_encoders.encode(x)
                    y = self._output_encoders.encode(y)
                    yield tuple(x), tuple(y)
            else:
                for x, y in self._data:
                    yield x, y

    def batch(self, *args, **kwargs):
        return self.__iter__()

    def __call__(self, *args, **kwargs):
        return self.__iter__()

    def shapes(self):
        if self._output_encoders and self._input_encoders:
            return self._input_encoders.shapes(), self._output_encoders.shapes()
        return None, None

    def types(self):
        if self._output_encoders and self._input_encoders:
            return self._input_encoders.types(), self._output_encoders.types()
        return 'string', 'string'


class XGenerator(BaseGenerator):

    def __init__(self, input_encoders: EncoderList):

        super().__init__()

        if not isinstance(input_encoders, EncoderList) and input_encoders is not None:
            raise ValueError("Param input_encoders must be EncoderList or None")

        if input_encoders:
            self._validate(input_encoders, 'input_encoders')

        self._input_encoders = input_encoders
        self.lock = threading.Lock()

    # def __iter__(self):
    #     return self

    def __iter__(self):

        if not self._data:
            raise ValueError("Data reader is not set. Use set_data_reader method to set reader.")

        with self.lock:
            if self._input_encoders:
                for x in self._data:
                    x = self._input_encoders.encode(x)
                    yield tuple(x)
            else:
                for x in self._data:
                    yield x

    def batch(self, *args, **kwargs):
        return self.__iter__()

    def __call__(self, *args, **kwargs):
        return self.__iter__()

    def shapes(self):
        if self._input_encoders:
            return self._input_encoders.shapes()
        return None

    def types(self):
        if self._input_encoders:
            return self._input_encoders.types()
        return 'string'
