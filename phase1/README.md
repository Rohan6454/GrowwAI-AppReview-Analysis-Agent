# Phase 1: Data Ingestion

## Overview
Phase 1 implements data ingestion for the Groww app reviews from Google Play Store and Apple App Store. The phase focuses on building reliable CSV import adapters and establishing a foundation for subsequent data processing phases.

This folder contains documentation for Phase 1 of the App Review Insights Analyzer AI agent.

## Purpose
Collect public app reviews from Google Play Store and Apple App Store for the last 8-12 weeks, validate required fields, and preserve original source data for downstream AI analysis.

## MCP relevance
Phase 1 is upstream of MCP-driven report and Gmail workflow. It feeds the agent with reliable review data before AI analysis begins.

## Hallucination rules
- Only ingest reviews from public sources; do not fabricate reviews or review metadata.
- Do not fill missing fields with guessed content; invalid entries must be flagged and excluded.
- Preserve source review text and metadata without inventing additional information.

## Current contents
- phase1_data_ingestion_evaluations.md
- phase1_data_ingestion_edge_cases.md
