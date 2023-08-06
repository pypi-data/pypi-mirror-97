def file_reader(file):
    for row in open(file):
        yield row
