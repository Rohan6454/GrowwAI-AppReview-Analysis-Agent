import os
import json
import google.generativeai as genai

class WeeklyNoteGenerator:
    """Generates an executive weekly note using Gemini."""

    def __init__(self):
        # API key should be loaded from environment by dotenv in the main script
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing.")
        genai.configure(api_key=api_key)
        
        # Use gemini-2.5-flash for summarization task
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_report(self, themes: list, quotes: list, actions: list) -> str:
        """
        Generates a concise markdown report using LLM.
        """
        prompt = f"""
You are a top-tier Product Manager. Based on the following user review analysis, write a concise weekly insight report (maximum 250 words) formatted in Markdown.

Data points to include:
- The top 5 themes from the reviews.
- 5 representative user quotes (Make sure to highlight reviews where the sentiment is tough/critical to prompt stakeholders to make changes).
- 5 prioritized action recommendations based on those critical reviews.

Ensure the tone is executive-friendly but urgent regarding areas of improvement, and formatting is clean. Do NOT include any PII.

THEMES:
{json.dumps(themes, indent=2)}

QUOTES:
{json.dumps(quotes, indent=2)}

ACTIONS:
{json.dumps(actions, indent=2)}

Please write the Markdown report now:
"""
        response = self.model.generate_content(prompt)
        return response.text
