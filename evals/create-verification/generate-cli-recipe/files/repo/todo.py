import json
import os
import sys

STORE = os.environ.get("TODO_FILE", "todo.json")


def load():
    if not os.path.exists(STORE):
        return []
    with open(STORE) as handle:
        return json.load(handle)


def save(items):
    with open(STORE, "w") as handle:
        json.dump(items, handle)


def main(argv):
    command = argv[1] if len(argv) > 1 else "list"
    items = load()
    if command == "add":
        items.append({"text": " ".join(argv[2:]), "done": False})
        save(items)
        print(f"added #{len(items)}")
    elif command == "done":
        items[int(argv[2]) - 1]["done"] = True
        save(items)
        print(f"done #{argv[2]}")
    elif command == "list":
        for number, item in enumerate(items, 1):
            print(f"{number}. [{'x' if item['done'] else ' '}] {item['text']}")
    else:
        print(f"unknown command: {command}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
