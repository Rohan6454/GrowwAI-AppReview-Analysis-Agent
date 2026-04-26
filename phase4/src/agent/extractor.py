import pandas as pd
import re
from typing import List, Dict, Optional

class QuoteExtractor:
    """Utility to select high-quality representative quotes from reviews."""
    
    def __init__(self):
        # Stop words to filter out generic high-frequency words in keyword matching
        self.generic_words = {'app', 'good', 'nice', 'best', 'great', 'excellent', 'love', 'use', 'easy'}

    def calculate_quote_score(self, text: str, theme_keywords: List[str], quote_sentiment: float) -> float:
        """Score a quote based on length, keyword relevance, quality, and negative sentiment preference."""
        if not text or not isinstance(text, str):
            return 0.0
            
        words = text.split()
        word_count = len(words)
        
        # 1. Length Score (Gaussian-like curve centered around 20 words)
        # Penalize very short (< 5) or very long (> 60) quotes
        if word_count < 5:
            length_score = 0.2
        elif word_count > 60:
            length_score = 0.3
        else:
            # Ideal range 10-40 words
            length_score = 1.0 if 10 <= word_count <= 40 else 0.7
            
        # 2. Keyword Relevance (Specificity)
        # Filter out generic keywords from the theme
        meaningful_keywords = [k for k in theme_keywords if k not in self.generic_words]
        if not meaningful_keywords:
            meaningful_keywords = theme_keywords
            
        matches = sum(1 for kw in meaningful_keywords if kw.lower() in text.lower())
        keyword_score = min(1.0, matches / len(meaningful_keywords)) if meaningful_keywords else 0.5
        
        # 3. Quality Heuristics
        # Penalize all caps
        quality_score = 1.0
        if text.isupper():
            quality_score *= 0.5
        # Penalize excessive punctuation
        if text.count('!') > 3 or text.count('?') > 3:
            quality_score *= 0.8
            
        # 4. Sentiment Preference (Favor negative/tough reviews to prompt changes)
        sentiment_multiplier = 1.0
        if quote_sentiment < 0:
            sentiment_multiplier = 2.0  # Big bonus for negative sentiment
        elif quote_sentiment < 0.3:
            sentiment_multiplier = 1.5  # Moderate bonus for neutral/slightly positive
            
        return (length_score * 0.4 + keyword_score * 0.4 + quality_score * 0.2) * sentiment_multiplier

    def extract_best_quotes(self, df: pd.DataFrame, themes: List[Dict], n: int = 3) -> List[Dict]:
        """Select top n quotes across the provided themes."""
        scored_quotes = []
        
        for theme in themes:
            theme_name = theme['theme_name']
            keywords = theme['keywords']
            avg_sentiment = theme['average_sentiment']
            
            # Filter reviews for this theme
            theme_reviews = df[df['theme'] == theme_name]
            
            for _, row in theme_reviews.iterrows():
                # Pass the actual quote sentiment to prioritize negative reviews
                score = self.calculate_quote_score(row['cleaned_text'], keywords, row['sentiment_score'])
                scored_quotes.append({
                    'quote': row['review_text'], # Use original text for the quote
                    'cleaned_quote': row['cleaned_text'],
                    'author': row.get('author', 'Anonymous'),
                    'theme': theme_name,
                    'sentiment': row['sentiment_score'],
                    'score': score
                })
                
        # Sort by score descending
        scored_quotes.sort(key=lambda x: x['score'], reverse=True)
        
        # Select top N, ensuring diversity (at most 1 per theme if N < num_themes)
        selected = []
        used_themes = set()
        
        for q in scored_quotes:
            if q['theme'] not in used_themes:
                selected.append(q)
                used_themes.add(q['theme'])
            if len(selected) == n:
                break
                
        # If we need more to reach N, take the next best regardless of theme
        if len(selected) < n:
            for q in scored_quotes:
                if q not in selected:
                    selected.append(q)
                if len(selected) == n:
                    break
                    
        return selected
