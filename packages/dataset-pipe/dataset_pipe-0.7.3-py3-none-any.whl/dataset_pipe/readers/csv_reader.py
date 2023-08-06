import csv


def csv_reader(file, separator=","):
    with open(file) as f:
        for row in csv.reader(f, delimiter=separator):
            yield row
