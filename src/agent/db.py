import os
import sqlite3
import pandas as pd

SCHEMA = '''
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    external_id TEXT,
    rating INTEGER NOT NULL,
    review_title TEXT,
    review_text TEXT NOT NULL,
    review_date TEXT NOT NULL,
    language TEXT,
    raw_payload TEXT,
    ingested_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    priority INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    generated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
'''

def get_db_url():
    """Get the database URL from environment variables."""
    db_url = os.environ.get("DATABASE_URL")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return db_url

def init_db(db_path: str):
    """Initialize the database schema."""
    db_url = get_db_url()
    if db_url:
        from sqlalchemy import create_engine, text
        engine = create_engine(db_url)
        with engine.connect() as conn:
            # Split schema into individual statements for SQLAlchemy
            for statement in SCHEMA.split(';'):
                if statement.strip():
                    # Remove AUTOINCREMENT for Postgres, it uses SERIAL or identity
                    stmt = statement.replace("AUTOINCREMENT", "")
                    conn.execute(text(stmt))
            conn.commit()
        print(f'Initialized cloud database schema')
    else:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.executescript(SCHEMA)
            conn.commit()
        print(f'Initialized local database schema at {db_path}')

def save_report(title: str, content: str, db_path: str = 'data/reviews.db'):
    """Save a report to the database."""
    db_url = get_db_url()
    if db_url:
        from sqlalchemy import create_engine, text
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO reports (title, content) VALUES (:title, :content)"),
                {"title": title, "content": content}
            )
            conn.commit()
    else:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reports (title, content) VALUES (?, ?)", (title, content))
            conn.commit()

def get_connection(db_path: str):
    db_url = get_db_url()
    if db_url:
        from sqlalchemy import create_engine
        return create_engine(db_url)
    return sqlite3.connect(db_path)
