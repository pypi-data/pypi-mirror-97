class BaseDataSet:

    def __init__(self, reader):

        def _filter(data):
            return {
                       'input': data,
                   }, {
                       'output': data,
                   }

        self.reader = reader
        self.map_lambda = _filter
        self._processor = None

    def process(self, func):
        self._processor = func
        return self

    def map(self, map_lambda):
        self.map_lambda = map_lambda
        return self
