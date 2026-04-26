"""
Quick test script to validate Phase 1 implementation without pytest complexity.
"""

import sys
import tempfile
import sqlite3
from pathlib import Path

# Add phase1 src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from agent.review import Review
from agent.ingest import CSVDataAdapter, DatabaseIngester, ingest_csv_to_db


def test_review_model():
    """Test Review model creation and validation."""
    print("Testing Review model...")
    
    # Valid review
    try:
        review = Review(
            rating=5,
            review_title="Great app",
            review_text="Really enjoyed it",
            review_date="2024-04-20",
            source="Google Play Store"
        )
        print("  ✓ Valid review created successfully")
    except Exception as e:
        print(f"  ✗ Failed to create valid review: {e}")
        return False
    
    # Invalid rating
    try:
        Review(5, "test", "test", "2024-04-20", "Google Play Store")  # This is valid
        Review(10, "test", "test", "2024-04-20", "Google Play Store")  # This should fail
        print("  ✗ Invalid rating not rejected")
        return False
    except ValueError:
        print("  ✓ Invalid rating properly rejected")
    
    return True


def test_csv_adapter():
    """Test CSV data adapter."""
    print("\nTesting CSV adapter...")
    
    # Create temporary CSV
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write("rating,review_title,review_text,review_date,source\n")
        f.write("5,Great,Really enjoyed it,2024-04-20,Google Play Store\n")
        f.write("4,Good,Nice experience,2024-04-19,Apple App Store\n")
        temp_csv = f.name
    
    try:
        adapter = CSVDataAdapter(temp_csv)
        reviews, errors = adapter.load_reviews()
        
        if len(reviews) == 2 and len(errors) == 0:
            print(f"  ✓ Loaded {len(reviews)} reviews from CSV")
            print(f"    - Review 1: {reviews[0].review_title} ({reviews[0].source})")
            print(f"    - Review 2: {reviews[1].review_title} ({reviews[1].source})")
        else:
            print(f"  ✗ Unexpected load results: {len(reviews)} reviews, {len(errors)} errors")
            return False
    
    finally:
        Path(temp_csv).unlink(missing_ok=True)
    
    return True


def test_database_ingestion():
    """Test database ingestion."""
    print("\nTesting database ingestion...")
    
    # Create temporary database with schema
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_db = f.name
    
    try:
        # Initialize schema
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
        
        if stats['inserted'] == 2:
            print(f"  ✓ Ingested {stats['inserted']} reviews successfully")
            print(f"    - Total: {stats['total']}, Inserted: {stats['inserted']}, Errors: {stats['errors']}")
        else:
            print(f"  ✗ Unexpected ingestion stats: {stats}")
            return False
        
        # Verify database
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM reviews")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count == 2:
            print(f"  ✓ Database verification: {count} reviews confirmed")
        else:
            print(f"  ✗ Database verification failed: expected 2, got {count}")
            return False
    
    finally:
        Path(temp_db).unlink(missing_ok=True)
    
    return True


def test_end_to_end():
    """Test end-to-end CSV to database pipeline."""
    print("\nTesting end-to-end pipeline...")
    
    # Create temporary CSV
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write("rating,review_title,review_text,review_date,source\n")
        f.write("5,Amazing,Absolutely love it,2024-04-20,Google Play Store\n")
        f.write("4,Good,Pretty good,2024-04-19,Apple App Store\n")
        f.write("3,Average,It's okay,2024-04-18,Google Play Store\n")
        temp_csv = f.name
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_db = f.name
    
    try:
        # Initialize schema
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
        
        # Run end-to-end
        result = ingest_csv_to_db(temp_csv, temp_db)
        
        if result['success'] and result['reviews_loaded'] == 3:
            print(f"  ✓ End-to-end pipeline successful")
            print(f"    - Loaded: {result['reviews_loaded']} reviews")
            print(f"    - Inserted: {result['ingestion_stats']['inserted']} reviews")
            print(f"    - Errors: {len(result['errors'])}")
        else:
            print(f"  ✗ Pipeline failed: {result}")
            return False
    
    finally:
        Path(temp_csv).unlink(missing_ok=True)
        Path(temp_db).unlink(missing_ok=True)
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("PHASE 1: DATA INGESTION - QUICK TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Review Model", test_review_model),
        ("CSV Adapter", test_csv_adapter),
        ("Database Ingestion", test_database_ingestion),
        ("End-to-End Pipeline", test_end_to_end),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n✗ {test_name} FAILED with exception:")
            print(f"  {type(e).__name__}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed_count = sum(1 for _, passed in results if passed)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {passed_count}/{len(results)} tests passed")
    print("=" * 60)
    
    return passed_count == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
