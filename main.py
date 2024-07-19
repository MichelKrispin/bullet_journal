import os
import sqlite3
from datetime import datetime
from enum import Enum
import argparse
import sys
from colors import *

parser = argparse.ArgumentParser(
    prog="BulletJournal",
    description="A small tasks organizer.\nIf no option is given, then todays tasks will be shown.",
    epilog="If you need help, find someone who can help.",
)
parser.add_argument(
    "option",
    type=str,
    nargs="?",
    choices=["l", "a", "d", "rm"],
    help="The option. Valid options are 'l'='list all', 'a'='add', 'd'='do id', 'rm'='remove'",
)
parser.add_argument(
    "suboption",
    type=int,
    nargs="?",
    help="A suboption for 'd'. Valid options are tasks ids",
)


class TaskStates(Enum):
    """The state description of a task."""

    DUE = "due"
    DONE = "done"
    MIGRATED = "migrated"
    IGNORED = "ignored"


class BulletJournal:
    """Create a bullet journal object.
    Checks on every startup for the db_file, located at '~/.bullet_journal/journal.db'
    and if it doesn't exist yet, creates the path and the file.
    """

    def __init__(
        self,
        db_file: str = os.path.join(
            os.path.expanduser("~"), ".bullet_journal/journal.db"
        ),
    ) -> None:
        self.db_file = db_file
        # Create path if it doesn't exist
        if not os.path.exists(os.path.dirname(self.db_file)):
            os.makedirs(os.path.dirname(self.db_file))

        # If file doesn't exist, create new database file
        # or connect to it if it exists
        self.connection = sqlite3.connect(
            self.db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self.cursor = self.connection.cursor()

        # If the database didn't exist yet, create new task table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT,
                priority INTEGER,
                state TEXT,
                date INTEGER
            )
        """
        )
        self.connection.commit()

        self.migrate()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()

    def migrate(self) -> None:
        """Check if some tasks are due from previous days and ask to migrate them, so copy and set due."""
        date_today = datetime.today()
        date_today = date_today.replace(hour=0, minute=0, second=0, microsecond=0)
        execution_string = f'SELECT id, title, priority, date from tasks WHERE date < {int(date_today.timestamp())} and state = "due"'
        self.cursor.execute(execution_string)
        records = self.cursor.fetchall()

        if len(records) > 0:
            with Bold() as p:
                p("Migration")
            print(" of ", end="")
            with Underline() as p:
                p(str(len(records)))
            print(" unfinished tasks.")
            for row in records:
                task_id = row[0]
                title = row[1]
                priority = row[2]
                date = datetime.fromtimestamp(row[3]).strftime("%d.%m.%y")
                answer = None
                while answer is None:
                    try:
                        with Bold() as p:
                            p("Migrate ")
                        if priority > 0:
                            with BrightRed() as p:
                                p(f"({priority})")
                        else:
                            print("   ", end="")
                        with Italic() as p:
                            p(f" {title}")
                        print(f" from {date}? [y/n/d] ", end="")
                        answer = input("")
                        if answer not in ["y", "n", "d"]:
                            raise ValueError("")
                    except ValueError:
                        with BrightRed():
                            print(
                                'For yes type "y", for no type "n" and for done type "d"'
                            )
                updated_state = ""
                if answer == "y":
                    # Create a new task
                    self.add_task(title, priority, TaskStates.DUE)
                    updated_state = TaskStates.MIGRATED
                elif answer == "d":
                    # Create a new task and set it to done
                    self.add_task(title, priority, TaskStates.DONE)
                    updated_state = TaskStates.MIGRATED
                else:  # Otherwise "n"
                    updated_state = TaskStates.IGNORED
                # Update the state of the old task
                self.update_task(task_id, updated_state)

    def update_task(self, task_id: int, new_state: TaskStates) -> None:
        """Update a task with a new state, so usually set a task to done or to migrate.

        Args:
            task_id (int): The task id.
            new_state (TaskStates): The updated state.
        """
        update_task_state = "UPDATE tasks set state=? WHERE id=?"
        try:
            self.cursor.execute(update_task_state, (new_state.value, task_id))
            self.connection.commit()
        except Exception as e:
            with BrightRed():
                print(f"BulletJournal: error: update task: {str(e)}")

    def add_task(self, title: str, priority: int, state: TaskStates) -> None:
        date_today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        self.cursor.execute(
            """INSERT INTO tasks (title, priority, state, date)
                VALUES(?,?,?,?)""",
            (title, priority, state.value, int(date_today.timestamp())),
        )
        self.connection.commit()

    def get_tasks(self, today: bool = True) -> None:
        """Fetch all tasks or just the tasks of the current date.

        Args:
            today (bool, optional): Whether to fetch all tasks or just the one of today. Defaults to True.
        """
        execution_string = "SELECT id, title, priority, state, date from tasks"
        if today:
            print("        ", end="")
            with Bold(), Underline():
                print("Today")
            date_today = datetime.today().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            execution_string += f" WHERE date >= {int(date_today.timestamp())}"
        execution_string += " ORDER BY date ASC, state ASC, priority ASC;"
        self.cursor.execute(execution_string)
        records = self.cursor.fetchall()

        def print_line(priority, title, date, task_id):
            if priority > 0:
                with BrightRed() as p:
                    p(f"({priority})")
            else:
                print("   ", end="")
            print(" ", end="")
            with Italic() as p:
                p(f"{title:45}")
            if not today:
                print(f" from {date} ", end="")
            with BrightBlack():
                print(f"[id={task_id}]")

        for row in records:
            task_id = row[0]
            title = row[1]
            priority = row[2]
            state = row[3]
            date = datetime.fromtimestamp(row[4]).strftime("%d.%m.%y")
            if state == TaskStates.DONE.value:
                with Bold(), Green() as p:
                    p("[x] ")
                    print_line(priority, title, date, task_id)
            elif state == TaskStates.DUE.value:
                with Bold() as p:
                    p("[ ] ")
                print_line(priority, title, date, task_id)
            elif state == TaskStates.MIGRATED.value:
                with Dim() as p:
                    p("[>] ")
                    print_line(priority, title, date, task_id)
            elif state == TaskStates.IGNORED.value:
                with Strikethrough() as p:
                    p("[ ] ")
                    print_line(priority, title, date, task_id)

    def delete_task(self, task_id: int) -> None:
        """Delete the task with a given id if it exists.

        Args:
            task_id (int): The given task id.
        """
        # First check if a task with that id actually exist
        self.cursor.execute("SELECT id from tasks WHERE id=?", (task_id,))
        if len(self.cursor.fetchall()) == 0:
            with BrightRed():
                print(f"BulletJournal: No task with id={task_id} exists")
            sys.exit(-1)

        deletion_string = "DELETE FROM tasks WHERE id=?"
        self.cursor.execute(deletion_string, (task_id,))
        self.connection.commit()


if __name__ == "__main__":
    args = parser.parse_args()

    with BulletJournal() as journal:
        # Showing the today tasks
        if args.option == None:
            journal.get_tasks()

        # Showing all tasks
        elif args.option == "l":
            journal.get_tasks(today=False)

        # Removing a task
        elif args.option == "rm":
            if args.suboption == None:
                with BrightRed():
                    print(
                        "BulletJournal: error: argument option: invalid choice: after 'rm' a task id must be given"
                    )
                sys.exit(-1)
            task_id = args.suboption
            journal.delete_task(task_id)
            journal.get_tasks()

        # Adding a new task
        elif args.option == "a":
            print("          ", end="")
            with Bold(), Underline():
                print("New Task")
            title = ""
            while title == "":
                with Bold() as p:
                    p("Title:    ")
                title = input("")
            priority = -1
            while priority < 0:
                with Bold() as p:
                    p("Priority: ")
                try:
                    priority = input("")
                    if priority == "":
                        priority = 0
                    else:
                        priority = int(priority)
                        if priority < 0 or priority > 9:
                            raise ValueError()
                except ValueError:
                    with BrightRed():
                        print("Must be between 0 and 9")
            journal.add_task(title, priority, TaskStates.DUE)
            print("")
            journal.get_tasks()

        # Set a task to done
        elif args.option == "d":
            if args.suboption == None:
                with BrightRed():
                    print(
                        "BulletJournal: error: argument option: invalid choice: after 'd' a task id must be given"
                    )
                sys.exit(-1)
            task_id = args.suboption
            with Bold() as p:
                p("Finished")
            print(" task ", end="")
            with Underline():
                print(str(task_id))
            journal.update_task(task_id, TaskStates.DONE)
            journal.get_tasks()
