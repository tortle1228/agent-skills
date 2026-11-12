import csv
import json
import sys


def build_csv(rows):
    lines = ["id,name,qty"]
    lines += [f"{r['id']},{r['name']},{r['qty']}" for r in rows]
    return "\n".join(lines) + "\n"


def validate(rows):
    for row in rows:
        if row["qty"] < 0:
            raise ValueError(f"negative qty for {row['id']}")


def export_csv(rows, path):
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "name", "qty"])
        for row in rows:
            writer.writerow([row["id"], row["name"], row["qty"]])


def main(argv):
    with open(argv[1]) as handle:
        rows = (row for row in json.load(handle))
    validate(rows)
    export_csv(rows, argv[2])
    print(f"exported to {argv[2]}")


if __name__ == "__main__":
    main(sys.argv)
