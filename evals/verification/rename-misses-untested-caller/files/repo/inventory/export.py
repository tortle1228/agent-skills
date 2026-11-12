from inventory.loader import load_rows


def names(path):
    return [row["name"] for row in load_rows(path)]
