import sqlite3
from pathlib import Path
from contextlib import contextmanager
from app.config import settings

def db_path() -> Path:
    prefix = "sqlite:///"
    raw = settings.database_url[len(prefix):] if settings.database_url.startswith(prefix) else settings.database_url
    return Path(raw)

def init_db() -> None:
    path = db_path()
    if str(path.parent) not in ("", "."):
        path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            planner TEXT NOT NULL,
            request_json TEXT NOT NULL,
            response_json TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")
        db.commit()

@contextmanager
def get_db():
    db = sqlite3.connect(db_path())
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()
