"""Deterministic ambiguity rules."""

from __future__ import annotations

from specforge.domain.models import AmbiguityFinding, ConstraintSet, NormalizedBrief
from specforge.pipeline.analysis_signals import (
    contains_vague_goals,
    find_evidence,
    has_monetization_signal,
    has_success_signal,
)


def infer_ambiguities(brief: NormalizedBrief, constraints: ConstraintSet) -> list[AmbiguityFinding]:
    """Collect ambiguous or underspecified planning signals."""

    findings: list[AmbiguityFinding] = []
    if not brief.audience:
        findings.append(
            AmbiguityFinding(
                category="audience",
                severity="high",
                description="The primary user or buyer is not clearly identified.",
                evidence=find_evidence(
                    brief.normalized_text,
                    ["user", "customer", "client", "team"],
                )[:2],
                recommendation="Name one primary user or buyer for the first release.",
                source_type="unresolved",
                question="Who is the primary user or buyer for the first release?",
            )
        )
    if not constraints.platform_hints:
        findings.append(
            AmbiguityFinding(
                category="platform",
                severity="high",
                description="The brief does not make the first platform explicit.",
                evidence=[brief.summary],
                recommendation="Choose a first platform before expanding the scope narrative.",
                source_type="unresolved",
                question=(
                    "What platform matters first: web, mobile, desktop, CLI, API, "
                    "or internal workflow tooling?"
                ),
            )
        )
    if not brief.goals or contains_vague_goals(brief.goals):
        findings.append(
            AmbiguityFinding(
                category="goals",
                severity="high" if not brief.goals else "medium",
                description="The goals are missing or too vague to anchor scope cleanly.",
                evidence=brief.goals[:2] or [brief.summary],
                recommendation="Rewrite the goals as concrete outcomes, not general aspirations.",
                source_type="unresolved" if not brief.goals else "inferred",
                question="What are the one to three concrete outcomes that define success?",
            )
        )
    if not has_success_signal(brief):
        findings.append(
            AmbiguityFinding(
                category="success_criteria",
                severity="medium",
                description=(
                    "No explicit success criteria, metric, or concrete completion "
                    "signal was found."
                ),
                evidence=brief.goals[:2] or [brief.summary],
                recommendation="Add one measurable or binary success check for the first release.",
                source_type="unresolved",
                question="How will the team know the first release is successful?",
            )
        )
    if not has_monetization_signal(brief) and constraints.audience_hint in {"b2b", "b2c"}:
        findings.append(
            AmbiguityFinding(
                category="monetization",
                severity="medium",
                description=(
                    "The brief describes an external product but gives no pricing "
                    "or monetization direction."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    ["client", "customer", "b2b", "b2c"],
                )[:2],
                recommendation=(
                    "State whether pricing is subscription, usage-based, internal "
                    "cost center, or deferred."
                ),
                source_type="unresolved",
                question=(
                    "How is the product expected to make money, or is pricing "
                    "intentionally deferred?"
                ),
            )
        )
    if not constraints.budget:
        findings.append(
            AmbiguityFinding(
                category="budget",
                severity="medium",
                description="No budget range or spend ceiling was found.",
                evidence=[brief.summary],
                recommendation="Add a rough budget ceiling to keep scope realistic.",
                source_type="unresolved",
                question="What budget range constrains this work?",
            )
        )
    if not constraints.timeline:
        findings.append(
            AmbiguityFinding(
                category="timeline",
                severity="medium",
                description="No delivery timing constraint was found.",
                evidence=[brief.summary],
                recommendation="State the date or timebox the MVP should optimize for.",
                source_type="unresolved",
                question="What timeline or deadline should delivery planning optimize for?",
            )
        )
    return findings
