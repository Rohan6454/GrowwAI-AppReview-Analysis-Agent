import pytest
import numpy as np
from phase3.src.agent.analyzer import ReviewAnalyzer

@pytest.fixture
def analyzer():
    return ReviewAnalyzer(n_clusters=2)

def test_sentiment_analysis(analyzer):
    assert analyzer.analyze_sentiment("This app is great and fast!") > 0
    assert analyzer.analyze_sentiment("Horrible experience, it crashed.") < 0
    assert analyzer.analyze_sentiment("It is a blue app.") == 0

def test_clustering_basic(analyzer):
    texts = [
        "best app for trading",
        "great investment platform",
        "worst login experience",
        "cannot login to my account"
    ]
    clusters = analyzer.perform_clustering(texts)
    assert len(clusters) == 4
    assert len(set(clusters)) <= 2

def test_cluster_keywords(analyzer):
    texts = [
        "login issue login problem",
        "login failed login error",
        "trading app stock market",
        "market trading platform stock"
    ]
    analyzer.perform_clustering(texts)
    keywords = analyzer.get_cluster_keywords(top_n=1)
    assert len(keywords) == 2
    # Check if either 'login' or 'trading'/'stock' shows up
    all_keywords = [k[0] for k in keywords.values()]
    assert any(k in ['login', 'trading', 'stock', 'market'] for k in all_keywords)

def test_theme_naming(analyzer):
    keywords = ["login", "problem", "error"]
    assert analyzer.generate_theme_name(keywords) == "Login / Problem"
