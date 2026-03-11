"""Deterministic delivery-pack generation with Stage 2 analysis integration."""

from __future__ import annotations

from datetime import UTC, datetime

from specforge.domain.models import AnalysisReport, DeliveryPack, NormalizedBrief
from specforge.pipeline.intake import dedupe


def generate_delivery_pack(brief: NormalizedBrief) -> DeliveryPack:
    """Build a deterministic Stage 2 delivery-pack skeleton."""

    analysis = brief.analysis or AnalysisReport(assumptions=brief.assumptions)
    scope_draft = build_scope_draft(brief)
    first_step = build_first_step_recommendation(brief, analysis)
    explicit_user_input = build_explicit_user_input(brief)
    inferred_structure = build_inferred_structure(brief, analysis)
    why_risky = build_why_risky(analysis, brief.risks)

    return DeliveryPack(
        generated_at=datetime.now(UTC).isoformat(),
        brief=brief,
        analysis=analysis,
        brief_summary=build_brief_summary(brief),
        goals=brief.goals,
        non_goals=brief.non_goals,
        scope_draft=scope_draft,
        explicit_user_input=explicit_user_input,
        inferred_structure=inferred_structure,
        constraints=brief.constraints,
        open_questions=analysis.prioritized_open_questions or brief.open_questions,
        assumptions=analysis.assumptions or brief.assumptions,
        risk_register=dedupe(brief.risks),
        recommended_mvp_cut=analysis.recommended_mvp_cut,
        why_this_is_risky=why_risky,
        first_step_recommendation=first_step,
        analysis_counts=build_analysis_counts(analysis),
    )


def build_brief_summary(brief: NormalizedBrief) -> str:
    """Create a compact deterministic summary sentence."""

    product = brief.product_type or "product concept"
    audience = ", ".join(brief.audience) if brief.audience else "an unspecified audience"
    if brief.goals:
        return f"{brief.title} is a {product} aimed at {audience}. Primary goal: {brief.goals[0]}."
    return f"{brief.title} is a {product} aimed at {audience}. Goals still need clarification."


def build_scope_draft(brief: NormalizedBrief) -> list[str]:
    """Assemble a small deterministic scope draft."""

    items = []
    if brief.product_type:
        items.append(f"Shape the first scoped draft around a {brief.product_type}.")
    if brief.audience:
        items.append(f"Prioritize the needs of {', '.join(brief.audience)}.")
    if brief.goals:
        items.extend(f"Support goal: {goal}." for goal in brief.goals[:3])
    if brief.non_goals:
        items.extend(f"Keep out of scope for now: {item}." for item in brief.non_goals[:3])
    if brief.constraints.platform_hints:
        items.append(
            "Respect platform hints: " + ", ".join(brief.constraints.platform_hints[:4]) + "."
        )
    return dedupe(items)


def build_explicit_user_input(brief: NormalizedBrief) -> list[str]:
    """Collect explicit source claims for display in the pack."""

    explicit = brief.goals[:3] + brief.non_goals[:3] + brief.constraints.explicit_constraints[:4]
    return dedupe(explicit)


def build_inferred_structure(
    brief: NormalizedBrief,
    analysis: AnalysisReport,
) -> list[str]:
    """Collect deterministic inferences for display in the pack."""

    inferred = []
    if brief.product_type:
        inferred.append(f"Inferred product type: {brief.product_type}.")
    if brief.constraints.audience_hint:
        inferred.append(f"Inferred audience mode: {brief.constraints.audience_hint}.")
    if brief.constraints.platform_hints:
        inferred.append(
            "Inferred platform hints: " + ", ".join(brief.constraints.platform_hints) + "."
        )
    if analysis.contradictions:
        inferred.append(
            "Detected contradiction pressure across "
            f"{len(analysis.contradictions)} planning area(s)."
        )
    return dedupe(inferred)


def build_why_risky(analysis: AnalysisReport, existing_risks: list[str]) -> list[str]:
    """Explain risk in terms of contradictions and unresolved decisions."""

    risky = [item.description for item in analysis.contradictions]
    risky.extend(item.description for item in analysis.missing_decisions)
    risky.extend(existing_risks)
    return dedupe(risky)


def build_first_step_recommendation(
    brief: NormalizedBrief,
    analysis: AnalysisReport,
) -> str:
    """Recommend the next delivery action based on analysis."""

    if analysis.prioritized_open_questions:
        return (
            "Resolve the top unresolved question before expanding scope: "
            f"{analysis.prioritized_open_questions[0]}"
        )
    if analysis.recommended_mvp_cut:
        return analysis.recommended_mvp_cut[0]
    if brief.goals:
        return (
            "Turn the normalized goals into a milestone-1 checklist and confirm "
            "the first acceptance criteria manually."
        )
    return "Clarify the target user and desired outcome before attempting detailed planning."


def build_analysis_counts(analysis: AnalysisReport) -> dict[str, int]:
    """Return summary counts for the analysis layer."""

    return {
        "ambiguities": len(analysis.ambiguities),
        "contradictions": len(analysis.contradictions),
        "missing_decisions": len(analysis.missing_decisions),
        "assumptions": len(analysis.assumptions),
        "open_questions": len(analysis.prioritized_open_questions),
    }
