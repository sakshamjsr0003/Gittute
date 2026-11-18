"""
PS 22 - To-Do List Application
Concepts: Lists, Functions, Loops, File Handling

Features: add, view, complete and delete tasks.
Tasks are stored in todo.txt (one per line as "title|status")
and the file is saved after every change.
"""

FILENAME = "todo.txt"


def load_tasks():
    """Load tasks from todo.txt. Returns an empty list if the file is missing."""
    tasks = []
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                if "|" in line:
                    title, status = line.rsplit("|", 1)
                else:
                    title, status = line, "Pending"
                if status not in ("Pending", "Done"):
                    status = "Pending"
                tasks.append({"title": title, "status": status})
    except FileNotFoundError:
        pass  # No file yet -> start with an empty list
    except OSError:
        print("Warning: could not read todo.txt. Starting with an empty list.")
    return tasks


def save_tasks(tasks):
    """Write all tasks to todo.txt."""
    try:
        with open(FILENAME, "w", encoding="utf-8") as f:
            for t in tasks:
                f.write(f"{t['title']}|{t['status']}\n")
    except OSError:
        print("Error: could not save tasks to todo.txt.")


def read_task_number(tasks, prompt):
    """Ask for a task number and validate it. Returns an index or None."""
    raw = input(prompt).strip()
    try:
        number = int(raw)
    except ValueError:
        print("Invalid input. Please enter a valid task number.")
        return None
    if number < 1 or number > len(tasks):
        print(f"Task number {number} not found.")
        return None
    return number - 1


def add_task(tasks):
    """Add a new task with status Pending."""
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return
    tasks.append({"title": title, "status": "Pending"})
    save_tasks(tasks)
    print(f"Task added. {len(tasks)} | {title} | Pending")


def view_tasks(tasks):
    """Display all tasks."""
    if not tasks:
        print("No tasks found. Your to-do list is empty.")
        return
    for i, t in enumerate(tasks, start=1):
        print(f"{i} | {t['title']} | {t['status']}")


def complete_task(tasks):
    """Mark a task as Done."""
    idx = read_task_number(tasks, "Enter task number to complete: ")
    if idx is None:
        return
    if tasks[idx]["status"] == "Done":
        print(f"Task {idx + 1} is already completed.")
        return
    tasks[idx]["status"] = "Done"
    save_tasks(tasks)
    print(f"Task {idx + 1} marked as completed.")


def delete_task(tasks):
    """Delete a task."""
    idx = read_task_number(tasks, "Enter task number to delete: ")
    if idx is None:
        return
    tasks.pop(idx)
    save_tasks(tasks)
    print(f"Task {idx + 1} deleted. Tasks left: {len(tasks)}")


def main():
    tasks = load_tasks()
    while True:
        print("\n===== TO-DO LIST =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
