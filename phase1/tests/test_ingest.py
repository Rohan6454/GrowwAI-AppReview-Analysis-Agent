"""
Unit tests for Phase 1: Data Ingestion
Tests CSV loading, validation, and database ingestion.
"""

import pytest
import tempfile
import sqlite3
from pathlib import Path
from agent.review import Review
from agent.ingest import CSVDataAdapter, DatabaseIngester, ingest_csv_to_db


class TestReviewModel:
    """Test Review data model."""
    
    def test_valid_review(self):
        """Test creating a valid review."""
        review = Review(
            rating=5,
            review_title="Great app",
            review_text="Really enjoyed using this app",
            review_date="2024-04-20",
            source="Google Play Store"
        )
        assert review.rating == 5
        assert review.app == "Groww"
    
    def test_invalid_rating(self):
        """Test review with invalid rating."""
        with pytest.raises(ValueError):
            Review(
                rating=10,
                review_title="Great app",
                review_text="Really enjoyed using this app",
                review_date="2024-04-20",
                source="Google Play Store"
            )
    
    def test_empty_title(self):
        """Test review with empty title."""
        with pytest.raises(ValueError):
            Review(
                rating=5,
                review_title="",
                review_text="Really enjoyed using this app",
                review_date="2024-04-20",
                source="Google Play Store"
            )
    
    def test_invalid_source(self):
        """Test review with invalid source."""
        with pytest.raises(ValueError):
            Review(
                rating=5,
                review_title="Great app",
                review_text="Really enjoyed using this app",
                review_date="2024-04-20",
                source="Invalid Source"
            )
    
    def test_review_to_dict(self):
        """Test converting review to dictionary."""
        review = Review(
            rating=4,
            review_title="Good app",
            review_text="Works well",
            review_date="2024-04-15",
            source="Apple App Store"
        )
        data = review.to_dict()
        assert data['rating'] == 4
        assert data['source'] == "Apple App Store"
    
    def test_review_from_dict(self):
        """Test creating review from dictionary."""
        data = {
            'rating': 5,
            'review_title': 'Great',
            'review_text': 'Really great',
            'review_date': '2024-04-20',
            'source': 'Google Play Store'
        }
        review = Review.from_dict(data)
        assert review.rating == 5
        assert review.review_title == 'Great'


class TestCSVDataAdapter:
    """Test CSV data adapter."""
    
    def test_load_valid_csv(self):
        """Test loading valid CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("rating,review_title,review_text,review_date,source\n")
            f.write("5,Great app,Really enjoyed it,2024-04-20,Google Play Store\n")
            f.write("4,Good app,Nice experience,2024-04-19,Apple App Store\n")
            temp_path = f.name
        
        try:
            adapter = CSVDataAdapter(temp_path)
            reviews, errors = adapter.load_reviews()
            
            assert len(reviews) == 2
            assert len(errors) == 0
            assert reviews[0].rating == 5
            assert reviews[1].source == "Apple App Store"
        
        finally:
            Path(temp_path).unlink()
    
    def test_load_csv_with_missing_fields(self):
        """Test loading CSV with missing required fields."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("rating,review_title\n")
            f.write("5,Great app\n")
            temp_path = f.name
        
        try:
            adapter = CSVDataAdapter(temp_path)
            with pytest.raises(ValueError):
                adapter.load_reviews()
        
        finally:
            Path(temp_path).unlink()
    
    def test_load_nonexistent_csv(self):
        """Test loading non-existent CSV file."""
        with pytest.raises(FileNotFoundError):
            CSVDataAdapter("/nonexistent/file.csv")
    
    def test_validate_reviews(self):
        """Test review validation."""
        reviews = [
            Review(5, "Great", "Really great", "2024-04-20", "Google Play Store"),
            Review(10, "Bad", "Invalid rating", "2024-04-20", "Google Play Store")  # This should fail validation
        ]
        
        adapter = CSVDataAdapter.__new__(CSVDataAdapter)
        valid, invalid = adapter.validate_reviews([reviews[0]])
        
        assert len(valid) == 1
        assert len(invalid) == 0


class TestDatabaseIngester:
    """Test database ingestion."""
    
    def test_ingest_reviews(self):
        """Test ingesting reviews into database."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_db = f.name
        
        try:
            # Initialize database schema
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE reviews (
                    id INTEGER PRIMARY KEY,
                    rating INTEGER,
                    review_text TEXT,
                    review_date TEXT,
                    metadata TEXT
                )
            ''')
            conn.commit()
            conn.close()
            
            # Test ingestion
            reviews = [
                Review(5, "Great", "Really great", "2024-04-20", "Google Play Store"),
                Review(4, "Good", "Nice", "2024-04-19", "Apple App Store"),
            ]
            
            ingester = DatabaseIngester(temp_db)
            stats = ingester.ingest_reviews(reviews)
            
            assert stats['total'] == 2
            assert stats['inserted'] == 2
            assert stats['errors'] == 0
            
            # Verify data in database
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM reviews")
            count = cursor.fetchone()[0]
            conn.close()
            
            assert count == 2
        
        finally:
            Path(temp_db).unlink(missing_ok=True)
    
    def test_ingest_empty_reviews(self):
        """Test ingesting empty review list."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_db = f.name
        
        try:
            ingester = DatabaseIngester(temp_db)
            stats = ingester.ingest_reviews([])
            
            assert stats['total'] == 0
            assert stats['inserted'] == 0
        
        finally:
            Path(temp_db).unlink(missing_ok=True)


class TestEndToEndIngestion:
    """Test end-to-end ingestion pipeline."""
    
    def test_csv_to_db_ingestion(self):
        """Test complete CSV to database ingestion."""
        # Create temp CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("rating,review_title,review_text,review_date,source\n")
            f.write("5,Great,Really great,2024-04-20,Google Play Store\n")
            f.write("4,Good,Nice,2024-04-19,Apple App Store\n")
            temp_csv = f.name
        
        # Create temp database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_db = f.name
        
        try:
            # Initialize database schema
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE reviews (
                    id INTEGER PRIMARY KEY,
                    rating INTEGER,
                    review_text TEXT,
                    review_date TEXT,
                    metadata TEXT
                )
            ''')
            conn.commit()
            conn.close()
            
            # Run ingestion
            result = ingest_csv_to_db(temp_csv, temp_db)
            
            assert result['success'] == True
            assert result['reviews_loaded'] == 2
            assert result['ingestion_stats']['inserted'] == 2
        
        finally:
            Path(temp_csv).unlink(missing_ok=True)
            Path(temp_db).unlink(missing_ok=True)
