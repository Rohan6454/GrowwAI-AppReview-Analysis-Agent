🧩 Problem Statement: App Review Insights Analyzer (Groww)

1. Background & Context
Groww is a fast-growing investment platform where user experience directly impacts trust, retention, and revenue. Every week, thousands of users leave feedback on platforms like the Google Play Store and Apple App Store.

However, this feedback is:
Unstructured
High volume
Scattered across platforms
Difficult to manually analyze at scale

As a result, critical product insights often:
Get missed
Are discovered too late
Lack prioritization context

2. Core Problem
How might we automatically transform raw app reviews into structured, actionable product insights—on a weekly basis—without manual effort?

More specifically:
Product, Growth, and Leadership teams lack a reliable, fast, and standardized way to understand user sentiment, identify recurring issues, and decide what to fix next.

3. Objective
Build an AI-powered insights agent that:
Collects recent app reviews (last 8–12 weeks)
Identifies key themes (max 5)
Extracts representative user quotes
Recommends actionable improvements
Outputs a concise, decision-ready weekly report
Automatically drafts an email summary

4. Key Inputs
Data Sources (Strict Constraint-Compliant)
Google Play Store public reviews (exportable datasets)
Apple App Store public reviews (via APIs or datasets)
Data Fields Required
Rating (1–5)
Review title
Review text
Date

5. Core Functional Requirements

A. Data Ingestion Layer
Import reviews from past 8–12 weeks
Accept CSV / API input
Clean & normalize text (remove noise, emojis if needed)

B. Insight Generation Engine (Core AI Layer)
    1. Theme Clustering
Group reviews into maximum 5 themes
Themes should be:
Mutually exclusive (as much as possible)
Interpretable (e.g., “KYC Issues”, not “Cluster 1”)
    2. Sentiment-Aware Prioritization
Identify which themes matter most based on:
Volume
Negative sentiment weight
Recency
    3. Quote Extraction
Select 3 high-quality user quotes
Must be:
Specific
Representative of themes
Cleaned (no PII)
    4. Action Recommendation
Generate 3 product action ideas
Should be:
Concrete (not vague like “Improve UX”)
Insight-backed
Prioritized

C. Weekly Note Generator
Generate a ≤250-word one-page report containing:
Top 3 themes
3 user quotes
3 action ideas

Tone:
Crisp
Executive-friendly
Non-technical

D. Email Draft Generator
Convert the weekly note into a structured email
Include:
Subject line
Summary body
No actual sending required (draft is enough)

6. Output Requirements
    
    1. Weekly Insight Note
Format: Markdown / PDF / Doc
Constraints:
≤250 words
Clean formatting
No PII

    2. Email Draft
Professional tone
Ready-to-send format

    3. Dataset
CSV of reviews used
Redacted if necessary

    4. README
Must include:
Steps to re-run weekly pipeline
Theme definitions
Assumptions

7. Non-Functional Requirements
Privacy-first → No usernames, emails, IDs
Explainability → Themes + quotes must clearly align
Consistency → Same input → similar output structure
Speed → Should run within minutes
Reusability → Easy weekly rerun

8. Constraints
Only public data sources
No scraping behind login walls
Max 5 themes
Output must be scannable
No hallucinated insights

9. Success Metrics
Define success like a PM:
Output Quality
Themes are meaningful & distinct
Quotes clearly support themes
Actions are implementable
Efficiency
Time saved vs manual analysis
Usability
Can a PM make a decision in <2 minutes?

10. End-to-End Workflow
Import → Clean → Cluster → Extract → Summarize → Generate Actions → Draft Email

11. Key Risks & Challenges
Noisy / short reviews
Duplicate feedback
Theme overlap
LLM hallucination
Weak action recommendations

12. What Makes This “Irreplaceable” Level
To truly stand out, your system should:
Use real data pipelines (not mock data)
Show traceability (quote → theme → action)
Demonstrate product thinking, not just AI output
Include clear prioritization logic