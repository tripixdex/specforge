# Scope

## Product Vision

SpecForge helps founders, consultants, and internal product leads turn inconsistent brief text into a reviewable scope package before implementation starts. Stage 4 keeps the deterministic pipeline and local API intact while adding a clean browser UI for demo use.

## Target Users

- solo founders preparing a first execution brief
- agencies or consultants running structured discovery
- recruiters or reviewers evaluating the product demo
- internal operators tightening scope before build work starts

## Stage 4 In Scope

- deterministic intake normalization from plain-text briefs
- deterministic ambiguity, contradiction, missing-decision, and assumption analysis
- deterministic delivery-pack generation and local filesystem export
- CLI flows for `analyze`, `generate`, and `demo`
- typed FastAPI endpoints for `/health`, `/analyze`, `/generate`, and `/demo`
- server-rendered local browser UI for brief entry, demo selection, analysis, and generation
- repo-local output policy under `outputs/` for API and UI generation
- request and input validation with honest local-only behavior

## Stage 4 Out of Scope

- cloud deployment
- hosted storage or collaboration
- auth, accounts, or multi-user workflows
- external integrations
- arbitrary filesystem output paths from the API or UI
- autonomous product-planning claims

## Stage 4 Limits

The UI runs the same deterministic heuristics as the CLI and API. It is a polished local demo surface, not a production frontend or a rich collaborative application.
