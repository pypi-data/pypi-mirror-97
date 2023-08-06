import numpy as np
from collections import OrderedDict


class EncoderList(OrderedDict):

    def __init__(self, *args, **kwargs):
        super(EncoderList, self).__init__(*args, **kwargs)
        self.no_of_encoders = len(self.values())

    def batch_encode(self, batch_of_items):
        if not isinstance(batch_of_items, list):
            raise ValueError("Batch_of_items must be list.")
        result = [[] for _ in range(self.no_of_encoders)]
        for i, encoder in enumerate(self.values()):
            for item in batch_of_items:
                result[i].append(encoder.encode(item))
        return [np.array(x) for x in result]

    def encode(self, items):
        if isinstance(items, OrderedDict):
            el = list(self.keys())
            il = list(items.keys())
            if el != il:
                raise ValueError("Order of ListEncoder and returned data for generator does not match. Order of ListEncoder {}, order of data {}".
                                 format(el, il))
            encoded = OrderedDict()
            for name, data in items.items():
                encoded[name] = self[name].encode(data)
            return list(encoded.values())
        else:
            return [encoder.encode(items) for _, encoder in self.items()]

    def shapes(self):
        return tuple([encoder.shape() for name, encoder in self.items()])

    def types(self):
        return tuple([encoder.type() for name, encoder in self.items()])

