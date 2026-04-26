# Phase 2: Data Cleaning and Normalization

This folder contains documentation for Phase 2 of the App Review Insights Analyzer AI agent.

## Purpose
Clean and normalize review text while removing noise and PII, preparing the data for AI-driven theme analysis and report generation.

## MCP relevance
Phase 2 ensures the agent operates on trustworthy, privacy-safe text before moving into the AI analysis pipeline and Google Docs/Gmail outputs.

## Hallucination rules
- Clean only by removing noise and normalizing formatting; do not invent or infer missing user intent or content.
- Redact PII without adding new information or changing meaning.
- Preserve ambiguous review text instead of rewriting it into something the source does not support.

## Current contents
- phase2_data_cleaning_evaluations.md
- phase2_data_cleaning_edge_cases.md
