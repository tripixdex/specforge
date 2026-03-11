"""Shared orchestration for the server-rendered SpecForge UI."""

from __future__ import annotations

from specforge.api.schemas import AnalyzeRequest, GenerateRequest
from specforge.api.service import (
    OUTPUTS_ROOT,
    analyze_request,
    safe_output_label,
)
from specforge.domain.models import AnalysisReport, DeliveryArtifact, NormalizedBrief
from specforge.pipeline import export_delivery_pack, generate_delivery_pack
from specforge.ui.models import ArtifactPreviewView, FindingView, UiResultView


def analyze_for_ui(
    *,
    brief_text: str,
    title: str | None = None,
    source_type: str = "ui",
) -> UiResultView:
    """Run deterministic analysis and return a UI view model."""

    request = AnalyzeRequest(brief_text=brief_text, title=title, source_type=source_type)
    brief, report = analyze_request(request)
    return build_ui_result(brief=brief, report=report, mode="analyze")


def generate_for_ui(
    *,
    brief_text: str,
    title: str | None = None,
    output_label: str | None = None,
) -> UiResultView:
    """Run generation and return a UI view model with artifact previews."""

    request = GenerateRequest(
        brief_text=brief_text,
        title=title,
        source_type="ui",
        output_label=output_label,
    )
    brief, report = analyze_request(request)
    pack = generate_delivery_pack(brief)
    output_dir = export_delivery_pack(
        pack,
        output_root=OUTPUTS_ROOT,
        run_label=safe_output_label(request.output_label),
    )
    result = build_ui_result(
        brief=brief,
        report=report,
        mode="generate",
        output_path=str(output_dir.resolve()),
        artifacts=pack.artifacts,
    )
    return result


def build_ui_result(
    *,
    brief: NormalizedBrief,
    report: AnalysisReport,
    mode: str,
    output_path: str | None = None,
    artifacts: list[DeliveryArtifact] | None = None,
) -> UiResultView:
    """Convert pipeline output into a template-friendly UI state."""

    artifacts = artifacts or []
    return UiResultView(
        title=brief.title,
        source_text=brief.source_text,
        normalized_summary=brief.summary,
        ambiguity_findings=[to_finding_view(item) for item in report.ambiguities],
        contradiction_findings=[to_finding_view(item) for item in report.contradictions],
        missing_decisions=[to_finding_view(item) for item in report.missing_decisions],
        assumptions=[item.statement for item in report.assumptions],
        open_questions=report.prioritized_open_questions[:6],
        recommended_mvp_cut=report.recommended_mvp_cut,
        output_path=output_path,
        artifact_previews=[to_artifact_preview(item) for item in artifacts],
        artifact_names=[item.name for item in artifacts],
        mode=mode,
        counts={
            "ambiguities": len(report.ambiguities),
            "contradictions": len(report.contradictions),
            "missing_decisions": len(report.missing_decisions),
            "assumptions": len(report.assumptions),
            "open_questions": len(report.prioritized_open_questions),
        },
    )


def to_finding_view(item: object) -> FindingView:
    """Convert a domain finding into a small UI view model."""

    return FindingView(
        category=getattr(item, "category"),
        severity=getattr(item, "severity"),
        description=getattr(item, "description"),
        recommendation=getattr(item, "recommendation"),
        evidence=list(getattr(item, "evidence", []))[:3],
    )


def to_artifact_preview(item: DeliveryArtifact) -> ArtifactPreviewView:
    """Build a short artifact preview for the generated bundle panel."""

    preview = item.content[:800].strip()
    return ArtifactPreviewView(
        name=item.name,
        relative_path=item.relative_path,
        kind=item.kind,
        preview=preview,
    )
