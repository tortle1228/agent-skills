import sys


def count_blank(lines):
    return sum(1 for line in lines if line == "")


def main(argv):
    path = argv[1]
    with open(path) as handle:
        lines = handle.readlines()
    print(f"lines={len(lines)} blank={count_blank(lines)}")


if __name__ == "__main__":
    main(sys.argv)
