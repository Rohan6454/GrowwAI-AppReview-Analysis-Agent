import re
import emoji
from typing import Optional

class ReviewCleaner:
    """Utility class for cleaning and normalizing app reviews."""
    
    def __init__(self):
        # Regex for common PII patterns
        self.email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.phone_regex = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        # Regex for special characters but keep some punctuation
        self.spec_char_regex = re.compile(r'[^a-zA-Z0-9\s.,!?\'\[\]_]')

    def clean_text(self, text: str) -> str:
        """Perform basic text cleaning: emoji removal, case normalization, whitespace cleanup."""
        if not text or not isinstance(text, str):
            return ""
        
        # 1. Remove emojis
        text = emoji.replace_emoji(text, replace='')
        
        # 2. Normalize to lowercase
        text = text.lower()
        
        # 3. Remove non-standard characters (keep basic punctuation)
        text = self.spec_char_regex.sub(' ', text)
        
        # 4. Normalize whitespace
        text = ' '.join(text.split())
        
        return text.strip()

    def redact_pii(self, text: str) -> str:
        """Identify and redact PII like emails and phone numbers."""
        if not text:
            return ""
        
        # Redact emails
        text = self.email_regex.sub('[REDACTED_EMAIL]', text)
        
        # Redact phone numbers
        text = self.phone_regex.sub('[REDACTED_PHONE]', text)
        
        return text

    def is_spam(self, text: str) -> bool:
        """Heuristic check to identify potential spam or low-value reviews."""
        if not text:
            return True
        
        # Filter extremely short reviews
        words = text.split()
        if len(words) < 2:
            return True
        
        # Filter reviews with excessive character repetition (e.g., "aaaaaaa")
        if re.search(r'(.)\1{4,}', text):
            return True
            
        return False

    def process(self, text: str) -> Optional[str]:
        """Full pipeline processing."""
        # First redact PII to avoid cleaning stripping parts of it
        processed = self.redact_pii(text)
        # Then clean formatting
        processed = self.clean_text(processed)
        
        # Final check if it's still useful
        if self.is_spam(processed):
            return None
            
        return processed
