"""Shared orchestration for the server-rendered SpecForge UI."""

from __future__ import annotations

from pathlib import Path

from specforge.api.schemas import AnalyzeRequest, GenerateRequest
from specforge.api.service import (
    OUTPUTS_ROOT,
    REPO_ROOT,
    analyze_request,
    safe_output_label,
)
from specforge.domain.models import AnalysisReport, DeliveryArtifact, NormalizedBrief
from specforge.pipeline import export_delivery_pack, generate_delivery_pack
from specforge.pipeline.language import category_label, detect_language
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
    locale = detect_language(brief.normalized_text)
    return UiResultView(
        title=brief.title,
        language=locale,
        source_text=brief.source_text,
        normalized_summary=brief.summary,
        ambiguity_findings=[to_finding_view(item, locale=locale) for item in report.ambiguities],
        contradiction_findings=[
            to_finding_view(item, locale=locale) for item in report.contradictions
        ],
        missing_decisions=[
            to_finding_view(item, locale=locale) for item in report.missing_decisions
        ],
        assumptions=[item.statement for item in report.assumptions],
        open_questions=report.prioritized_open_questions[:6],
        recommended_mvp_cut=report.recommended_mvp_cut,
        output_path=output_path,
        output_path_display=to_repo_local_path(output_path),
        artifact_previews=[to_artifact_preview(item) for item in artifacts],
        artifact_names=[item.name for item in artifacts],
        underspecified_banner=underspecified_banner(brief=brief, report=report),
        underspecified_essentials=underspecified_essentials(brief=brief),
        mode=mode,
        counts={
            "ambiguities": len(report.ambiguities),
            "contradictions": len(report.contradictions),
            "missing_decisions": len(report.missing_decisions),
            "assumptions": len(report.assumptions),
            "open_questions": len(report.prioritized_open_questions),
        },
    )


def to_finding_view(item: object, *, locale: str) -> FindingView:
    """Convert a domain finding into a small UI view model."""

    return FindingView(
        category=getattr(item, "category"),
        display_category=category_label(getattr(item, "category"), locale),
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
        is_human_readable=item.kind != "json",
    )


def underspecified_banner(*, brief: NormalizedBrief, report: AnalysisReport) -> str | None:
    """Return a humane short-brief warning when the input is too thin."""

    word_count = len(brief.normalized_text.split())
    locale = detect_language(brief.normalized_text)
    if word_count > 8:
        return None
    if report.contradictions:
        return None
    if locale == "ru":
        return (
            "Бриф пока слишком короткий. Дайте чуть больше контекста, чтобы выводы стали надежнее."
        )
    return (
        "This brief is still very short. Add a bit more context to make the output "
        "more trustworthy."
    )


def underspecified_essentials(*, brief: NormalizedBrief) -> list[str]:
    """Return the top essentials to request first for under-specified briefs."""

    word_count = len(brief.normalized_text.split())
    locale = detect_language(brief.normalized_text)
    if word_count > 8:
        return []

    items: list[str] = []
    if not brief.audience:
        items.append("Кто основной пользователь?" if locale == "ru" else "Who is the primary user?")
    if not brief.constraints.platform_hints:
        items.append(
            "Какая платформа важнее первой?" if locale == "ru" else "Which platform matters first?"
        )
    if not brief.goals:
        items.append(
            "Какой один результат должен дать первый релиз?"
            if locale == "ru"
            else "What one outcome should the first release deliver?"
        )
    return items[:3]


def to_repo_local_path(output_path: str | None) -> str | None:
    """Return a calmer repo-local path display for the browser UI."""

    if not output_path:
        return None
    try:
        return str(Path(output_path).resolve().relative_to(REPO_ROOT.resolve()))
    except ValueError:
        return output_path
