# Todo
A simple command-line todo manager built with Python and SQLite.


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
`python tasks.py <command> (options)`

### List of Commands:
- add_task : Registers a new task you can have in any given day
- schd_task : Schedules a task for a specific date, with the option of that task happening cyclically every single day or in a specific day of a week
- list_tasks : Provides the List of tasks that are schedule for the day the command is given
- reset_tasks : Completely wipes any task scheduled and registered

