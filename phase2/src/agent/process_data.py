import pandas as pd
from pathlib import Path
from cleaner import ReviewCleaner
import sys

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_FILE = DATA_DIR / "groww_combined_reviews.csv"
OUTPUT_FILE = DATA_DIR / "groww_cleaned_reviews.csv"

def process_reviews():
    """Load, clean, and deduplicate reviews."""
    print("=" * 60)
    print("PHASE 2: DATA CLEANING AND NORMALIZATION")
    print("=" * 60)
    
    if not INPUT_FILE.exists():
        print(f"✗ Input file not found: {INPUT_FILE}")
        return False
        
    print(f"[PROCESS] Loading raw reviews from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    initial_count = len(df)
    print(f"  - Loaded {initial_count} reviews.")
    
    cleaner = ReviewCleaner()
    
    print("[PROCESS] Cleaning and normalizing review text...")
    # Apply cleaning pipeline
    df['cleaned_text'] = df['review_text'].apply(lambda x: cleaner.process(str(x)))
    
    # Remove rows that were identified as spam/empty
    df = df.dropna(subset=['cleaned_text'])
    after_cleaning_count = len(df)
    print(f"  - {initial_count - after_cleaning_count} reviews removed as spam or low-value.")
    
    print("[PROCESS] Handling duplicates...")
    # Exact deduplication on cleaned text and author
    # We keep the first occurrence
    df = df.drop_duplicates(subset=['cleaned_text', 'author'], keep='first')
    final_count = len(df)
    print(f"  - {after_cleaning_count - final_count} duplicates removed.")
    
    print(f"[SUCCESS] Saving cleaned reviews to {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    
    print("\n" + "=" * 60)
    print("CLEANING SUMMARY")
    print("=" * 60)
    print(f"Raw reviews:        {initial_count}")
    print(f"Cleaned & Filtered: {after_cleaning_count}")
    print(f"Final (Unique):     {final_count}")
    print(f"Reduction:          {((initial_count - final_count) / initial_count * 100):.1f}%")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = process_reviews()
    sys.exit(0 if success else 1)
