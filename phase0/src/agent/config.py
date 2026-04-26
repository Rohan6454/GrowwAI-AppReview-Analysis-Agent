import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, '..', '..', '..', 'data')
DEFAULT_DB_PATH = os.path.join(BASE_DIR, '..', '..', '..', 'data', 'reviews.db')

MCP_GOOGLE_DOCS_DOC_ID = os.environ.get('MCP_GOOGLE_DOCS_DOC_ID', '')
MCP_GMAIL_DRAFT_LABEL = os.environ.get('MCP_GMAIL_DRAFT_LABEL', 'App Review Insights')

REVIEW_FIELDS = ['rating', 'review_title', 'review_text', 'review_date']
