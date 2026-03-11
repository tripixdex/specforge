# Evaluation Plan

## Evaluation Philosophy

SpecForge should first be evaluated on traceability and usefulness, not on intelligence theater. Stage 2 outputs are deterministic analytical drafts, so the main question is whether they expose obvious tensions and missing decisions honestly and consistently.

## Stage 2 Checks

- schema instantiation tests for analysis models
- ambiguity detection tests for under-specified briefs
- contradiction detection tests for at least two rule patterns
- missing-decision detection tests
- export tests for analysis-aware artifacts
- CLI analyze and generate happy-path coverage

## Future Evaluation Work

- compare deterministic findings against labeled review datasets
- separate deterministic evaluation from any future assisted analyzer evaluation
- add rubric-based review for whether recommended MVP cuts are useful in real discovery sessions
