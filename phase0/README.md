# Phase 0: Foundations & Scaffolding

This folder contains all foundations and scaffolding for the App Review Insights Analyzer AI agent.

## Purpose
Establish the repository structure, database schema, CLI scaffolding, CI/CD, and MCP integration plan needed to build the agent reliably.

## Deliverables
- ✅ Repository structure and documentation conventions
- ✅ SQLite database schema for reviews, themes, quotes, actions, reports, and email drafts
- ✅ CLI scaffolding for ingestion, cleaning, clustering, reporting, and email workflows
- ✅ CI configuration for linting and automated testing
- ✅ MCP integration planning documentation

## Structure
```
phase0/
├── src/agent/          # CLI and agent code scaffold
├── tests/              # Test suite for CLI
├── docs/               # Phase 0 documentation
├── schema.sql          # SQLite schema
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── .github/workflows/ # CI configuration
```

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Initialize database: `python -m agent init-db --db ../data/reviews.db`
3. Run tests: `pytest`
4. Use CLI: `python -m agent --help`

## MCP Relevance
Phase 0 defines the integration points and deployment foundations for Google Docs and Gmail connectivity through MCP stubs in `src/agent/mcp.py`.

## Documentation
- [Repository Structure](docs/repository_structure.md) - Project layout and conventions
- [MCP Integration Plan](docs/mcp_integration_plan.md) - Google Docs and Gmail connectivity
- [Evaluations](phase0_foundations_evaluations.md) - Success metrics and quality checks
- [Edge Cases](phase0_foundations_edge_cases.md) - Known challenges and mitigation

## Hallucination Rules
- Do not invent requirements or architecture components unsupported by project goals.
- Keep infrastructure design grounded in the actual agent workflow.
- All code scaffolding should serve the phase-based implementation plan.
