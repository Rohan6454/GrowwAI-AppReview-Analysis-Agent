# Phase 5: Action Recommendation Generation - Evaluations

## Success Metrics
- **Action Concreteness:** 90% of recommendations are specific and actionable (not vague)
- **Implementability:** 85% of recommendations are feasible within product constraints
- **Theme Alignment:** 95% of recommendations directly address identified themes
- **Quote Support:** 90% of recommendations are supported by extracted quotes
- **Prioritization Logic:** Recommendations are ordered by impact and feasibility
- **Generation Speed:** Generate 3 recommendations within 2 minutes

## Quality Checks
- **Specificity:** Recommendations include concrete steps, not just high-level ideas
- **Measurable Outcomes:** Actions have clear success criteria or metrics
- **Resource Requirements:** Recommendations consider development time and effort
- **User Impact:** Actions address user pain points identified in reviews
- **Business Value:** Recommendations align with product goals and priorities

## Agent Rules
- Only generate actions that are directly supported by theme and quote evidence; do not hallucinate solutions.
- If there is insufficient support for an action, state that additional evidence is needed rather than inventing a recommendation.
- Keep actions grounded in the input data and avoid unrelated product suggestions.

## Performance Benchmarks
- Consistent recommendations across multiple runs with same input
- Handle varying numbers of themes and quotes
- Memory efficient processing
- Scalable to different input sizes

## Testing Approach
- Human evaluation of recommendation quality and implementability
- Product manager feedback on action feasibility
- Validation against theme and quote inputs
- A/B testing different prompt engineering approaches
- Performance and consistency testing