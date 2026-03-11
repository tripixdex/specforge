"""Low-level deterministic signals used by the analysis layer."""

from __future__ import annotations

import re

from specforge.domain.models import NormalizedBrief
from specforge.pipeline.intake import dedupe

BUDGET_PATTERN = re.compile(
    r"(\$[\d,]+(?:\s*-\s*\$[\d,]+)?[kKmM]?|under \$[\d,]+[kKmM]?|below \$[\d,]+[kKmM]?)",
    re.IGNORECASE,
)
TIMELINE_PATTERN = re.compile(
    (
        r"(\d+\s+(?:days|day|weeks|week|months|month|quarters|quarter)"
        r"|this quarter|next quarter|asap|next month)"
    ),
    re.IGNORECASE,
)
TEAM_PATTERN = re.compile(
    (
        r"(\bsolo founder\b|\bjust me\b|"
        r"\b\d+\s+(?:person|people|engineers|engineer|developers|developer)\b)"
    ),
    re.IGNORECASE,
)
NUMERIC_PATTERN = re.compile(r"\b\d+(?:%|x)?\b")


def extract_first_match(pattern: re.Pattern[str], text: str) -> str | None:
    """Return the first regex match if it exists."""

    match = pattern.search(text)
    return match.group(1) if match else None


def infer_team_size(text: str) -> str | None:
    """Infer a team size or staffing hint from text."""

    match = TEAM_PATTERN.search(text)
    if not match:
        return None
    value = match.group(1).lower()
    if value in {"solo founder", "just me"}:
        return "1 person"
    return value


def infer_platform_hints(lowered: str) -> list[str]:
    """Infer platform hints from direct keywords."""

    hints = []
    keyword_map = {
        r"\blocal-first\b": "local-first",
        r"\boffline\b": "offline-friendly",
        r"\bbrowser\b": "browser-ui-planned",
        r"\bweb\b": "web",
        r"\bmobile\b": "mobile",
        r"\bdesktop\b": "desktop",
        r"\bcli\b": "cli",
        r"\bapi\b": "api",
        r"\binternal tool\b": "internal-tool",
    }
    for pattern, label in keyword_map.items():
        if re.search(pattern, lowered):
            hints.append(label)
    return dedupe(hints)


def infer_audience_hint(lowered: str) -> str | None:
    """Infer whether the brief leans B2B, B2C, or internal."""

    if "internal" in lowered or "ops team" in lowered or "operations team" in lowered:
        return "internal"
    if any(word in lowered for word in ["b2b", "clients", "agency", "enterprise"]):
        return "b2b"
    if any(word in lowered for word in ["b2c", "consumers"]):
        return "b2c"
    return None


def infer_tradeoffs(lowered: str) -> list[str]:
    """Infer coarse delivery tradeoff hints from wording."""

    tradeoffs = []
    if any(word in lowered for word in ["fast", "quick", "asap", "mvp", "prototype"]):
        tradeoffs.append("speed prioritized")
    budget_markers = ["budget", "cheap", "lean", "bootstrap", "under $", "below $"]
    if any(word in lowered for word in budget_markers):
        tradeoffs.append("budget prioritized")
    if any(word in lowered for word in ["quality", "reliable", "accurate", "polished"]):
        tradeoffs.append("quality prioritized")
    return tradeoffs


def contains_vague_goals(goals: list[str]) -> bool:
    """Return whether the current goals are still too vague."""

    vague_terms = ["better", "easier", "powerful", "innovative", "feature-rich", "all-in-one"]
    return any(any(term in goal.lower() for term in vague_terms) for goal in goals)


def has_success_signal(brief: NormalizedBrief) -> bool:
    """Return whether the brief suggests measurable success."""

    if any(NUMERIC_PATTERN.search(goal) for goal in brief.goals):
        return True
    lowered = brief.normalized_text.lower()
    return any(word in lowered for word in ["success means", "metric", "kpi", "reduce", "increase"])


def has_monetization_signal(brief: NormalizedBrief) -> bool:
    """Return whether monetization or pricing is already mentioned."""

    lowered = brief.normalized_text.lower()
    monetization_terms = [
        "pricing",
        "subscription",
        "revenue",
        "paid",
        "free tier",
        "monetization",
    ]
    return any(word in lowered for word in monetization_terms)


def has_broad_scope_signal(brief: NormalizedBrief) -> bool:
    """Return whether the brief implies a broad scope surface."""

    lowered = brief.normalized_text.lower()
    if len(brief.goals) >= 4:
        return True
    return any(
        word in lowered
        for word in [
            "all-in-one",
            "everything",
            "full suite",
            "multiple teams",
            "admin",
            "billing",
            "analytics",
            "integrations",
        ]
    )


def has_enterprise_scope_signal(lowered: str) -> bool:
    """Return whether the brief implies enterprise-grade scope."""

    return any(
        word in lowered
        for word in [
            "enterprise",
            "sso",
            "audit",
            "role-based",
            "compliance",
            "permissions",
            "soc 2",
            "gdpr",
        ]
    )


def requires_security_decision(lowered: str) -> bool:
    """Return whether the brief implies a security or compliance decision should exist."""

    return any(
        word in lowered
        for word in [
            "enterprise",
            "patient",
            "financial",
            "customer data",
            "pii",
            "compliance",
            "audit",
        ]
    )


def has_security_signal(lowered: str) -> bool:
    """Return whether the brief already names a security posture."""

    return any(
        word in lowered
        for word in [
            "security",
            "compliance",
            "permission",
            "role-based",
            "encryption",
            "audit",
            "sso",
        ]
    )


def has_owner_signal(lowered: str) -> bool:
    """Return whether an owner/operator signal exists for internal tools."""

    return any(
        word in lowered
        for word in ["owner", "admin", "operations lead", "support lead", "maintain"]
    )


def infer_team_size_count(team_size: str | None) -> int:
    """Reduce a team-size string to a rough integer count."""

    if not team_size:
        return 99
    match = re.search(r"(\d+)", team_size)
    if match:
        return int(match.group(1))
    return 1 if "solo" in team_size or "1 person" in team_size else 99


def find_evidence(text: str, keywords: list[str]) -> list[str]:
    """Collect source lines that support a heuristic."""

    lines = []
    for line in text.splitlines():
        lowered = line.lower()
        if any(keyword.lower() in lowered for keyword in keywords):
            lines.append(line.strip())
    return dedupe(lines)


def collect_contradiction_evidence(brief: NormalizedBrief, keywords: list[str]) -> list[str]:
    """Collect evidence lines for contradiction findings."""

    evidence = find_evidence(brief.normalized_text, keywords)
    if not evidence and brief.goals:
        evidence = brief.goals[:2]
    return evidence


def sort_by_severity(items: list[object]) -> list[object]:
    """Sort findings by severity while preserving deterministic ordering."""

    order = {"high": 0, "medium": 1, "low": 2}
    return sorted(items, key=lambda item: order[getattr(item, "severity", "medium")])
