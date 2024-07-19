# Bullet Journal

A very simple command line bullet journal (that only implements the parts I need).
It stores the data in an sqlite3 database and provides an easy to use command line utility to add, update or migrate tasks.
For viewing tasks, it makes heavy use of ANSI escape sequences.

## Features

- Add a new task with a priority.
- Do a task.
- On the next day, on startup all unfinished tasks can be migrated if needed, or ignored, or ticked off.

## Usage

1. Provide the correct path of the `main.py` file in the script `b`.
2. Make it executable `chmod +x b`.
3. Copy the file `b` into a folder that is contained in `$PATH`.

- **View current tasks**
  - `b`
  - Simply typing `b` shows all the tasks of today.
  - If there are open tasks of previous days, they can be migrated to today by typing `y`, `n` by ignoring them if they aren't up to date anymore or `d` if they are already done.
  - Type `b a` to view _all_ tasks of all days. Might become a very long list.
- **Add a task**
  - `b a<enter>`
  - Provide the title and a priority between 1 and 9, or leave empty for no priority.
  - Note that the only the creation day will be remembered, not the exact hour and minute. This makes sorting easier.
- **Do a task**
  - `b d <task-id>`
  - This checks the task off.
- **Delete a task**
  - `b rm <task-id>`
  - Deletes the task completely
  - This is intended to if a mistake was made; if the task isn't up to date, just ignore it in the migration process.
