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
        
        model_name = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
        self.model = genai.GenerativeModel(model_name)

    def generate_report(self, themes: list, quotes: list, actions: list) -> str:
        """
        Generates a concise markdown report using LLM.
        """
        prompt = f"""
You are a top-tier Product Manager. Based on the following user review analysis, write a highly structured weekly insight report (maximum 300 words) formatted in Markdown.

FORMATTING REQUIREMENTS:
Do NOT write sentences that just list numbers (e.g., avoid "1. First theme is... 2. Second theme is..."). 
Instead, use a clear, easy-to-read structure with headings, bullet points, and blockquotes. Use exactly this structure:

### 🌟 Top Themes
(Use bullet points for the 5 themes, with a short bold title for each)

### 💬 Critical User Voices
(Use markdown blockquotes `>` for 5 representative tough/critical quotes, followed by a `- User` attribution)

### ⚡ Priority Action Items
(Use bullet points or checkboxes for the 5 recommended actions, keeping them actionable and concise)

Ensure the tone is executive-friendly but urgent regarding areas of improvement. Do NOT include any PII.

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
