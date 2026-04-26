# Phase 1: Data Ingestion - Evaluations

## Success Metrics
- **Data Collection Rate:** Successfully collect at least 90% of available reviews from the specified time window (8-12 weeks)
- **Data Completeness:** 100% of collected reviews contain all required fields (rating, title, text, date)
- **Date Range Accuracy:** All collected reviews fall within the 8-12 week window (no older/newer reviews)
- **Data Volume:** Minimum threshold of reviews collected (e.g., at least 100 reviews total across platforms)
- **Ingestion Speed:** Complete data collection within 5 minutes for typical volumes
- **Error Rate:** Less than 5% of ingestion attempts result in failures

## Quality Checks
- **Field Validation:** Automated checks confirm rating is 1-5, date is valid, text is not empty
- **Source Verification:** Reviews can be traced back to correct app store and app
- **Deduplication:** No duplicate reviews ingested (if detectable at this stage)
- **Format Consistency:** All data stored in consistent format (e.g., UTF-8 encoding)

## Agent Rules
- Only ingest reviews from validated public sources; do not fabricate reviews or review metadata.
- Do not generate review text or ratings for missing fields; invalid entries must be flagged and excluded.
- Preserve original source content without inference; downstream phases may normalize text but not invent new data.

## Performance Benchmarks
- Handle up to 10,000 reviews per ingestion run
- Memory usage stays within reasonable limits (<1GB for typical runs)
- API rate limits respected without failures

## Testing Approach
- Unit tests for data parsing and validation functions
- Integration tests with mock API responses
- End-to-end tests with sample datasets
- Load testing with large review volumes