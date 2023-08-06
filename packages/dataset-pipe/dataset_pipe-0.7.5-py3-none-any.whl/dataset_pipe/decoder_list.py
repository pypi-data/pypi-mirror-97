import numpy as np


class DecoderList:

    def __init__(self, decoders: list):
        if not isinstance(decoders, list):
            raise ValueError(
                "decoders mus be a list of output decoders in order of output results. {} given".format(type(decoders)))
        self.decoders = decoders
        self.no_of_decoders = len(decoders)

    def decode(self, items):
        return [encoder.decode(items) for encoder in self.decoders]

    def batch_decode(self, batch_of_items):

        # if there is only one output slot then this dimension is omitted. We need to standardize this
        # so we must add the dimension of output slot.
        if isinstance(batch_of_items, np.ndarray):
            batch_of_items = [batch_of_items]

        if not isinstance(batch_of_items, list):
            raise ValueError("Batch_of_items must be list of output results. {} given".format(type(batch_of_items)))

        if self.no_of_decoders != len(batch_of_items):
            raise ValueError("Number of decoders ({}) is not equal to  number of output results ({}) given".format(
                self.no_of_decoders, len(batch_of_items)))

        result = [[] for _ in range(self.no_of_decoders)]
        for i, decoder in enumerate(self.decoders):
            for item in batch_of_items[i]:
                result[i].append(decoder.decode(item))
        return result
