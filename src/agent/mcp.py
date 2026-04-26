"""Module for MCP integration points."""

import os
import sys

# Add mcp-server to path so we can import the tools
mcp_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'mcp-server')
sys.path.append(os.path.abspath(mcp_dir))

from docs_tool import append_to_doc
try:
    from gmail_tool import create_email_draft, send_email
except ImportError:
    # If run outside mcp-server dir
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'mcp-server'))
    try:
        from gmail_tool import create_email_draft, send_email
    except ImportError:
        create_email_draft = lambda to, subject, body, is_html=False: {"status": "error", "message": "gmail_tool not found"}
        send_email = lambda to, subject, body, is_html=False: {"status": "error", "message": "gmail_tool not found"}

def append_to_google_doc(doc_id: str, content: str):
    """Append content to a Google Doc via MCP."""
    print(f'Appending content to Google Doc {doc_id} via real MCP connector')
    return append_to_doc(doc_id, content)

def create_gmail_draft(to: str, subject: str, body: str, is_html: bool = False):
    """Create a Gmail draft via MCP."""
    print(f'Creating Gmail draft to {to} with subject: {subject} via real MCP connector (HTML: {is_html})')
    return create_email_draft(to, subject, body, is_html=is_html)


def send_gmail_email(to: str, subject: str, body: str, is_html: bool = False):
    """Send a Gmail email via MCP."""
    print(f'Sending Gmail email to {to} with subject: {subject} via real MCP connector (HTML: {is_html})')
    return send_email(to, subject, body, is_html=is_html)
