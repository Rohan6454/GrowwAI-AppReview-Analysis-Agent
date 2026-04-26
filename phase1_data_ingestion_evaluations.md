# Phase 1: Data Ingestion - Evaluations & Quality Checks

## Success Metrics

### Data Quality
- ✓ 100% of required fields (rating, title, text, date, source) successfully imported
- ✓ Zero data loss: all valid reviews ingested into database
- ✓ No corrupted or truncated review text
- ✓ Dates preserved in original format

### System Performance
- ✓ Ingest 20+ reviews in < 1 second
- ✓ Provide detailed error reporting for invalid rows
- ✓ Handle CSV files up to 100MB
- ✓ Database connection pooling for efficiency

### Data Validation
- ✓ 100% of reviews have valid ratings (1-5)
- ✓ 100% of reviews have non-empty title and text
- ✓ 100% of reviews have valid source (Google Play Store or Apple App Store)
- ✓ Duplicate reviews detected and handled

## Quality Checks

### Pre-Ingestion Checks
- [ ] CSV file exists and is readable
- [ ] CSV has required column headers
- [ ] CSV is not corrupted or malformed
- [ ] Data encoding is UTF-8

### Row-Level Validation
- [ ] Rating field is numeric and in range [1, 5]
- [ ] Review title is non-empty string
- [ ] Review text is non-empty string
- [ ] Review date is non-empty string
- [ ] Source is "Google Play Store" or "Apple App Store"
- [ ] No null/missing fields in required columns

### Database Validation
- [ ] Reviews table exists and has correct schema
- [ ] All successfully validated reviews inserted
- [ ] Duplicate reviews detected and skipped
- [ ] Metadata field properly formatted and stored
- [ ] Database transaction commits successfully

### Statistics Validation
- [ ] Total count = loaded count
- [ ] Inserted + skipped + errors = total
- [ ] Error messages are specific and actionable

## Agent Rules (Anti-Hallucination)

1. **Data Accuracy**: Do NOT modify review content during ingestion
   - Store original review text verbatim
   - Do NOT auto-correct spelling or grammar
   - Do NOT interpret emoji or special characters

2. **Source Attribution**: Do NOT invent source information
   - Only use "Google Play Store" or "Apple App Store"
   - Do NOT create new source types
   - Preserve source metadata in database

3. **Rating Integrity**: Do NOT adjust or normalize ratings
   - Store ratings as provided (1-5)
   - Do NOT convert decimal ratings to integers
   - Do NOT assume missing ratings

4. **Error Reporting**: Do NOT ignore or hide ingestion errors
   - Report every invalid row with specific error
   - Include row number in error details
   - Do NOT skip silent failures

5. **Metadata Preservation**: Do NOT lose metadata during ingestion
   - Store review title, date, and source
   - Format metadata consistently in database
   - Do NOT merge or deduplicate reviews by content

## Testing Approach

### Unit Tests
- Test Review model validation with valid and invalid data
- Test CSV adapter with well-formed and malformed CSV
- Test database ingestion with various data scenarios
- Test error handling and reporting

### Integration Tests
- Test complete CSV to database pipeline
- Verify data integrity after ingestion
- Verify statistics calculation
- Test with provided sample datasets

### Performance Tests
- Measure ingestion time for 20 reviews
- Verify database query performance
- Test with various file sizes

### Error Scenario Tests
- Missing CSV file
- Malformed CSV structure
- Invalid field values
- Database connection failures
- Duplicate reviews

## Deliverable Validation

### Code Artifacts
- [ ] `src/agent/review.py` - Review model with validation
- [ ] `src/agent/ingest.py` - CSV adapter and database ingester
- [ ] `tests/test_ingest.py` - Comprehensive test suite
- [ ] `docs/ingest_plan.md` - Implementation documentation
- [ ] `requirements.txt` - Phase 1 dependencies

### Functional Requirements
- [ ] CSV adapter successfully loads sample reviews
- [ ] Reviews pass validation checks
- [ ] Database ingestion inserts reviews correctly
- [ ] Statistics accurately reflect ingestion results
- [ ] All tests pass without errors

### Non-Functional Requirements
- [ ] Code follows PEP 8 conventions
- [ ] Error messages are clear and actionable
- [ ] Test coverage > 80% for core functions
- [ ] Documentation is complete and accurate

## Exit Criteria
- ✓ All tests pass: `pytest tests/test_ingest.py -v`
- ✓ Sample datasets successfully ingested (20 reviews)
- ✓ Database populated with ingested reviews
- ✓ Error handling verified for edge cases
- ✓ No data loss or corruption detected
- ✓ Ready for Phase 2: Data Cleaning
