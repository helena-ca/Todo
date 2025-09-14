--Tasks available that have been registered
CREATE TABLE IF NOT EXISTS Tasks(
    id INTEGER,
    name TEXT NOT NULL UNIQUE,
    --Reccurence: Does it repeat?
    rec INTEGER DEFAULT 0,
    --The time the task takes
    dur INTEGER NOT NULL,
    --The date the task starts
    start_date TEXT ,
    PRIMARY KEY (id),
    CHECK (rec IN (0,1))
    CHECK (dur > 0)
);

--List of tasks in a given day
CREATE TABLE IF NOT EXISTS Listicle(
    id INTEGER,
    task_id INTEGER NOT NULL,
    status INTEGER ,
    PRIMARY KEY (id),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    CHECK (status IS NULL or status IN (0,1))
);