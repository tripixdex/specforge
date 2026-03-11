# Architecture

## Architectural Direction

SpecForge remains a small-file, modular Python application. Stage 5 keeps the deterministic pipeline and local API as the core execution path, preserves the server-rendered browser UI, and adds a compact local evaluation layer rather than a heavier benchmarking system.

Repository hygiene rule: stage changes should preserve modular boundaries and split overloaded files when they start mixing orchestration, rules, rendering, or transport concerns.

## Implemented Stage 5 Components

- `domain/`: Pydantic models for briefs, findings, reports, artifacts, and delivery packs
- `pipeline/`: deterministic intake, analysis, generation, and export modules
- `cli.py`: thin orchestration layer for analyze, generate, and demo commands
- `input_validation.py`: shared local input guardrails
- `demo_catalog.py`: bundled demo registry used by API and UI
- `api/schemas.py`: typed request and response models for the API
- `api/service.py`: local API orchestration and safe output-policy helpers
- `api/routes.py`: JSON endpoint definitions
- `api/app.py`: app factory, static mounting, and error handling
- `ui/service.py`: shared UI orchestration on top of the same core services
- `ui/routes.py`: server-rendered UI endpoints
- `ui/templates/`: Jinja templates for the local browser UI
- `ui/static/`: local CSS assets for the browser demo
- `eval/`: local Stage 5 corpus data
- `eval/*.py`: typed eval loader and deterministic runner

## Implemented Flow

1. Accept a local text brief from the CLI, API, or browser UI.
2. Normalize the text into a `NormalizedBrief`.
3. Run deterministic analysis and produce an `AnalysisReport`.
4. Optionally generate a `DeliveryPack`.
5. Export artifacts under `outputs/` when generation is requested.
6. Optionally score the run against labeled local corpus expectations.
7. Render either JSON responses or local HTML views from the same core flow.

## UI Approach

Stage 4 uses a server-rendered FastAPI UI because it:

- keeps the stack small and easy to explain
- avoids front-end sprawl before the product direction is clearer
- reuses the existing local app runtime
- keeps validation and output policy anchored in the same backend code

## Output Safety

- API-generated bundles always land under repo-local `outputs/`
- UI-generated bundles also land under repo-local `outputs/`
- user-supplied output labels are validated and sanitized
- the API and UI do not accept arbitrary filesystem paths
- eval bundles land under repo-local `outputs/evals/`
- normal API errors return structured JSON without stack traces
- the CLI still allows `--output-root`; this is an intentional local-developer escape hatch and is documented as a divergence

## Evaluation Approach

- the corpus is file-backed and inspectable under `eval/`
- expectations are structural and category-based rather than exact-text matching
- the runner exports both per-case bundles and a stable summary artifact
- the harness is deterministic and local-first, but it is not a substitute for expert review

## What Stage 5 Does Not Implement

- cloud deployment
- auth or persistence
- collaborative editing
- external integrations
- required LLM analysis
- production-service guarantees
