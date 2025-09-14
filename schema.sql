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
    CHECK (dur > 0),
    CHECK (-1<wk<7)
);

--List of tasks in a given day
CREATE TABLE IF NOT EXISTS Listicle(
    id INTEGER,
    task_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
);