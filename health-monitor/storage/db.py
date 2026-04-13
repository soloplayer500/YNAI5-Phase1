import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "state" / "monitor.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist. Safe to call every startup."""
    with get_connection() as conn:
        conn.executescript(SCHEMA_PATH.read_text())
