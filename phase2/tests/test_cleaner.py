import pytest
from phase2.src.agent.cleaner import ReviewCleaner

@pytest.fixture
def cleaner():
    return ReviewCleaner()

def test_clean_text_basic(cleaner):
    assert cleaner.clean_text("Hello World!") == "hello world!"
    assert cleaner.clean_text("   Extra   Whitespace   ") == "extra whitespace"

def test_clean_text_emojis(cleaner):
    assert cleaner.clean_text("Best app ever! 🔥🚀") == "best app ever!"
    assert cleaner.clean_text("Love it ❤️❤️") == "love it"

def test_clean_text_special_chars(cleaner):
    assert cleaner.clean_text("What is this? @#$") == "what is this?"
    assert cleaner.clean_text("Price is $100") == "price is 100"

def test_redact_pii_email(cleaner):
    text = "Contact me at test@example.com"
    assert cleaner.redact_pii(text) == "Contact me at [REDACTED_EMAIL]"

def test_redact_pii_phone(cleaner):
    text = "Call me at 123-456-7890"
    assert cleaner.redact_pii(text) == "Call me at [REDACTED_PHONE]"

def test_is_spam(cleaner):
    assert cleaner.is_spam("Great") == True  # too short (1 word)
    assert cleaner.is_spam("Best app ever") == False
    assert cleaner.is_spam("aaaaaaaaaaaa") == True  # repetition

def test_full_pipeline(cleaner):
    text = "WOW! Best app ever! 🔥 Contact me at john@doe.com"
    result = cleaner.process(text)
    assert "wow!" in result
    assert "best app ever!" in result
    assert "[redacted_email]" in result  # processed to lower
    assert "🔥" not in result
