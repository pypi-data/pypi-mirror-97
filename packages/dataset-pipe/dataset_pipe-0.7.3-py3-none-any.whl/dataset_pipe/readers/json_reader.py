import json
from json import JSONDecodeError


def json_reader(file):
    for line in open(file):
        try:
            yield json.loads(line)
        except JSONDecodeError:
            continue
