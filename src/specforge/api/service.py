"""Service helpers for the local SpecForge API."""

from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException, status

from specforge.api.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    BriefSummaryResponse,
    DemoResponse,
    FindingCounts,
    GenerateRequest,
    GenerateResponse,
)
from specforge.demo_catalog import available_demo_names, default_demo_name, load_demo_brief
from specforge.domain.models import AnalysisReport, ConstraintSet, NormalizedBrief, RawBrief
from specforge.input_validation import normalize_brief_text
from specforge.pipeline import (
    analyze_brief,
    create_raw_brief,
    export_delivery_pack,
    generate_delivery_pack,
    normalize_brief,
)
from specforge.pipeline.export import slugify

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUTS_ROOT = REPO_ROOT / "outputs"


def build_raw_brief(request: AnalyzeRequest | GenerateRequest) -> RawBrief:
    """Convert an API request into a raw brief for the deterministic pipeline."""

    metadata = dict(request.metadata)
    if request.source_type:
        metadata["source_type"] = request.source_type
    if request.product_type:
        metadata["product_type"] = request.product_type
    return create_raw_brief(
        normalize_brief_text(request.brief_text),
        title=request.title,
        metadata=metadata,
    ).model_copy(
        update={
            "audience": request.audience,
            "goals": request.goals,
            "non_goals": request.non_goals,
            "notes": request.notes,
            "references": request.references,
            "constraints": ConstraintSet(non_goals=request.non_goals),
        }
    )


def analyze_request(
    request: AnalyzeRequest | GenerateRequest,
) -> tuple[NormalizedBrief, AnalysisReport]:
    """Run intake and analysis for an API request."""

    raw_brief = build_raw_brief(request)
    normalized = normalize_brief(raw_brief)
    return analyze_brief(normalized)


def build_analyze_response(brief: NormalizedBrief, report: AnalysisReport) -> AnalyzeResponse:
    """Map analysis models to the public API response."""

    counts = report_counts(report)
    return AnalyzeResponse(
        brief=BriefSummaryResponse(
            title=brief.title,
            product_type=brief.product_type,
            audience=brief.audience,
            goals=brief.goals,
            non_goals=brief.non_goals,
            summary=brief.summary,
        ),
        normalized_summary=brief.summary,
        counts=counts,
        top_open_questions=report.prioritized_open_questions[:5],
        recommended_mvp_cut=report.recommended_mvp_cut,
        assumptions=[item.statement for item in report.assumptions],
    )


def generate_response(request: GenerateRequest) -> GenerateResponse:
    """Run the full deterministic pipeline and export a local delivery bundle."""

    brief, report = analyze_request(request)
    pack = generate_delivery_pack(brief)
    output_dir = export_delivery_pack(
        pack,
        output_root=OUTPUTS_ROOT,
        run_label=safe_output_label(request.output_label),
    )
    output_path = str(output_dir.resolve())
    if not is_output_within_root(output_dir):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="generated output escaped the local outputs directory",
        )
    base = build_analyze_response(brief, report)
    return GenerateResponse(
        **base.model_dump(),
        output_path=output_path,
        artifact_files=sorted(artifact.name for artifact in pack.artifacts),
    )


def build_demo_response() -> DemoResponse:
    """Return a stable sample analysis based on a bundled brief."""

    demo_name = default_demo_name()
    title, brief_text, input_path = load_demo_brief(demo_name)
    request = AnalyzeRequest(
        brief_text=brief_text,
        title=title,
        source_type="demo-sample",
    )
    brief, report = analyze_request(request)
    return DemoResponse(
        demo_name=demo_name,
        demo_input_path=str(input_path),
        available_demos=available_demo_names(),
        sample_analysis=build_analyze_response(brief, report),
    )


def safe_output_label(label: str | None) -> str | None:
    """Sanitize user-provided labels for repo-local output folders."""

    if label is None:
        return None
    slug = slugify(label)
    if not slug:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="output_label must contain at least one alphanumeric character",
        )
    return slug


def report_counts(report: AnalysisReport) -> FindingCounts:
    """Create the public count summary from an analysis report."""

    return FindingCounts(
        ambiguities=len(report.ambiguities),
        contradictions=len(report.contradictions),
        missing_decisions=len(report.missing_decisions),
        assumptions=len(report.assumptions),
        open_questions=len(report.prioritized_open_questions),
    )


def is_output_within_root(output_dir: Path) -> bool:
    """Ensure exported bundles remain inside the repo-local outputs directory."""

    try:
        output_dir.resolve().relative_to(OUTPUTS_ROOT.resolve())
    except ValueError:
        return False
    return True
