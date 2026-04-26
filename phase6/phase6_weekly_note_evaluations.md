# Phase 6: Weekly Note Generation - Evaluations

## Success Metrics
- **Word Count Compliance:** 100% of reports are ≤250 words
- **Content Completeness:** All reports include top 3 themes, 3 quotes, and 3 actions
- **Readability Score:** Executive-friendly tone with appropriate technical level
- **Formatting Quality:** Clean, scannable Markdown formatting
- **Google Docs Append Success:** Report is appended to the target Google Doc without duplication or formatting loss
- **Generation Speed:** Create report within 30 seconds
- **Consistency:** Similar inputs produce consistent report structure

## Quality Checks
- **Theme Representation:** Top themes accurately reflected in report
- **Quote Integration:** Quotes are properly attributed and contextualized
- **Action Clarity:** Recommendations are clearly stated and prioritized
- **Executive Tone:** Non-technical language suitable for leadership
- **Scannability:** Report structure supports quick decision-making (<2 minutes)

## Agent Rules
- Summarize only the insights and actions produced by earlier phases; do not introduce new issues or invent extra findings.
- If a requested section cannot be populated with evidence, clearly indicate that fact rather than fabricate content.
- Maintain a traceable link between report sections and the underlying themes, quotes, and actions.

## Performance Benchmarks
- Handle reports with varying numbers of themes/quotes/actions
- Consistent formatting across different content types
- Memory efficient template processing
- Error-free generation for all input combinations

## Testing Approach
- Automated word count and structure validation
- Human readability and tone assessment
- Template rendering tests with edge case inputs
- Performance benchmarking
- Cross-browser Markdown rendering validation