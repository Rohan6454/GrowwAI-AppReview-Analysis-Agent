"""
Review data model for Phase 1: Data Ingestion.
Defines the Review class and validation logic.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Review:
    """Represents a single app review."""
    
    rating: int
    review_title: str
    review_text: str
    review_date: str
    source: str  # 'Google Play Store' or 'Apple App Store'
    app: str = "Groww"
    
    def __post_init__(self):
        """Validate review data after initialization."""
        self.validate()
    
    def validate(self):
        """Validate review fields meet requirements."""
        if not isinstance(self.rating, (int, float)) or not (1 <= self.rating <= 5):
            raise ValueError(f"Rating must be between 1-5, got {self.rating}")
        
        if not isinstance(self.review_title, str) or len(self.review_title) == 0:
            raise ValueError("Review title must be a non-empty string")
        
        if not isinstance(self.review_text, str) or len(self.review_text) == 0:
            raise ValueError("Review text must be a non-empty string")
        
        if not isinstance(self.review_date, str) or len(self.review_date) == 0:
            raise ValueError("Review date must be a non-empty string")
        
        if self.source not in ["Google Play Store", "Apple App Store"]:
            raise ValueError(f"Source must be 'Google Play Store' or 'Apple App Store', got {self.source}")
    
    def to_dict(self):
        """Convert review to dictionary."""
        return {
            'rating': self.rating,
            'review_title': self.review_title,
            'review_text': self.review_text,
            'review_date': self.review_date,
            'source': self.source,
            'app': self.app
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Review':
        """Create Review from dictionary."""
        return cls(
            rating=int(data.get('rating')),
            review_title=str(data.get('review_title', '')).strip(),
            review_text=str(data.get('review_text', '')).strip(),
            review_date=str(data.get('review_date', '')).strip(),
            source=str(data.get('source', '')).strip(),
            app=str(data.get('app', 'Groww')).strip()
        )
