# Scope

## Product Vision

SpecForge helps founders, consultants, and internal product leads turn inconsistent brief text into a reviewable scope package before implementation starts. Stage 5 keeps the deterministic pipeline, local API, and browser UI intact while adding a real local evaluation layer and a targeted hardening pass.

## Target Users

- solo founders preparing a first execution brief
- agencies or consultants running structured discovery
- recruiters or reviewers evaluating the product demo
- internal operators tightening scope before build work starts

## Stage 5 In Scope

- deterministic intake normalization from plain-text briefs
- deterministic ambiguity, contradiction, missing-decision, and assumption analysis
- deterministic delivery-pack generation and local filesystem export
- CLI flows for `analyze`, `generate`, and `demo`
- typed FastAPI endpoints for `/health`, `/analyze`, `/generate`, and `/demo`
- server-rendered local browser UI for brief entry, demo selection, analysis, and generation
- local evaluation corpus under `eval/`
- deterministic eval harness with structural expectations and output completeness checks
- repo-local output policy under `outputs/` for API and UI generation
- request and input validation with honest local-only behavior

## Stage 5 Out of Scope

- cloud deployment
- hosted storage or collaboration
- auth, accounts, or multi-user workflows
- external integrations
- arbitrary filesystem output paths from the API or UI
- autonomous product-planning claims

## Stage 5 Limits

The UI runs the same deterministic heuristics as the CLI and API. The eval harness is a local rubric layer, not a scientific benchmark. SpecForge remains a polished local demo product, not a production service.
