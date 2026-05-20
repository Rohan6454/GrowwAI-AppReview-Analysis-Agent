"""
Test Phase 1 ingestion with actual Groww review data.
"""

import sys
import sqlite3
from pathlib import Path

import os
from dotenv import load_dotenv

# Add project root to sys path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'phase1' / 'src'))

# Load env vars
load_dotenv(BASE_DIR / '.env')

from agent.ingest import ingest_csv_to_db
from src.agent.db import init_db


def main():
    # Initialize database (handles both local and cloud)
    db_path = 'data/reviews.db'
    init_db(db_path)
    print(f'[SUCCESS] Database initialized')
    
    # Ingest sample data
    print('\n=== INGESTING GROWW REVIEWS ===')
    result = ingest_csv_to_db('data/groww_combined_reviews.csv', db_path)
    
    print(f'\nIngestion Results:')
    print(f'  - CSV Path: {result["csv_path"]}')
    print(f'  - Reviews Loaded: {result["reviews_loaded"]}')
    print(f'  - Load Errors: {result["load_errors"]}')
    
    if result["success"]:
        stats = result["ingestion_stats"]
        print(f'  - Ingested: {stats.get("inserted", 0)}')
        print(f'  - Skipped: {stats.get("skipped", 0)}')
        print(f'  - Errors: {stats.get("errors", 0)}')
    else:
        print(f'  - INGESTION FAILED!')
        if result["errors"]:
            print(f'  - Errors: {result["errors"]}')
        sys.exit(1)
    
    # Verify database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as total FROM reviews')
    total_row = cursor.fetchone()
    total = total_row[0] if total_row else 0
    
    print(f'\nDatabase Verification:')
    print(f'  - Total Reviews: {total}')
    
    if total > 0:
        cursor.execute('SELECT AVG(rating) FROM reviews')
        avg = cursor.fetchone()[0]
        print(f'  - Average Rating: {avg:.2f}')
        
        cursor.execute('SELECT review_title FROM reviews LIMIT 1')
        title_row = cursor.fetchone()
        if title_row:
            print(f'  - Sample Title: {title_row[0]}')
        
        # Show rating distribution
        cursor.execute('''
            SELECT rating, COUNT(*) as count 
            FROM reviews 
            GROUP BY rating 
            ORDER BY rating DESC
        ''')
        print(f'\nRating Distribution:')
        for rating, count in cursor.fetchall():
            print(f'  - {rating} stars: {count} reviews')
        
        # Show source distribution
        cursor.execute('''
            SELECT source, COUNT(*) as count 
            FROM reviews 
            GROUP BY source
        ''')
        print(f'\nSource Distribution:')
        for source, count in cursor.fetchall():
            print(f'  - {source}: {count} reviews')
    
    conn.close()
    print('\n[SUCCESS] Phase 1 ingestion pipeline complete!')


if __name__ == '__main__':
    main()
