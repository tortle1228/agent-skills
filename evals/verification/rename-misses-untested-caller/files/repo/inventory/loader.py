import csv


def load_rows(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))
