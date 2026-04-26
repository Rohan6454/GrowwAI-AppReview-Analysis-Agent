import json
from pathlib import Path
from generator import RecommendationGenerator
import sys

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
THEME_FILE = DATA_DIR / "theme_summary.json"
QUOTE_FILE = DATA_DIR / "selected_quotes.json"
OUTPUT_FILE = DATA_DIR / "action_recommendations.json"

# Ensure local imports work
sys.path.append(str(Path(__file__).parent))

def run_generation():
    """Execute the recommendation generation pipeline."""
    print("=" * 60)
    print("PHASE 5: ACTION RECOMMENDATION GENERATION")
    print("=" * 60)
    
    if not THEME_FILE.exists() or not QUOTE_FILE.exists():
        print("✗ Theme summary or selected quotes not found.")
        return False
        
    print(f"[PROCESS] Loading analysis data...")
    with open(THEME_FILE, 'r', encoding='utf-8') as f:
        themes = json.load(f)
    with open(QUOTE_FILE, 'r', encoding='utf-8') as f:
        quotes = json.load(f)
        
    generator = RecommendationGenerator()
    
    print("[PROCESS] Synthesizing 5 concrete product recommendations...")
    recommendations = generator.generate_recommendations(themes, quotes)
    
    print(f"[SUCCESS] Saving recommendations to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(recommendations, f, indent=4)
        
    print("\n" + "=" * 60)
    print("PRODUCT ACTION RECOMMENDATIONS")
    print("=" * 60)
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. [{rec['theme']}] - {rec['priority']} Priority")
        print(f"   Insight: {rec['insight']}")
        print(f"   Action:  {rec['recommendation']}")
        print("-" * 60)
        
    return True

if __name__ == "__main__":
    success = run_generation()
    sys.exit(0 if success else 1)
