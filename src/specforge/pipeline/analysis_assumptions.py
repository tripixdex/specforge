"""Assumption-specific rules for deterministic analysis."""

from __future__ import annotations

from specforge.domain.models import AssumptionItem, ConstraintSet, NormalizedBrief
from specforge.pipeline.analysis_signals import find_evidence


def infer_assumptions(brief: NormalizedBrief, constraints: ConstraintSet) -> list[AssumptionItem]:
    """Create narrow assumptions only where the brief strongly implies them."""

    assumptions: list[AssumptionItem] = []
    if "local-first" in constraints.platform_hints:
        assumptions.append(
            AssumptionItem(
                category="deployment",
                severity="medium",
                statement="The first release should keep inputs and outputs on the local machine.",
                description="Local execution is treated as a hard planning assumption for the MVP.",
                rationale="The brief explicitly references local-first operation.",
                evidence=find_evidence(
                    brief.normalized_text,
                    ["local-first", "local first", "keep data local", "offline"],
                ),
                recommendation=(
                    "Keep hosted collaboration and remote storage out of the first "
                    "scoped cut."
                ),
                source_type="explicit",
                confidence="high",
            )
        )
    if constraints.audience_hint == "internal":
        assumptions.append(
            AssumptionItem(
                category="audience",
                severity="medium",
                statement=(
                    "The first scope should optimize for internal operators rather "
                    "than external self-serve users."
                ),
                description="Internal operator workflows appear to be the primary user context.",
                rationale="The brief uses internal-team language.",
                evidence=find_evidence(
                    brief.normalized_text,
                    ["internal", "operations team", "ops team", "support team"],
                ),
                recommendation=(
                    "Defer external account-management flows until the internal "
                    "workflow is clear."
                ),
                source_type="inferred",
                confidence="medium",
            )
        )
    if not constraints.timeline and brief.goals:
        assumptions.append(
            AssumptionItem(
                category="delivery",
                severity="low",
                statement=(
                    "Planning will default to a narrow first milestone because no "
                    "explicit timeline was given."
                ),
                description=(
                    "No timeline signal was found, so early scope should remain "
                    "conservative."
                ),
                rationale="Missing timing context makes broad sequencing risky.",
                evidence=[brief.goals[0]],
                recommendation="Confirm the expected deadline before adding secondary workflows.",
                source_type="unresolved",
                confidence="low",
            )
        )
    return assumptions


def dedupe_assumptions(items: list[AssumptionItem]) -> list[AssumptionItem]:
    """Deduplicate assumptions by statement while preserving order."""

    seen: set[str] = set()
    unique: list[AssumptionItem] = []
    for item in items:
        if item.statement not in seen:
            seen.add(item.statement)
            unique.append(item)
    return unique
