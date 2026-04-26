"""
Test Phase 1 ingestion with actual Groww review data.
"""

import sys
import sqlite3
from pathlib import Path

# Add phase1 src to path
sys.path.insert(0, str(Path('phase1/src')))

from agent.ingest import ingest_csv_to_db
from phase0.src.agent.db import init_db


def main():
    # Initialize Phase 0 database
    db_path = 'data/reviews.db'
    init_db(db_path)
    print(f'[SUCCESS] Database initialized: {db_path}')
    
    # Ingest sample data
    print('\n=== INGESTING GROWW REVIEWS ===')
    result = ingest_csv_to_db('data/groww_combined_reviews.csv', db_path)
    
    print(f'\nIngestion Results:')
    print(f'  - CSV Path: {result["csv_path"]}')
    print(f'  - Reviews Loaded: {result["reviews_loaded"]}')
    print(f'  - Load Errors: {result["load_errors"]}')
    print(f'  - Ingested: {result["ingestion_stats"]["inserted"]}')
    print(f'  - Skipped: {result["ingestion_stats"]["skipped"]}')
    print(f'  - Errors: {result["ingestion_stats"]["errors"]}')
    
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
