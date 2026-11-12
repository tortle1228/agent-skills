from inventory.loader import load_rows


def total_qty(path):
    return sum(int(row["qty"]) for row in load_rows(path))
