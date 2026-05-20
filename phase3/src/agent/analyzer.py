import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import List, Dict, Tuple

# Ensure NLTK data is available
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

class ReviewAnalyzer:
    """Analyzer for clustering reviews into themes and calculating sentiment."""
    
    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.vectorizer = TfidfVectorizer(
            max_df=0.8,
            min_df=2,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.sia = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text: str) -> float:
        """Calculate compound sentiment score."""
        if not text:
            return 0.0
        return self.sia.polarity_scores(text)['compound']

    def perform_clustering(self, texts: List[str]) -> np.ndarray:
        """Vectorize texts and perform K-Means clustering."""
        if not texts:
            return np.array([])
            
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        clusters = self.kmeans.fit_predict(tfidf_matrix)
        return clusters

    def get_cluster_keywords(self, top_n: int = 5) -> Dict[int, List[str]]:
        """Extract top keywords for each cluster based on centroid distance."""
        centroids = self.kmeans.cluster_centers_
        terms = self.vectorizer.get_feature_names_out()
        
        cluster_keywords = {}
        for i in range(self.n_clusters):
            # Sort indices of centroid by weight
            top_term_indices = centroids[i].argsort()[::-1][:top_n]
            cluster_keywords[i] = [terms[idx] for idx in top_term_indices]
            
        return cluster_keywords

    def generate_theme_name(self, keywords: List[str]) -> str:
        """Use Gemini to dynamically generate a theme name from keywords."""
        try:
            import google.generativeai as genai
            import os
            api_key = os.environ.get("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                model_name = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
                model = genai.GenerativeModel(model_name)
                prompt = f"Given these review keywords: {', '.join(keywords)}. Generate a short, catchy, 1-4 word theme name that summarizes them. Only return the theme name, no quotes or extra text."
                response = model.generate_content(prompt)
                name = response.text.strip()
                # Remove quotes if the model added them
                if name.startswith('"') and name.endswith('"'):
                    name = name[1:-1]
                return name
        except Exception as e:
            print(f"Error generating theme name with Gemini: {e}")
            
        # Fallback to keyword concatenation if Gemini fails
        return " / ".join([k.capitalize() for k in keywords[:2]])
