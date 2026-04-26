import pandas as pd
import json
from pathlib import Path
from analyzer import ReviewAnalyzer
import sys

# Ensure local imports work
sys.path.append(str(Path(__file__).parent))

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_FILE = DATA_DIR / "groww_cleaned_reviews.csv"
OUTPUT_FILE = DATA_DIR / "groww_analyzed_reviews.csv"
SUMMARY_FILE = DATA_DIR / "theme_summary.json"

def run_analysis():
    """Run clustering and sentiment analysis pipeline."""
    print("=" * 60)
    print("PHASE 3: THEME CLUSTERING AND SENTIMENT ANALYSIS")
    print("=" * 60)
    
    if not INPUT_FILE.exists():
        print(f"✗ Input file not found: {INPUT_FILE}")
        return False
        
    print(f"[PROCESS] Loading cleaned reviews from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    if df.empty:
        print("✗ No reviews to analyze.")
        return False
        
    # Filter out any rows with missing cleaned_text
    df = df.dropna(subset=['cleaned_text'])
    
    analyzer = ReviewAnalyzer(n_clusters=5)
    
    print("[PROCESS] Clustering reviews into 5 themes...")
    df['cluster'] = analyzer.perform_clustering(df['cleaned_text'].tolist())
    
    print("[PROCESS] Calculating sentiment scores...")
    df['sentiment_score'] = df['cleaned_text'].apply(analyzer.analyze_sentiment)
    
    print("[PROCESS] Generating theme names and summaries...")
    keywords = analyzer.get_cluster_keywords(top_n=5)
    
    theme_summary = []
    for cluster_id in range(5):
        cluster_df = df[df['cluster'] == cluster_id]
        cluster_keywords = keywords[cluster_id]
        theme_name = analyzer.generate_theme_name(cluster_keywords)
        
        avg_sentiment = cluster_df['sentiment_score'].mean()
        volume = len(cluster_df)
        
        # Priority score: Higher volume and more negative sentiment = higher priority
        # We use (1 - sentiment) to weight negative reviews higher
        priority_score = volume * (1.1 - avg_sentiment)
        
        theme_summary.append({
            'cluster_id': int(cluster_id),
            'theme_name': theme_name,
            'keywords': cluster_keywords,
            'volume': int(volume),
            'average_sentiment': float(avg_sentiment),
            'priority_score': float(priority_score)
        })
        
    # Sort themes by priority
    theme_summary.sort(key=lambda x: x['priority_score'], reverse=True)
    
    # Map cluster IDs to theme names in the main dataframe
    cluster_to_name = {t['cluster_id']: t['theme_name'] for t in theme_summary}
    df['theme'] = df['cluster'].map(cluster_to_name)
    
    print(f"[SUCCESS] Saving analyzed reviews to {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    
    print(f"[SUCCESS] Saving theme summary to {SUMMARY_FILE}...")
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(theme_summary, f, indent=4)
        
    print("\n" + "=" * 60)
    print("THEME ANALYSIS SUMMARY (Sorted by Priority)")
    print("=" * 60)
    for i, theme in enumerate(theme_summary, 1):
        sentiment_label = "Positive" if theme['average_sentiment'] > 0.1 else ("Negative" if theme['average_sentiment'] < -0.1 else "Neutral")
        print(f"{i}. {theme['theme_name']:<25} | Vol: {theme['volume']:>4} | Sent: {theme['average_sentiment']:>5.2f} ({sentiment_label})")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = run_analysis()
    sys.exit(0 if success else 1)
