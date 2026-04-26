# Phase 8: Operational Runbook

## Overview
This runbook covers the operational details for the Weekly App Review Insights Pipeline, primarily focusing on its automated execution via GitHub Actions.

## Setting Up GitHub Actions
To successfully run the pipeline on GitHub, you must configure the following **Repository Secrets** in your GitHub repository settings (`Settings > Secrets and variables > Actions > New repository secret`):

1. `GOOGLE_API_KEY`: Your Gemini API Key.
2. `MCP_GOOGLE_DOCS_DOC_ID`: The ID of the Google Doc where the report will be appended.
3. `MCP_GMAIL_TO`: The email address that will receive the weekly drafts.
4. `MCP_GMAIL_SUBJECT`: The subject line for the email drafts.
5. `GOOGLE_TOKEN_JSON`: The complete raw JSON contents of your `mcp-server/token.json` file. This is crucial for authenticating securely with Google APIs in the cloud.

## Monitoring and Debugging
If the GitHub Action fails or you want to verify the output:
1. Navigate to the **Actions** tab in your GitHub repository.
2. Click on the specific workflow run.
3. Scroll down to the **Artifacts** section at the bottom of the summary page.
4. Download the `pipeline-log` artifact. This zip contains the `pipeline.log` file with exact timestamps, retry attempts, and detailed error outputs for every step.

### Common Errors & Remediation
- **Token Expiry (`invalid_grant` or 401)**: The `GOOGLE_TOKEN_JSON` has expired or been revoked. You must re-run the local OAuth script (e.g., run `python mcp-server/auth.py` or any script importing it), complete the browser login to generate a new `token.json` locally, and then update the `GOOGLE_TOKEN_JSON` secret in GitHub.
- **API Quota Exceeded (429 Error)**: The pipeline has built-in retry logic (up to 3 retries with a 5-second delay). If it still fails and aborts, verify your API quotas in Google Cloud Console or Google AI Studio. Wait for the quota to reset and manually trigger the workflow using the `workflow_dispatch` button.
- **Model Not Found**: If Google deprecates or changes the Gemini model identifier, update the model string in `phase6/src/generator.py` and push the change.
