# Todo
A simple command-line manager of tasks built with Python and SQLite.


## Instalation:

### Requirements
- Python 3.7+
- SQLite (Included with python)

### Setup
1. Clone this repository:
    ```bash
    git clone https://github.com/helena-ca/Todo.git
2. Initialize the database (happens automatically on first run).
    ```bash
    python tasks.py list_tasks

## Usage
### Basic invocation:
Run `python tasks.py <command> [options]`

### List of Commands:
- add_task <name> : Registers a new task you can have in any given day
- schd_task <name> <date> [--recurring] [--wk]: Schedules a task for a specific date, with the option of that task happening cyclically every single day or in a specific day of a week
- list_tasks : Provides the list of tasks that are schedule for the day the command is given
- reset_tasks : Completely wipes any task scheduled or registered

### Examples
Add a task:
`python tasks.py add_task "Laundry"`

Schedule a task:
`python tasks.py schd_task "Laundry" 2025-09-15`

Make it reccur every monday:
`python tasks.py schd_task "Laundry" 2025-09-15 -r -wk 0`

List the tasks you have for today:
`python tasks.py list_tasks`

Reset the list:
`python tasks.py reset_tasks`