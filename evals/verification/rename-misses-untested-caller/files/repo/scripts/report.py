import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inventory import loader  # noqa: E402

with open("config.json") as handle:
    config = json.load(handle)

rows = getattr(loader, config["reader"])(sys.argv[1])
print(f"rows={len(rows)}")
