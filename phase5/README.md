# Phase 5: Action Recommendation Generation

This folder contains documentation for Phase 5 of the App Review Insights Analyzer AI agent.

## Purpose
Generate concrete, prioritized product actions that directly address the identified themes and user quotes.

## MCP relevance
Phase 5 produces the actionable recommendations that appear in the report saved to Google Docs and the email draft created in Gmail.

## Hallucination rules
- Only recommend actions supported by review themes and quotes.
- Do not invent product solutions or outcomes not evidenced by the source data.
- If evidence is insufficient, state that more review context is needed rather than fabricating an action.

## Current contents
- phase5_action_recommendation_evaluations.md
- phase5_action_recommendation_edge_cases.md
