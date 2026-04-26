# App Review Insights Analyzer

An MCP-based AI agent that ingests app reviews, processes them with AI-driven analysis, and publishes weekly insights to Google Docs and Gmail.

## Phase 0: Foundations & Scaffolding
This project scaffold includes:
- repository structure and documentation conventions
- SQLite schema for reviews and analysis metadata
- CLI command skeleton for ingestion, analysis, reporting, and delivery workflows
- CI workflow for linting and tests
- MCP integration planning documentation

## Getting started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Initialize the database:
   ```bash
   python -m agent.db --init data/reviews.db
   ```
3. Use the CLI for the agent workflow:
   ```bash
   python -m agent.cli ingest --source google_play --input reviews.csv
   ```

## Project layout
- `src/agent/`: agent code and CLI scaffold
- `docs/`: design and architecture documentation
- `phase0/`..`phase8/`: phase-specific documentation and requirements
- `.github/workflows/ci.yml`: CI configuration
