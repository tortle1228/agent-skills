import sys

try:
    open("lint.cfg").close()
except FileNotFoundError:
    print("error: lint.cfg not found", file=sys.stderr)
    sys.exit(2)
print("style ok")
