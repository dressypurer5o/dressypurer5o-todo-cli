"""A tiny command-line todo list backed by a JSON file."""

import json
import sys
from datetime import datetime
from pathlib import Path

STORE = Path.home() / ".todo_cli.json"


def load():
    if STORE.exists():
        return json.loads(STORE.read_text(encoding="utf-8"))
    return []


def save(items):
    STORE.write_text(json.dumps(items, indent=2, ensure_ascii=False),
                     encoding="utf-8")


def main():
    items = load()
    command = sys.argv[1] if len(sys.argv) > 1 else "list"

    if command == "list":
        for index, item in enumerate(items, 1):
            mark = "x" if item["done"] else " "
            print(f"[{mark}] {index}. {item['text']}")
    elif command == "add":
        text = " ".join(sys.argv[2:])
        if not text:
            print("usage: todo.py add <text>")
            return 1
        items.append({"text": text, "done": False,
                      "created": datetime.now().isoformat(timespec="seconds")})
        save(items)
        print("added")
    elif command == "done":
        index = int(sys.argv[2]) - 1
        if 0 <= index < len(items):
            items[index]["done"] = True
            save(items)
            print("marked done")
        else:
            print("bad index")
            return 1
    else:
        print("unknown command")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

