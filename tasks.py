import sqlite3
import argparse
import datetime

# --- Create the Database ---
def start_db (schema):
    conn=sqlite3.connect("todoapp.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row

    with open(schema) as f:
        conn.executescript(f.read())

    conn.commit()
    return conn

# --- Set up CLI Interaction ---
def set_parser(conn):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required = True)

    def valid_taskname(maybe_name):
        row = conn.execute("SELECT 1 FROM Tasks WHERE name = ?", (maybe_name,)).fetchone()
        if row:
            return maybe_name
        raise argparse.ArgumentTypeError(
            f"Not a valid task name: {maybe_name}. Add it first or check spelling."
        )

    def valid_date(pot_date):
        try:
            return datetime.datetime.strptime(pot_date, "%Y-%m-%d").date()
        except:
            raise argparse.ArgumentTypeError(f"Not a valid date: {pot_date}. Use format YYYY-MM-DD.")

    def valid_wk(pot_wk):
        try:
            v = int(pot_wk)
        except:
            raise argparse.ArgumentTypeError("Weekday must be an integer.")
        if -1<v<7:
            return pot_wk
        else:
            raise argparse.ArgumentTypeError(f"Not a valid weekday: {pot_wk}. Try a number between 0 and 6 inclusive.")

    p_add_task = sub.add_parser("add_task", help = "Plan a new task for the future")
    p_add_task.add_argument("name", help= "Name of the task")

    p_schd = sub.add_parser("schd_task", help = "Schedule a task once or ciclically")
    p_schd.add_argument("name", type= valid_taskname, help= "Name of the task")
    p_schd.add_argument("date", type = valid_date, help= "When does this task starts or happens in YYYY-MM-DD format")
    p_schd.add_argument("-r", "--recurring", action = "store_true", help= "Whether it repeats or not")
    p_schd.add_argument("--wk", type=valid_wk ,help= "What day of the week does this task reccur in. 0-Monday through 6-Sunday.")

    sub.add_parser("list_tasks", help= "Provides list of tasks for today")

    sub.add_parser("reset_tasks", help = "Wipe your tasks and start clean.")
    return parser

# --- Main project functionalities ---
def add_task(conn, name):
    conn.execute("INSERT INTO Tasks (name) VALUES (?)", (name,))
    conn.commit()
    print(f"The task {name} has been registered")

def list_task(conn):
    list_update(conn)
    today_todo = conn.execute("""
        SELECT t.name
        FROM Listicle AS l
        INNER JOIN Tasks AS t ON t.id = l.task_id
        ORDER BY t.name;
    """)
    for todo in today_todo:
        print(todo["name"])
    if today_todo.fetchone() is None:
        print("You have no tasks today.")

def list_update(conn):
    conn.execute("DELETE FROM Listicle;")
    cur = conn.execute("SELECT * FROM Tasks")
    now = datetime.datetime.now()
    for row in cur:
        sd= row["start_date"]
        if sd is None:
            continue
        task_temp_date = datetime.datetime.strptime(row["start_date"], "%Y-%m-%d").date()
        if task_temp_date  == now.date():
            conn.execute ("INSERT INTO Listicle (task_id) VALUES (?)", (row["id"],))
        elif task_temp_date  < now.date():
            if row["rec"]:
                if row["wk"] is None:
                    conn.execute ("INSERT INTO Listicle (task_id) VALUES (?)", (row["id"],))
                else:
                    if row["wk"]==now.weekday():
                        conn.execute ("INSERT INTO Listicle (task_id) VALUES (?)", (row["id"],))
    conn.commit()

def schd_task(conn,name, date, rec, wk):
    conn.execute("UPDATE Tasks SET start_date = ?, rec = ?, wk = ? WHERE name = ?", (date, rec, wk, name))
    conn.commit()
    print(f"The task {name} has been registered")

def reset_tasks(conn):
    conn.execute("DELETE FROM Tasks;")
    conn.execute("DELETE FROM Listicle;")
    print("Your todo list has been reset.")
    conn.commit()


conn= start_db("schema.sql")
parser = set_parser(conn)
args = parser.parse_args()

if args.cmd =="add_task":
    add_task(conn, args.name)
elif args.cmd =="schd_task":
    n_date = str(args.date)
    n_r = 1 if args.recurring else 0
    schd_task(conn, args.name, n_date, n_r, args.wk)
elif args.cmd =="list_tasks":
    list_task(conn)
elif args.cmd == "reset_tasks":
    reset_tasks(conn)