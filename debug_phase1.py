"""
Debug Phase 1 ingestion errors.
"""

import sys
from pathlib import Path

# Add phase1 src to path
sys.path.insert(0, str(Path('phase1/src')))

from agent.ingest import ingest_csv_to_db


def main():
    result = ingest_csv_to_db('data/groww_combined_reviews.csv', 'data/test.db')
    
    print(f"Ingestion Results:")
    print(f"  Success: {result['success']}")
    print(f"  Reviews Loaded: {result['reviews_loaded']}")
    print(f"  Load Errors: {result['load_errors']}")
    print(f"  Ingestion Stats: {result['ingestion_stats']}")
    
    if result['errors']:
        print(f"\nErrors ({len(result['errors'])}):")
        for i, error in enumerate(result['errors'][:5], 1):
            print(f"\n  Error {i}:")
            if isinstance(error, dict):
                for key, value in error.items():
                    if key != 'data':
                        print(f"    {key}: {value}")
                    else:
                        print(f"    data: {str(value)[:80]}...")
            else:
                print(f"    {error}")


if __name__ == '__main__':
    main()
