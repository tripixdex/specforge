# Architecture

## Architectural Direction

SpecForge remains a small-file, modular Python application. Stage 4 keeps the deterministic pipeline and local API as the core execution path and adds a server-rendered browser UI rather than a separate frontend stack.

Repository hygiene rule: stage changes should preserve modular boundaries and split overloaded files when they start mixing orchestration, rules, rendering, or transport concerns.

## Implemented Stage 4 Components

- `domain/`: Pydantic models for briefs, findings, reports, artifacts, and delivery packs
- `pipeline/`: deterministic intake, analysis, generation, and export modules
- `cli.py`: thin orchestration layer for analyze, generate, and demo commands
- `api/schemas.py`: typed request and response models for the API
- `api/service.py`: local API orchestration and safe output-policy helpers
- `api/routes.py`: JSON endpoint definitions
- `api/app.py`: app factory, static mounting, and error handling
- `ui/service.py`: shared UI orchestration on top of the same core services
- `ui/routes.py`: server-rendered UI endpoints
- `ui/templates/`: Jinja templates for the local browser UI
- `ui/static/`: local CSS assets for the browser demo

## Implemented Flow

1. Accept a local text brief from the CLI, API, or browser UI.
2. Normalize the text into a `NormalizedBrief`.
3. Run deterministic analysis and produce an `AnalysisReport`.
4. Optionally generate a `DeliveryPack`.
5. Export artifacts under `outputs/` when generation is requested.
6. Render either JSON responses or local HTML views from the same core flow.

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
- normal API errors return structured JSON without stack traces

## What Stage 4 Does Not Implement

- cloud deployment
- auth or persistence
- collaborative editing
- external integrations
- required LLM analysis
- production-service guarantees
