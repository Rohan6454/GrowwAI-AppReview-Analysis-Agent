# Phase 3: Theme Clustering and Sentiment Analysis

This folder contains documentation for Phase 3 of the App Review Insights Analyzer AI agent.

## Purpose
Use AI-assisted semantic grouping and sentiment analysis to cluster reviews into up to five interpretable themes.

## MCP relevance
Phase 3 generates the core insights that will later populate the Google Doc report and Gmail draft.

## Hallucination rules
- Derive theme labels directly from source review text and sentiment evidence.
- Do not invent themes or label clusters without supporting review content.
- If the review set lacks sufficient evidence for a clear theme, surface that limitation instead of forcing a theme.

## Current contents
- phase3_theme_clustering_evaluations.md
- phase3_theme_clustering_edge_cases.md
