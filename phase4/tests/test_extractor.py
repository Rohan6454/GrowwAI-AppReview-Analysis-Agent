import pytest
import pandas as pd
from phase4.src.agent.extractor import QuoteExtractor

@pytest.fixture
def extractor():
    return QuoteExtractor()

def test_calculate_quote_score_length(extractor):
    # Short
    assert extractor.calculate_quote_score("Good", ["app"], 0.5) < 0.5
    # Ideal
    ideal = "This is a very good app that I use for trading and it works perfectly."
    assert extractor.calculate_quote_score(ideal, ["trading"], 0.5) > 0.6

def test_calculate_quote_score_keywords(extractor):
    text_with_kw = "The login experience is very smooth and fast."
    text_without_kw = "The app is very smooth and fast."
    keywords = ["login", "experience"]
    
    score_with = extractor.calculate_quote_score(text_with_kw, keywords, 0.5)
    score_without = extractor.calculate_quote_score(text_without_kw, keywords, 0.5)
    
    assert score_with > score_without

def test_extract_best_quotes_diversity(extractor):
    data = {
        'review_text': ["Text 1", "Text 2", "Text 3"],
        'cleaned_text': ["text 1", "text 2", "text 3"],
        'theme': ["Theme A", "Theme A", "Theme B"],
        'sentiment_score': [0.5, 0.6, 0.7],
        'author': ["A1", "A2", "B1"]
    }
    df = pd.DataFrame(data)
    themes = [
        {'theme_name': "Theme A", 'keywords': ["text"], 'average_sentiment': 0.5},
        {'theme_name': "Theme B", 'keywords': ["text"], 'average_sentiment': 0.7}
    ]
    
    selected = extractor.extract_best_quotes(df, themes, n=2)
    assert len(selected) == 2
    # Should pick one from each theme for diversity
    themes_selected = [q['theme'] for q in selected]
    assert "Theme A" in themes_selected
    assert "Theme B" in themes_selected
