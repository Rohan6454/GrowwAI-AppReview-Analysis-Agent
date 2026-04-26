"""Module for MCP integration points."""

import os
import sys

# Add mcp-server to path so we can import the tools
mcp_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'mcp-server')
sys.path.append(os.path.abspath(mcp_dir))

from docs_tool import append_to_doc
from gmail_tool import create_email_draft

def append_to_google_doc(doc_id: str, content: str):
    """Append content to a Google Doc via MCP."""
    print(f'Appending content to Google Doc {doc_id} via real MCP connector')
    return append_to_doc(doc_id, content)

def create_gmail_draft(to: str, subject: str, body: str, is_html: bool = False):
    """Create a Gmail draft via MCP."""
    print(f'Creating Gmail draft to {to} with subject: {subject} via real MCP connector (HTML: {is_html})')
    return create_email_draft(to, subject, body, is_html=is_html)
