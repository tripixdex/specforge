"""Higher-level outputs derived from deterministic analysis findings."""

from __future__ import annotations

from specforge.domain.models import (
    AmbiguityFinding,
    ConstraintSet,
    ContradictionFinding,
    MissingDecision,
    NormalizedBrief,
    TraceabilityLink,
)
from specforge.pipeline.analysis_signals import infer_team_size_count, sort_by_severity
from specforge.pipeline.intake import dedupe


def prioritize_open_questions(
    ambiguities: list[AmbiguityFinding],
    contradictions: list[ContradictionFinding],
    missing_decisions: list[MissingDecision],
) -> list[str]:
    """Create a prioritized open-question list from findings."""

    questions = [item.question for item in sort_by_severity(ambiguities)]
    for decision in sort_by_severity(missing_decisions):
        questions.append(f"Decision needed: {decision.description}")
    for contradiction in sort_by_severity(contradictions):
        questions.append(f"Resolve contradiction: {contradiction.description}")
    return dedupe(questions)


def infer_mvp_cut(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
    contradictions: list[ContradictionFinding],
    missing_decisions: list[MissingDecision],
) -> list[str]:
    """Recommend a narrower MVP cut from deterministic signals."""

    cut = []
    if brief.goals:
        cut.append(f"Anchor the first release on this primary goal: {brief.goals[0]}")
    if len(brief.goals) > 1:
        cut.append("Defer secondary goals until the first workflow is validated.")
    if len(constraints.platform_hints) > 1:
        platforms = ", ".join(constraints.platform_hints)
        cut.append(
            "Choose one primary platform instead of splitting across: "
            f"{platforms}."
        )
    if any(item.category == "pricing" for item in missing_decisions):
        cut.append(
            "Treat pricing as a follow-up decision unless monetization is core "
            "to the first workflow."
        )
    if any(item.category == "minimal-mvp-vs-enterprise-scope" for item in contradictions):
        cut.append(
            "Remove enterprise-only requirements such as SSO, audit trails, or "
            "compliance-heavy scope from MVP."
        )
    if any(
        item.category == "small-team-aggressive-deadline-broad-scope"
        for item in contradictions
    ):
        cut.append(
            "Cut the release to one role and one core workflow before keeping "
            "the stated deadline."
        )
    if not cut:
        cut.append(
            "Keep the first release focused on one user, one workflow, and one "
            "local review loop."
        )
    return dedupe(cut)


def build_traceability_links(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
) -> list[TraceabilityLink]:
    """Create lightweight traceability links for key extracted signals."""

    links: list[TraceabilityLink] = []
    for goal in brief.goals[:3]:
        links.append(TraceabilityLink(source_excerpt=goal, target_section="scope.md"))
    for constraint in constraints.explicit_constraints[:3]:
        links.append(TraceabilityLink(source_excerpt=constraint, target_section="constraints.md"))
    return links


def infer_risks(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
    contradictions: list[ContradictionFinding],
    missing_decisions: list[MissingDecision],
) -> list[str]:
    """Seed the risk register from analytical findings."""

    risks = [item.description for item in contradictions]
    risks.extend(
        item.description
        for item in missing_decisions
        if item.severity in {"medium", "high"}
    )
    if constraints.timeline and infer_team_size_count(constraints.team_size) <= 1:
        risks.append(
            "A one-person team plus an explicit delivery timeline increases "
            "schedule risk."
        )
    if not brief.audience:
        risks.append("Unclear audience definition weakens prioritization and acceptance criteria.")
    return dedupe(risks)
