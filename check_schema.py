"""
Check database schema and table existence.
"""

import sqlite3
from pathlib import Path

# Check if test.db exists
db_path = 'data/test.db'
if not Path(db_path).exists():
    print(f"Database does not exist: {db_path}")
else:
    print(f"Database exists: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        
        if tables:
            # Check reviews table schema
            cursor.execute("PRAGMA table_info(reviews)")
            columns = cursor.fetchall()
            print(f"Reviews table columns:")
            for col in columns:
                print(f"  - {col}")
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

# Also check reviews.db
print("\n---\n")
db_path2 = 'data/reviews.db'
if not Path(db_path2).exists():
    print(f"Database does not exist: {db_path2}")
else:
    print(f"Database exists: {db_path2}")
    try:
        conn = sqlite3.connect(db_path2)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {[t[0] for t in tables]}")
        
        if tables:
            # Check reviews table schema
            cursor.execute("PRAGMA table_info(reviews)")
            columns = cursor.fetchall()
            print(f"Reviews table columns:")
            for col in columns:
                print(f"  - {col}")
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
