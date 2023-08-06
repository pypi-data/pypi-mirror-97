from collections import OrderedDict


class Input(OrderedDict):

    def __init__(self, *args, **kwargs):
        super(Input, self).__init__(*args, **kwargs)
