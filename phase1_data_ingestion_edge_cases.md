# Phase 1: Data Ingestion - Edge Cases & Hallucination Prevention

## Edge Cases

### CSV Structure Edge Cases
1. **Empty CSV File**
   - Issue: CSV exists but has no data rows
   - Handling: Return empty reviews list, not an error
   - Test: Create CSV with only headers

2. **Missing Column Headers**
   - Issue: CSV has data but missing required columns
   - Handling: Raise error immediately, do not attempt to parse
   - Test: CSV missing 'source' column

3. **Extra Columns**
   - Issue: CSV has more columns than required
   - Handling: Ignore extra columns, parse required fields
   - Test: CSV with additional 'user_id' or 'platform' columns

4. **Unicode Characters in Reviews**
   - Issue: Review contains emoji, special characters, or multi-byte UTF-8
   - Handling: Preserve exactly as-is, do not strip or convert
   - Test: Reviews with 😊 emoji, Hindi characters, special symbols

5. **Very Long Review Text**
   - Issue: Review text exceeds typical string length
   - Handling: Store in full, truncate only if database has length limit
   - Test: 5000+ character review text

### Data Type Edge Cases
1. **Rating as Float**
   - Issue: Rating provided as 4.5 instead of 4
   - Handling: Convert to int or reject based on strictness requirement
   - Decision: For now, reject with error (maintain integer requirement)
   - Test: Rating = "4.5"

2. **Rating as String**
   - Issue: Rating provided as "5" instead of 5
   - Handling: Attempt to parse as integer, reject if invalid
   - Test: Rating = "five"

3. **Date Formats**
   - Issue: Different date formats (2024-04-20 vs 04/20/2024 vs 20-04-2024)
   - Handling: Store as-is without normalization (Phase 2 job)
   - Do NOT assume or correct date format
   - Test: Mixed date formats

4. **Empty String Fields**
   - Issue: Field present but value is empty or whitespace only
   - Handling: Treat as missing, skip row with error
   - Test: Rating present but empty: "rating,review_title,review_text,review_date,source\n,title,text,date,source"

### Source Edge Cases
1. **Invalid Source String**
   - Issue: Source is "Google Play" instead of "Google Play Store"
   - Handling: Reject row with error, do NOT auto-correct
   - Do NOT invent variations like "GPStore" or "GooglePlay"
   - Test: Source = "Google Play" (missing "Store")

2. **Case Sensitivity**
   - Issue: Source is "google play store" (lowercase)
   - Handling: Reject as invalid (must match exactly), do NOT normalize
   - Test: Source = "google play store"

3. **Whitespace in Source**
   - Issue: Source has leading/trailing spaces: " Google Play Store "
   - Handling: Strip whitespace, then validate (reasonable parsing)
   - Test: Source = " Apple App Store "

### Metadata Preservation Edge Cases
1. **Title with Special Formatting**
   - Issue: Title contains newlines, tabs, or multiple spaces
   - Handling: Preserve as-is, do NOT normalize whitespace
   - Test: Title = "Great\nApp\nEver"

2. **Review Date Precision**
   - Issue: Date includes time information: "2024-04-20 14:30:00"
   - Handling: Store as-is, do NOT extract only date portion
   - Test: Date = "2024-04-20T14:30:00Z"

3. **Duplicate Reviews Across Sources**
   - Issue: Same review text appears in both Google Play Store and Apple App Store datasets
   - Handling: Insert as separate reviews (not duplicates at ingestion level)
   - Do NOT merge reviews from different sources
   - Test: Identical review text with source=Google Play Store and source=Apple App Store

### Database Edge Cases
1. **Database Does Not Exist**
   - Issue: Database file path provided but database not initialized
   - Handling: Raise error with clear message about missing schema
   - Do NOT attempt to create database automatically
   - Test: Pass non-existent database path without schema

2. **Database Table Does Not Exist**
   - Issue: Database exists but reviews table not created
   - Handling: Raise error, do NOT create table automatically
   - Do NOT invent schema
   - Test: Database with no tables

3. **Database Locked/Read-Only**
   - Issue: Database file exists but cannot be written to
   - Handling: Raise error about permissions/lock
   - Test: Read-only database file

4. **Constraint Violation**
   - Issue: Review fails unique constraint or foreign key constraint
   - Handling: Skip review, increment skipped count, do NOT raise error
   - Test: Duplicate reviews in CSV

### Batch Size Edge Cases
1. **Single Review**
   - Issue: CSV with only one data row
   - Handling: Process normally, return stats with count=1
   - Test: CSV with 1 review

2. **Large Batch (1000+ reviews)**
   - Issue: CSV with many reviews
   - Handling: Process in batches to manage memory
   - Test: CSV with 1000 reviews

3. **Batch with Partial Failures**
   - Issue: Some reviews valid, some invalid in same batch
   - Handling: Ingest valid ones, skip invalid ones, report all errors
   - Do NOT fail entire batch on single error
   - Test: CSV with 10 reviews, 3 invalid

## Hallucination Prevention Rules

### Do NOT:
1. **Invent missing data**: If review text is missing, do NOT generate placeholder text
2. **Modify source attribution**: Do NOT change source or add unspecified sources
3. **Normalize data during ingestion**: Do NOT correct spellings, normalize dates, or adjust ratings
4. **Create database schema**: Do NOT auto-create tables or columns
5. **Assume date formats**: Do NOT parse or convert dates; store as-is
6. **Skip silent errors**: Do NOT ignore rows without reporting
7. **Merge duplicate records**: Do NOT deduplicate or combine reviews
8. **Invent metadata**: Do NOT add fields not present in source data

### Do:
1. **Report errors explicitly**: Every failed row must appear in error list
2. **Preserve data exactly**: Store content verbatim from CSV
3. **Validate strictly**: Reject invalid data with clear error messages
4. **Track statistics**: Report inserted, skipped, and error counts accurately
5. **Maintain source integrity**: Keep source attribution and metadata intact

## Testing Edge Cases

### CSV Parsing Tests
```python
# Test 1: Empty CSV
csv_content = "rating,review_title,review_text,review_date,source\n"
# Expected: empty reviews list, no errors

# Test 2: Unicode characters
csv_content = "5,Great 😊,Amazing app 🚀,2024-04-20,Google Play Store\n"
# Expected: preserve emoji, store exactly

# Test 3: Long review text
csv_content = "5,Great,{very long text...},2024-04-20,Apple App Store\n"
# Expected: store full text, no truncation
```

### Validation Tests
```python
# Test 4: Invalid rating
csv_content = "10,Great,Nice app,2024-04-20,Google Play Store\n"
# Expected: error, skip row, rating out of range

# Test 5: Missing source
csv_content = "5,Great,Nice app,2024-04-20,\n"
# Expected: error, skip row, empty source field

# Test 6: Invalid source
csv_content = "5,Great,Nice app,2024-04-20,Facebook\n"
# Expected: error, skip row, do NOT normalize to "Social Media"
```

### Data Integrity Tests
```python
# Test 7: Duplicate reviews
csv_content = """rating,review_title,review_text,review_date,source
5,Great,Nice app,2024-04-20,Google Play Store
5,Great,Nice app,2024-04-20,Google Play Store
"""
# Expected: both inserted (ingestion level doesn't deduplicate)

# Test 8: Whitespace handling
csv_content = "5, Great , Nice app ,2024-04-20,  Google Play Store  \n"
# Expected: source stripped, content preserved with leading spaces in title/text
```

## Known Limitations

1. **No Date Normalization**: Dates stored as-is (Phase 2 responsibility)
2. **No Text Normalization**: Spelling/grammar not corrected (Phase 2 responsibility)
3. **No Rating Conversion**: Decimal ratings rejected (Phase 2 may handle if needed)
4. **No Deduplication**: Duplicate records ingested separately (Phase 2 responsibility)
5. **No PII Detection**: PII not filtered during ingestion (Phase 2 responsibility)

## Phase Handoff
- **Input to Phase 2**: Full ingested dataset with all metadata preserved
- **Assumption for Phase 2**: Database reviews table fully populated with raw data
- **No modifications**: All data passes through unchanged during ingestion
