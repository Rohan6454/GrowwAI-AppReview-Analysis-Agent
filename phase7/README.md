# Phase 7: Email Draft Generation

This folder contains documentation for Phase 7 of the App Review Insights Analyzer AI agent.

## Purpose
Convert the weekly Google Docs report into a structured Gmail draft for stakeholder communication.

## MCP relevance
Phase 7 uses MCP Gmail integration to produce a ready-to-review email draft without sending it.

## Hallucination rules
- Draft email content only from the weekly report and source insights.
- Do not add new issues, recipients, approvals, or next steps that are not supported by the source report.
- If the report is incomplete, clearly state the limitation rather than fabricate details.

## Current contents
- phase7_email_draft_evaluations.md
- phase7_email_draft_edge_cases.md
