"""Thin orchestration wrapper for the deterministic analysis layer."""

from __future__ import annotations

from specforge.domain.models import AnalysisReport, NormalizedBrief
from specforge.pipeline.analysis_ambiguities import infer_ambiguities
from specforge.pipeline.analysis_assumptions import dedupe_assumptions, infer_assumptions
from specforge.pipeline.analysis_decisions import infer_contradictions, infer_missing_decisions
from specforge.pipeline.analysis_outcomes import (
    build_traceability_links,
    infer_mvp_cut,
    infer_risks,
    prioritize_open_questions,
)
from specforge.pipeline.analysis_signals import (
    BUDGET_PATTERN,
    TIMELINE_PATTERN,
    extract_first_match,
    infer_audience_hint,
    infer_platform_hints,
    infer_team_size,
    infer_tradeoffs,
)
from specforge.pipeline.intake import dedupe


def analyze_brief(brief: NormalizedBrief) -> tuple[NormalizedBrief, AnalysisReport]:
    """Extract deterministic constraints and a richer Stage 2 analysis report."""

    text = brief.normalized_text
    lowered = text.lower()
    constraints = brief.constraints.model_copy(
        update={
            "budget": brief.constraints.budget or extract_first_match(BUDGET_PATTERN, text),
            "timeline": brief.constraints.timeline or extract_first_match(TIMELINE_PATTERN, text),
            "team_size": brief.constraints.team_size or infer_team_size(text),
            "platform_hints": dedupe(
                brief.constraints.platform_hints + infer_platform_hints(lowered)
            ),
            "audience_hint": brief.constraints.audience_hint or infer_audience_hint(lowered),
            "speed_quality_budget_tradeoffs": dedupe(
                brief.constraints.speed_quality_budget_tradeoffs + infer_tradeoffs(lowered)
            ),
        }
    )
    ambiguities = infer_ambiguities(brief, constraints)
    contradictions = infer_contradictions(brief, constraints)
    missing_decisions = infer_missing_decisions(brief, constraints)
    assumptions = dedupe_assumptions(brief.assumptions + infer_assumptions(brief, constraints))
    open_questions = prioritize_open_questions(ambiguities, contradictions, missing_decisions)
    risks = dedupe(brief.risks + infer_risks(brief, constraints, contradictions, missing_decisions))
    recommended_mvp_cut = infer_mvp_cut(brief, constraints, contradictions, missing_decisions)
    traceability_links = build_traceability_links(brief, constraints)

    report = AnalysisReport(
        ambiguities=ambiguities,
        contradictions=contradictions,
        missing_decisions=missing_decisions,
        assumptions=assumptions,
        prioritized_open_questions=open_questions,
        recommended_mvp_cut=recommended_mvp_cut,
        traceability_links=traceability_links,
    )
    analyzed = brief.model_copy(
        update={
            "constraints": constraints,
            "assumptions": assumptions,
            "open_questions": open_questions,
            "risks": risks,
            "analysis": report,
        }
    )
    return analyzed, report
