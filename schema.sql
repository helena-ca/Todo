--Tasks available that have been registered
CREATE TABLE IF NOT EXISTS Tasks(
    id INTEGER,
    name TEXT NOT NULL UNIQUE,
    start_date TEXT ,
    --Reccurence: Does it repeat?
    rec INTEGER DEFAULT 0,
    --If it repeats, does it repeat on a specific weekday
    wk INTEGER,
    PRIMARY KEY (id),
    CHECK (rec IN (0,1)),
    CHECK (wk BETWEEN 0 AND 6 OR wk IS NULL)
);

--List of tasks in a given day
CREATE TABLE IF NOT EXISTS Listicle(
    id INTEGER,
    task_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (task_id) REFERENCES Tasks(id) ON DELETE CASCADE
);