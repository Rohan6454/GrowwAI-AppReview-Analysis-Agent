# Phase 4: Quote Extraction

This folder contains documentation for Phase 4 of the App Review Insights Analyzer AI agent.

## Purpose
Select representative, high-quality quotes from reviews that support the identified themes and can be included in the Google Doc report.

## MCP relevance
Phase 4 provides the evidence quotes that make the report credible and traceable in the MCP-generated Google Doc.

## Hallucination rules
- Extract quotes as exact excerpts from source reviews; do not paraphrase or invent quote details.
- Exclude quotes containing PII; if no clean quote exists, note that rather than create one.
- Ensure each quote is traceable to its originating review.

## Current contents
- phase4_quote_extraction_evaluations.md
- phase4_quote_extraction_edge_cases.md
