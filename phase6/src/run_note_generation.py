import os
import sys
import json
from dotenv import load_dotenv

# Add project root to sys path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from phase6.src.generator import WeeklyNoteGenerator
from src.agent.mcp import append_to_google_doc

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def main():
    # Load env vars
    load_dotenv(os.path.join(BASE_DIR, '.env'))
    
    data_dir = os.path.join(BASE_DIR, 'data')
    themes_path = os.path.join(data_dir, 'theme_summary.json')
    quotes_path = os.path.join(data_dir, 'selected_quotes.json')
    actions_path = os.path.join(data_dir, 'action_recommendations.json')
    report_path = os.path.join(data_dir, 'weekly_report.md')
    
    print("Loading data...")
    themes = load_json(themes_path)
    quotes = load_json(quotes_path)
    actions = load_json(actions_path)
    
    print("Generating weekly report using Gemini...")
    generator = WeeklyNoteGenerator()
    report_content = generator.generate_report(themes, quotes, actions)
    
    print("Saving report locally...")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    # Word count validation
    word_count = len(report_content.split())
    print(f"Report generated. Word count: {word_count}")
    if word_count > 300: # allow slight buffer for LLM inaccuracy
        print("Warning: Report might exceed the 250 words limit.")
        
    doc_id = os.environ.get("MCP_GOOGLE_DOCS_DOC_ID")
    if doc_id:
        print(f"Appending to Google Doc ID: {doc_id}")
        # The append_to_doc script expects token.json to be in current directory
        cwd = os.getcwd()
        try:
            mcp_server_dir = os.path.join(BASE_DIR, 'mcp-server')
            os.chdir(mcp_server_dir)
            result = append_to_google_doc(doc_id, report_content)
            print("Google Docs API Result:", result)
        except Exception as e:
            print(f"Error appending to Google Doc: {e}")
        finally:
            os.chdir(cwd)
    else:
        print("Skipping Google Docs append: MCP_GOOGLE_DOCS_DOC_ID is not set.")

if __name__ == "__main__":
    main()
