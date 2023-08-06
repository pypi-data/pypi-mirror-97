from collections import OrderedDict


class Output(OrderedDict):

    def __init__(self, *args, **kwargs):
        super(Output, self).__init__(*args, **kwargs)
