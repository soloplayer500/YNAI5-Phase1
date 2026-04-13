CREATE TABLE IF NOT EXISTS events (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp        TEXT NOT NULL,
    metric           TEXT NOT NULL,
    value            REAL NOT NULL,
    level            TEXT NOT NULL,
    context          TEXT,
    suggested_action TEXT
);

CREATE TABLE IF NOT EXISTS states (
    metric          TEXT PRIMARY KEY,
    current_state   TEXT NOT NULL DEFAULT 'OK',
    last_changed    TEXT,
    last_alert_sent TEXT
);

CREATE TABLE IF NOT EXISTS alerts_sent (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    metric    TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    type      TEXT NOT NULL  -- 'trigger' or 'recovery'
);

CREATE TABLE IF NOT EXISTS monitor_self_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp  TEXT NOT NULL,
    error_type TEXT NOT NULL,
    message    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS memory_trends (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp             TEXT NOT NULL,
    available_ram_percent REAL NOT NULL,
    swap_used_mb          REAL NOT NULL,
    swap_delta_mb         REAL         -- NULL on first entry
);

CREATE TABLE IF NOT EXISTS process_snapshots (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp    TEXT NOT NULL,
    process_name TEXT NOT NULL,
    pid          INTEGER NOT NULL,
    memory_mb    REAL NOT NULL,
    cpu_percent  REAL NOT NULL,
    rank         INTEGER NOT NULL  -- 1 = highest memory consumer
);

CREATE TABLE IF NOT EXISTS baseline_metrics (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp         TEXT NOT NULL,
    avg_available_ram REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS decision_trace (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp     TEXT NOT NULL,
    metric        TEXT NOT NULL,
    observation   TEXT,
    insight       TEXT,
    decision      TEXT,
    action        TEXT,
    action_status TEXT,
    result        TEXT DEFAULT 'unknown',
    confidence    REAL
);

CREATE TABLE IF NOT EXISTS learning_log (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp        TEXT NOT NULL,
    issue            TEXT NOT NULL,
    action_suggested TEXT,
    action_taken     TEXT,
    outcome          TEXT
);
