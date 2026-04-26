"""
Data ingestion module for Phase 1: Data Ingestion.
Handles CSV import from Google Play Store and Apple App Store.
"""

import csv
import sqlite3
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime

from .review import Review


class CSVDataAdapter:
    """Adapter for importing reviews from CSV files."""
    
    def __init__(self, csv_path: str):
        """Initialize CSV adapter with file path."""
        self.csv_path = Path(csv_path)
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    def load_reviews(self) -> List[Review]:
        """Load reviews from CSV file."""
        reviews = []
        errors = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                if not reader.fieldnames:
                    raise ValueError("CSV file is empty or has no headers")
                
                required_fields = {'rating', 'review_title', 'review_text', 'review_date', 'source'}
                csv_fields = set(reader.fieldnames)
                
                missing_fields = required_fields - csv_fields
                if missing_fields:
                    raise ValueError(f"Missing required fields: {missing_fields}")
                
                for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is headers
                    try:
                        # Validate row has all required fields
                        for field in required_fields:
                            if field not in row or row[field].strip() == '':
                                raise ValueError(f"Missing or empty field: {field}")
                        
                        review = Review.from_dict(row)
                        reviews.append(review)
                    
                    except Exception as e:
                        errors.append({
                            'row': row_num,
                            'error': str(e),
                            'data': row
                        })
        
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")
        
        return reviews, errors
    
    def validate_reviews(self, reviews: List[Review]) -> Tuple[List[Review], List[Dict]]:
        """Validate reviews after loading."""
        valid_reviews = []
        invalid_reviews = []
        
        for review in reviews:
            try:
                review.validate()
                valid_reviews.append(review)
            except ValueError as e:
                invalid_reviews.append({
                    'error': str(e),
                    'data': review.to_dict()
                })
        
        return valid_reviews, invalid_reviews


class DatabaseIngester:
    """Ingest reviews into SQLite database."""
    
    def __init__(self, db_path: str):
        """Initialize database ingester."""
        self.db_path = db_path
    
    def ingest_reviews(self, reviews: List[Review]) -> Dict[str, int]:
        """Ingest reviews into database."""
        if not reviews:
            return {
                'total': 0,
                'inserted': 0,
                'skipped': 0,
                'errors': 0
            }
        
        stats = {
            'total': len(reviews),
            'inserted': 0,
            'skipped': 0,
            'errors': 0
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for review in reviews:
                try:
                    cursor.execute('''
                        INSERT INTO reviews (source, rating, review_title, review_text, review_date)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        review.source,
                        review.rating,
                        review.review_title,
                        review.review_text,
                        review.review_date
                    ))
                    stats['inserted'] += 1
                
                except sqlite3.IntegrityError:
                    stats['skipped'] += 1
                except Exception as e:
                    stats['errors'] += 1
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            raise ValueError(f"Database ingestion error: {str(e)}")
        
        return stats


def ingest_csv_to_db(csv_path: str, db_path: str) -> Dict:
    """End-to-end CSV to database ingestion."""
    result = {
        'success': False,
        'csv_path': csv_path,
        'db_path': db_path,
        'reviews_loaded': 0,
        'load_errors': 0,
        'ingestion_stats': {},
        'errors': []
    }
    
    try:
        # Load from CSV
        adapter = CSVDataAdapter(csv_path)
        reviews, load_errors = adapter.load_reviews()
        
        result['reviews_loaded'] = len(reviews)
        result['load_errors'] = len(load_errors)
        
        if load_errors:
            result['errors'].extend(load_errors)
        
        # Validate reviews
        valid_reviews, invalid_reviews = adapter.validate_reviews(reviews)
        
        if invalid_reviews:
            result['errors'].extend(invalid_reviews)
        
        # Ingest to database
        ingester = DatabaseIngester(db_path)
        stats = ingester.ingest_reviews(valid_reviews)
        
        result['ingestion_stats'] = stats
        result['success'] = stats['inserted'] > 0
    
    except Exception as e:
        result['errors'].append(f"Fatal error during ingestion: {str(e)}")
    
    return result
