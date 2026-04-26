"""
Comprehensive review extraction from Google Play Store and Apple App Store.
Extracts reviews from at least the past 1 week for Groww app.
"""

import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import sys
import time

# Target app details
GOOGLE_PLAY_ID = "com.nextbillion.groww"
APPLE_APP_ID = "1404871703"
APP_NAME = "Groww"

# Paths
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def extract_google_play_reviews(days=7):
    """Extract reviews from Google Play Store for the last N days."""
    print(f"[PROCESS] Extracting Google Play Store reviews for last {days} days...")
    
    try:
        from google_play_scraper import reviews, Sort
        
        all_reviews = []
        continuation_token = None
        target_date = datetime.now() - timedelta(days=days)
        
        print(f"  - Target date: {target_date.date()}")
        
        batch_count = 0
        max_batches = 20  # Safeguard to prevent infinite loops
        
        reached_target_date = False
        
        while not reached_target_date and batch_count < max_batches:
            batch_count += 1
            print(f"  - Fetching batch {batch_count}...")
            
            if continuation_token:
                batch, continuation_token = reviews(
                    app_id=GOOGLE_PLAY_ID,
                    lang='en',
                    country='in',
                    sort=Sort.NEWEST,
                    count=100,
                    continuation_token=continuation_token
                )
            else:
                batch, continuation_token = reviews(
                    app_id=GOOGLE_PLAY_ID,
                    lang='en',
                    country='in',
                    sort=Sort.NEWEST,
                    count=100
                )
            
            if not batch:
                print("  - No more reviews available.")
                break
                
            for review in batch:
                review_at = review.get('at')
                if review_at and review_at < target_date:
                    reached_target_date = True
                    # We don't break immediately to finish the current batch
                all_reviews.append(review)
            
            print(f"    [SUCCESS] Batch {batch_count}: {len(batch)} reviews (total: {len(all_reviews)})")
            
            if not continuation_token:
                break
            
            time.sleep(1) # Rate limiting
            
        # Filter to exactly the date range
        final_reviews = [r for r in all_reviews if r.get('at') and r.get('at') >= target_date]
        print(f"[SUCCESS] Extracted {len(final_reviews)} reviews from Google Play Store (within last {days} days)")
        return final_reviews
        
    except Exception as e:
        print(f"[ERROR] Error extracting Google Play reviews: {e}")
        return []

def extract_apple_app_store_reviews(how_many=200):
    """Extract reviews from Apple App Store."""
    print(f"[PROCESS] Extracting Apple App Store reviews...")
    
    try:
        from app_store_scraper import AppStore
        import warnings
        warnings.filterwarnings('ignore')
        
        scraper = AppStore(app_name=APP_NAME, app_id=APPLE_APP_ID, country="in")
        
        # Explicitly fetch reviews
        print(f"  - Fetching {how_many} reviews...")
        scraper.review(how_many=how_many)
        
        reviews_list = []
        if hasattr(scraper, 'reviews') and scraper.reviews:
            reviews_list = scraper.reviews
        elif hasattr(scraper, 'review_list') and scraper.review_list:
            reviews_list = scraper.review_list
            
        print(f"[SUCCESS] Extracted {len(reviews_list)} reviews from Apple App Store")
        return reviews_list
        
    except Exception as e:
        print(f"[ERROR] Error extracting Apple App Store reviews: {e}")
        return []

def normalize_google_play_reviews(reviews):
    """Normalize Google Play Store reviews to standard format."""
    normalized = []
    for review in reviews:
        try:
            normalized.append({
                'rating': int(review.get('score', 0)),
                'review_title': str(review.get('reviewTitle', '')).strip() or 'No Title',
                'review_text': str(review.get('content', '')).strip(),
                'review_date': review.get('at').strftime('%Y-%m-%d') if review.get('at') else '',
                'source': 'Google Play Store',
                'app': APP_NAME,
                'author': str(review.get('userName', '')).strip(),
                'thumbs_up': int(review.get('thumbsUpCount', 0))
            })
        except Exception as e:
            print(f"  [WARNING] Skipped malformed review: {e}")
    
    return normalized

def normalize_apple_reviews(reviews):
    """Normalize Apple App Store reviews to standard format."""
    normalized = []
    for review in reviews:
        try:
            # Apple review dates are usually datetime objects in app-store-scraper
            dt = review.get('date')
            date_str = dt.strftime('%Y-%m-%d') if hasattr(dt, 'strftime') else str(dt)[:10]
            
            normalized.append({
                'rating': int(review.get('rating', 0)),
                'review_title': str(review.get('title', '')).strip() or 'No Title',
                'review_text': str(review.get('review', '')).strip() or str(review.get('content', '')).strip(),
                'review_date': date_str,
                'source': 'Apple App Store',
                'app': APP_NAME,
                'author': str(review.get('userName', '')).strip() or str(review.get('author', '')).strip(),
                'helpful_count': int(review.get('isEdited', 0)) # app-store-scraper schema varies
            })
        except Exception as e:
            print(f"  [WARNING] Skipped malformed review: {e}")
    
    return normalized

def save_to_csv(reviews, filename):
    """Save reviews to CSV file."""
    if not reviews:
        print(f"  [WARNING] No reviews to save for {filename}")
        return False
    
    filepath = DATA_DIR / filename
    df = pd.DataFrame(reviews)
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"  [SUCCESS] Saved {len(reviews)} reviews to {filepath}")
    return True

def run_extraction():
    """Main extraction workflow."""
    print("=" * 70)
    print(f"{APP_NAME} APP REVIEWS - EXTENSIVE EXTRACTION")
    print("=" * 70)
    
    # 1. Google Play
    gp_raw = extract_google_play_reviews(days=10) # Get 10 days to be safe
    gp_normalized = normalize_google_play_reviews(gp_raw)
    save_to_csv(gp_normalized, "groww_google_play_reviews.csv")
    
    # 2. Apple App Store
    apple_raw = extract_apple_app_store_reviews(how_many=250)
    apple_normalized = normalize_apple_reviews(apple_raw)
    
    # Filter Apple reviews for last 10 days as well
    target_date_str = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
    apple_filtered = [r for r in apple_normalized if r['review_date'] >= target_date_str]
    print(f"  - Filtered Apple reviews to {len(apple_filtered)} recent ones (since {target_date_str})")
    
    save_to_csv(apple_filtered, "groww_apple_app_store_reviews.csv")
    
    # 3. Combined
    combined = gp_normalized + apple_filtered
    if combined:
        save_to_csv(combined, "groww_combined_reviews.csv")
        
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"Google Play Store: {len(gp_normalized)} reviews")
    print(f"Apple App Store: {len(apple_filtered)} reviews")
    print(f"Total: {len(combined)} reviews")
    print(f"Data location: {DATA_DIR.absolute()}")
    print("=" * 70)
    
    return len(combined) > 0

if __name__ == "__main__":
    run_extraction()
