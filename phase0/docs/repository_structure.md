# Phase 0: Repository Structure

## Overview
This document defines the repository structure and conventions for the App Review Insights Analyzer project.

## Directory Structure
```
phase0/
├── README.md                          # Phase 0 overview and purpose
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
├── schema.sql                         # SQLite database schema
├── src/
│   └── agent/
│       ├── __init__.py               # Agent package init
│       ├── __main__.py               # CLI entry point
│       ├── config.py                 # Configuration and constants
│       ├── cli.py                    # CLI command implementation
│       ├── db.py                     # Database initialization and utilities
│       └── mcp.py                    # MCP integration stubs
├── tests/
│   └── test_cli.py                   # CLI tests
├── docs/
│   └── mcp_integration_plan.md       # MCP integration documentation
└── .github/
    └── workflows/
        └── ci.yml                    # CI/CD workflow
```

## Documentation Conventions
- README files should provide phase-specific overview and purpose
- Implementation details should be documented in the phase folder
- Test documentation should be in test files as docstrings
- Configuration options should be centralized in config.py

## Code Organization
- Agent code lives in `src/agent/`
- Tests live in `tests/`
- Phase-specific docs in `docs/`
- Each phase follows the same structure for consistency

## Dependencies
- Python 3.11+
- python-dotenv (for environment configuration)
- pytest (for testing)
- MCP libraries (TBD in later phases)

## Development Workflow
1. Install dependencies: `pip install -r requirements.txt`
2. Initialize database: `python -m agent init-db --db ../data/reviews.db`
3. Run tests: `pytest`
4. Use CLI commands for ingestion, cleaning, clustering, reporting, and email drafting

## Environment Configuration
Use a `.env` file in the phase0 root to set:
- `MCP_GOOGLE_DOCS_DOC_ID`: Target Google Doc ID
- `MCP_GMAIL_DRAFT_LABEL`: Gmail draft label for organizing insights emails
