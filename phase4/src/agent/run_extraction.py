import pandas as pd
import json
from pathlib import Path
from extractor import QuoteExtractor
import sys

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_FILE = DATA_DIR / "groww_analyzed_reviews.csv"
THEME_FILE = DATA_DIR / "theme_summary.json"
OUTPUT_FILE = DATA_DIR / "selected_quotes.json"

# Ensure local imports work
sys.path.append(str(Path(__file__).parent))

def run_extraction():
    """Execute the quote extraction pipeline."""
    print("=" * 60)
    print("PHASE 4: QUOTE EXTRACTION")
    print("=" * 60)
    
    if not INPUT_FILE.exists() or not THEME_FILE.exists():
        print("✗ Analysis data or theme summary not found.")
        return False
        
    print(f"[PROCESS] Loading analyzed data and themes...")
    df = pd.read_csv(INPUT_FILE)
    with open(THEME_FILE, 'r', encoding='utf-8') as f:
        themes = json.load(f)
        
    extractor = QuoteExtractor()
    
    print("[PROCESS] Scoring and selecting top 5 representative quotes...")
    # Get top 5 themes for selection diversity
    top_themes = themes[:5]
    selected_quotes = extractor.extract_best_quotes(df, top_themes, n=5)
    
    print(f"[SUCCESS] Saving selected quotes to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(selected_quotes, f, indent=4)
        
    print("\n" + "=" * 60)
    print("SELECTED QUOTES")
    print("=" * 60)
    for i, q in enumerate(selected_quotes, 1):
        print(f"{i}. Theme: {q['theme']}")
        print(f"   Score: {q['score']:.2f} | Author: {q['author']}")
        print("-" * 60)
        
    return True

if __name__ == "__main__":
    success = run_extraction()
    sys.exit(0 if success else 1)
