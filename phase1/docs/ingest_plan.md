# Phase 1: Data Ingestion - Implementation Plan

## Overview
This document provides detailed implementation guidance for Phase 1 data ingestion.

## Implementation Steps

### Step 1: Review Data Model
**File**: `src/agent/review.py`

Define a Review dataclass with:
- `rating` (int): 1-5 scale
- `review_title` (str): Review headline
- `review_text` (str): Review body
- `review_date` (str): Date review was posted
- `source` (str): "Google Play Store" or "Apple App Store"
- `app` (str): Default "Groww"

Include validation in `__post_init__`:
- Rating between 1-5
- Non-empty title, text, date
- Valid source value

### Step 2: CSV Data Adapter
**File**: `src/agent/ingest.py`

Implement `CSVDataAdapter` class:
- Load CSV files with pandas or csv module
- Validate presence of required columns
- Parse each row into Review objects
- Collect and report errors for invalid rows
- Return both valid reviews and error details

Required columns:
- rating
- review_title
- review_text
- review_date
- source

### Step 3: Database Ingestion
**File**: `src/agent/ingest.py`

Implement `DatabaseIngester` class:
- Connect to SQLite database
- Insert validated reviews into reviews table
- Map Review fields to database columns:
  - `rating` → reviews.rating
  - `review_text` → reviews.review_text
  - `review_date` → reviews.review_date
  - Metadata (title, source, app) → reviews.metadata as delimited string
- Track statistics: total, inserted, skipped, errors
- Handle duplicate reviews gracefully

### Step 4: End-to-End Pipeline
**File**: `src/agent/ingest.py`

Implement `ingest_csv_to_db()` function:
1. Load reviews from CSV using CSVDataAdapter
2. Validate loaded reviews
3. Ingest valid reviews using DatabaseIngester
4. Return comprehensive result dictionary with:
   - success (bool)
   - reviews_loaded (int)
   - load_errors (int)
   - ingestion_stats (dict)
   - errors (list)

### Step 5: Comprehensive Testing
**File**: `tests/test_ingest.py`

Implement tests for:
- **Review Model**:
  - Valid review creation
  - Invalid rating rejection
  - Empty field handling
  - Source validation
  - To/from dictionary conversion

- **CSV Adapter**:
  - Valid CSV loading
  - Missing fields detection
  - Non-existent file handling
  - Error collection and reporting

- **Database Ingestion**:
  - Review insertion
  - Empty dataset handling
  - Duplicate detection (if applicable)

- **End-to-End**:
  - CSV to database pipeline
  - Error aggregation
  - Statistics calculation

## Data Format Specification

### Input CSV Format
```
rating,review_title,review_text,review_date,source
5,Great app,Really enjoyed it,2024-04-20,Google Play Store
4,Good experience,Nice features,2024-04-19,Apple App Store
```

### Database Storage
```sql
INSERT INTO reviews (rating, review_text, review_date, metadata)
VALUES (5, 'Really enjoyed it', '2024-04-20', 'title:Great app|source:Google Play Store|app:Groww')
```

## Validation Rules

### Review Rating
- Type: Integer
- Range: 1-5
- Required: Yes

### Review Title
- Type: String
- Min length: 1 character
- Max length: 255 characters (recommended)
- Required: Yes

### Review Text
- Type: String
- Min length: 1 character
- Required: Yes

### Review Date
- Type: String (ISO format recommended: YYYY-MM-DD)
- Required: Yes

### Source
- Type: String
- Allowed values: "Google Play Store", "Apple App Store"
- Required: Yes

## Error Handling Strategy

### Load Errors
- Missing required columns → Fail fast with error message
- Missing field values → Record error, skip row
- Invalid data types → Record error, skip row

### Ingestion Errors
- Database connection failures → Log and raise exception
- Duplicate reviews → Skip and count as skipped
- Constraint violations → Log and continue

### Reporting
- Return all errors in result dictionary
- Include row number and specific error message
- Track statistics for success/failure analysis

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Use temporary files and in-memory databases
- Mock external dependencies
- Verify error handling paths

### Integration Tests
- Test end-to-end CSV to database flow
- Use real CSV files and temporary databases
- Validate data integrity after ingestion
- Verify statistics calculation

### Test Data
- Valid reviews with all fields populated
- Invalid reviews with missing fields
- Reviews with edge case values
- Large datasets for performance testing

## Performance Considerations

- Batch database inserts for large datasets
- Use prepared statements to prevent SQL injection
- Stream CSV parsing to handle large files
- Track and report processing time

## Security Considerations

- Validate CSV file before processing
- Use parameterized SQL queries
- Sanitize file paths
- Limit file size to prevent resource exhaustion

## Next Phase Dependencies
- Phase 2 depends on successfully ingested reviews in database
- Database schema must be initialized before ingestion (Phase 0 requirement)
- Sample data provided for testing (20 reviews from data/ directory)
