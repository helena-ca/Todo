import sqlite3
import argparse


def start_db (schema):
    conn=sqlite3.connect("todoapp.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row

    with open(schema, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    return conn

def set_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required = True)

    p_add_task = sub.add_parser("add_task", help = "Plan a new task for the future")
    p_add_task.add_argument("name", help= "Name of the task")
    p_add_task.add_argument("-r", "--recurring", action = "store_true" ,help= "Whether it repeats or not")
    p_add_task.add_argument("dur", type=int ,help= "How much time the task takes to complete")
    p_add_task.add_argument("-d", "--date" ,help= "When does this task start")

    p_list_task = sub.add_parser("list_tasks", help= "Provides list of tasks for today")

    return parser

def add_task(conn, name, rec, dur, date):
    conn.execute("INSERT INTO Tasks (name, rec, dur, start_date) VALUES (?, ?, ?, ?)", (name, rec, dur, date))
    conn.commit()
    print(f"The task {name} has been registered")

def list_task(conn):
    today_todo = conn.execute("""
        SELECT t.name
        FROM Listicle AS l
        INNER JOIN Tasks AS t ON t.id = l.task_id
        ORDER BY t.name
    """)
    for todo in today_todo:
        print(todo["name"])


parser = set_parser()
args = parser.parse_args()

conn= start_db

if args.cmd =="add_task":
    add_task(conn, args.name, args.r, args.dur, args.date)
elif args.cmd =="list_tasks":
    list_task(conn)