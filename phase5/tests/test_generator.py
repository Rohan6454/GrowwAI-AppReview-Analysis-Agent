import pytest
from phase5.src.agent.generator import RecommendationGenerator

@pytest.fixture
def generator():
    return RecommendationGenerator()

def test_generate_recommendations_basic(generator):
    themes = [
        {'theme_name': "Login", 'keywords': ["login", "problem"], 'average_sentiment': -0.5},
        {'theme_name': "Trading", 'keywords': ["trading", "app"], 'average_sentiment': 0.5},
        {'theme_name': "Support", 'keywords': ["support", "slow"], 'average_sentiment': -0.2}
    ]
    quotes = [
        {'theme': "Login", 'quote': "Cannot login!"},
        {'theme': "Trading", 'quote': "Nice trading!"},
        {'theme': "Support", 'quote': "Slow support!"}
    ]
    
    recs = generator.generate_recommendations(themes, quotes)
    assert len(recs) == 3
    assert recs[0]['theme'] == "Login"
    assert "resolve reported login failures" in recs[0]['recommendation']
    assert recs[0]['priority'] == "High"

def test_generate_recommendations_empty(generator):
    assert generator.generate_recommendations([], []) == []

def test_generate_recommendations_default_action(generator):
    themes = [{'theme_name': "Unknown", 'keywords': ["xyz"], 'average_sentiment': 0.1}]
    recs = generator.generate_recommendations(themes, [])
    assert len(recs) == 1
    # Should fallback to "app" action
    assert "app stability and performance" in recs[0]['recommendation']
