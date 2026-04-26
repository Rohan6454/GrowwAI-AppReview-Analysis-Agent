# Architecture Overview: App Review Insights Analyzer

## Architecture Summary
The App Review Insights Analyzer is designed as an MCP-based AI agent that orchestrates review analysis, report generation, and stakeholder communication.

Core components:
- Data ingestion layer for review collection from Google Play Store and Apple App Store
- Cleaning and normalization layer for text preprocessing and PII redaction
- AI-driven analysis layer for theme clustering, sentiment scoring, quote extraction, and action recommendation
- Output generation layer for executive insights reports and email drafts
- MCP connectors for Google Docs and Gmail integration

## High-Level Flow
0. **Foundations & Scaffolding**
   - Establish repo structure, schema, CLI, and CI/CD
   - Define MCP integration points for Google Docs and Gmail

1. **Data Ingestion**
   - Collect review data from public CSV/API sources for the last 8-12 weeks
   - Validate required fields: rating, title, text, date

2. **Data Cleaning and Normalization**
   - Remove noise, emojis, and PII
   - Handle duplicates, encoding issues, and spam filtering

3. **AI Analysis**
   - Cluster reviews into up to 5 themes using semantic grouping
   - Apply sentiment-aware prioritization using volume, recency, and sentiment
   - Extract representative quotes and identify key themes

4. **Action Recommendation**
   - Use AI prompt engineering to generate concrete, prioritized product actions
   - Validate actions against themes and quote evidence

5. **Report Generation**
   - Create a concise executive summary report (≤250 words)
   - Append the report to a Google Doc via MCP

6. **Email Drafting**
   - Generate a structured Gmail draft through MCP for stakeholder sharing
   - Include subject, summary, and actionable next steps

7. **Orchestration, Scheduling & Hardening**
   - Schedule weekly runs and manage execution
   - Add observability, retry logic, cost controls, and runbooks
   - Validate idempotent Google Docs and Gmail operations

## Key Integrations
- **MCP platform**: Orchestrates the agent workflow and service connectors
- **Google Docs**: Appends generated weekly reports
- **Gmail**: Creates email drafts for review distribution

## Phase Mapping
- Phase 0: Foundations and scaffolding
- Phase 1: Data ingestion
- Phase 2: Data cleaning and normalization
- Phase 3: Theme clustering and sentiment analysis
- Phase 4: Quote extraction
- Phase 5: Action recommendation generation
- Phase 6: Weekly note generation and Google Docs append
- Phase 7: Email draft generation via Gmail
- Phase 8: Orchestration, scheduling, and hardening

## Non-Functional Requirements
- Privacy-first data handling
- Explainable theme and quote traceability
- Fast processing within minutes
- Consistent outputs across repeated runs
- Safe, public-data-only collection

## Deployment Notes
- Use MCP server patterns for agent orchestration
- Connect Gmail and Google Docs through secure MCP connectors
- Keep the Google Doc append and Gmail draft steps idempotent to avoid duplicate content
