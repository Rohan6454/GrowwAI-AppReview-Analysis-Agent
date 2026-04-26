# Phase 2: Data Cleaning and Normalization - Edge Cases

## PII and Privacy Edge Cases
- **Embedded PII:** User mentions their own email/phone in review text
- **Contextual PII:** Names of other people or companies mentioned in reviews
- **Location Data:** Reviews containing city names, addresses, or GPS coordinates
- **Account Information:** References to user IDs, transaction IDs, or account numbers
- **PII in Different Languages:** Personal information in non-English reviews

## Text Quality Edge Cases
- **All Emojis:** Reviews consisting entirely of emojis with no text
- **Single Character Reviews:** Reviews with just "Good" or "Bad"
- **Extremely Long Reviews:** 10,000+ character reviews with formatting issues
- **Mixed Languages:** Reviews switching between multiple languages
- **Code or Technical Content:** Reviews containing code snippets or technical jargon

## Duplicate and Spam Scenarios
- **Near-Duplicates:** Slightly modified versions of the same review
- **Bot-Generated Reviews:** Pattern-based spam reviews
- **Copy-Paste Reviews:** Same text posted multiple times
- **Translated Duplicates:** Same review translated to different languages
- **Review Templates:** Users filling out review templates with similar structure

## Encoding and Formatting Issues
- **Corrupted Characters:** Text with encoding errors or replacement characters
- **Special Characters:** Mathematical symbols, currency symbols, or Unicode art
- **Line Breaks and Formatting:** Reviews with excessive line breaks or markdown-like formatting
- **HTML Entities:** Reviews containing HTML tags or entities
- **Non-Text Content:** Reviews with URLs, hashtags, or @mentions

## Content Filtering Challenges
- **Ambiguous Content:** Reviews that could be spam or legitimate but hard to classify
- **Cultural Context:** Content that seems inappropriate but is culturally specific
- **Sarcasm Detection:** Sarcastic reviews that appear positive but are negative
- **Context-Dependent Meaning:** Words that change meaning based on context
- **Evolving Language:** New slang, memes, or internet culture references
- **Cleaning Hallucination Risk:** Do not invent meaning, sentiment, or missing content during normalization.

## Processing Edge Cases
- **Empty Dataset:** No reviews to clean
- **All Identical Reviews:** Every review is exactly the same text
- **Memory Constraints:** Very large dataset that exceeds available memory
- **Time-Sensitive Processing:** Need to clean reviews in real-time as they arrive
- **Incremental Updates:** Adding new reviews to already cleaned dataset