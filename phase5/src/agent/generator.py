from typing import List, Dict, Optional
import json

class RecommendationGenerator:
    """Generator for product action recommendations based on review analysis."""
    
    def __init__(self):
        # Action templates based on common theme keywords
        self.action_map = {
            "app": "Enhance overall app stability and performance during peak market hours.",
            "good": "Maintain current service levels and consider expanding feature set for experienced users.",
            "nice": "Refine UI micro-interactions to further improve user delight.",
            "easy": "Continue simplifying complex financial jargon and onboarding flows.",
            "use": "Optimize core user journeys to reduce clicks for common actions like order placement.",
            "login": "Investigate and resolve reported login failures and session timeout issues.",
            "trading": "Introduce advanced charting tools and indicators requested by the trading community.",
            "support": "Reduce customer support response times by implementing AI-driven first-response tools.",
            "charges": "Improve transparency around brokerage fees and hidden charges in the dashboard."
        }

    def generate_recommendations(self, themes: List[Dict], quotes: List[Dict]) -> List[Dict]:
        """Synthesize themes and quotes into concrete action recommendations."""
        recommendations = []
        
        # We take the top 5 themes for our 5 recommendations
        for i, theme in enumerate(themes[:5]):
            theme_name = theme['theme_name']
            keywords = theme['keywords']
            avg_sentiment = theme['average_sentiment']
            
            # Find a matching quote for this theme if available
            matching_quotes = [q for q in quotes if q['theme'] == theme_name]
            evidence_quote = matching_quotes[0]['quote'] if matching_quotes else "Based on general user feedback in this category."
            
            # Select the best action based on keywords
            action = self.action_map.get("app") # Default
            for kw in keywords:
                if kw.lower() in self.action_map:
                    action = self.action_map[kw.lower()]
                    break
            
            # Synthesize the insight
            sentiment_label = "positive" if avg_sentiment > 0.1 else "negative"
            insight = f"Users have a {sentiment_label} perception of '{theme_name}', highlighting keywords like {', '.join(keywords[:3])}."
            
            recommendations.append({
                'id': i + 1,
                'theme': theme_name,
                'insight': insight,
                'recommendation': action,
                'evidence': evidence_quote,
                'priority': 'High' if avg_sentiment < 0 else 'Medium'
            })
            
        return recommendations
