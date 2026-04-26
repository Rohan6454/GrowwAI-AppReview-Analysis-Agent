# MCP Integration Plan

## Overview
This document defines the MCP integration points for the App Review Insights Analyzer AI agent.

## Google Docs Integration
- Purpose: append the generated weekly report to a Google Doc.
- Required connector: MCP Google Docs service.
- Data flow:
  1. Phase 6 generates the weekly report content.
  2. The agent calls the MCP connector to append a new section to the target Google Doc.
  3. The connector ensures idempotency to avoid duplicate sections.
- Config:
  - `MCP_GOOGLE_DOCS_DOC_ID`
  - target document identifier stored in environment or secrets

## Gmail Integration
- Purpose: create a Gmail draft for stakeholder communication.
- Required connector: MCP Gmail service.
- Data flow:
  1. Phase 7 generates the email subject and body.
  2. The agent calls the MCP connector to create a draft email.
  3. The draft remains editable and is not sent automatically.
- Config:
  - `MCP_GMAIL_DRAFT_LABEL`
  - optional recipient list and mailing metadata managed outside the agent

## Idempotency Rules
- Google Docs append should detect existing report sections and avoid duplicates.
- Gmail draft creation should avoid repeated duplicate drafts on retries.
- Phase 8 should validate retry behavior for both connectors.

## Security and Privacy
- Use MCP-managed credentials for Google Docs and Gmail access.
- Do not store Google or Gmail credentials in source control.
- Ensure no PII is written to the Google Doc or email draft.
