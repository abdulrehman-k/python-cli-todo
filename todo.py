#!/usr/bin/env python3
"""CLI To-Do Manager: add, list, complete, and delete tasks. Saved in tasks.json."""

import argparse
import json
from datetime import datetime
from pathlib import Path

DB_FILE = Path("tasks.json")


def load_tasks():
    if not DB_FILE.exists():
        return []
    try:
        return json.loads(DB_FILE.read_text())
    except json.JSONDecodeError:
        print("Warning: tasks.json is corrupted. Starting with an empty list.")
        return []


def save_tasks(tasks):
    DB_FILE.write_text(json.dumps(tasks, indent=2))


def add_task(title):
    tasks = load_tasks()
    next_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({
        "id": next_id,
        "title": title,
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save_tasks(tasks)
    print(f"Added task #{next_id}: {title}")


def list_tasks(show_all=True):
    tasks = load_tasks()
    if not show_all:
        tasks = [t for t in tasks if not t["done"]]
    if not tasks:
        print("No tasks found.")
        return
    print(f"{'ID':<4} {'Status':<8} {'Created':<17} Title")
    print("-" * 50)
    for t in tasks:
        status = "[x]" if t["done"] else "[ ]"
        print(f"{t['id']:<4} {status:<8} {t['created']:<17} {t['title']}")


def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Completed task #{task_id}: {t['title']}")
            return
    print(f"Error: no task with ID {task_id}.")


def delete_task(task_id):
    tasks = load_tasks()
    remaining = [t for t in tasks if t["id"] != task_id]
    if len(remaining) == len(tasks):
        print(f"Error: no task with ID {task_id}.")
        return
    save_tasks(remaining)
    print(f"Deleted task #{task_id}.")


def build_parser():
    parser = argparse.ArgumentParser(description="Simple CLI To-Do Manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task description (use quotes)")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--pending", action="store_true", help="Show only unfinished tasks")

    p_done = sub.add_parser("done", help="Mark a task as completed")
    p_done.add_argument("id", type=int, help="Task ID")

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int, help="Task ID")

    return parser


def main():
    args = build_parser().parse_args()
    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks(show_all=not args.pending)
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)


if __name__ == "__main__":
    main()