"""Low-level deterministic signals used by the analysis layer."""

from __future__ import annotations

import re
from decimal import Decimal

from specforge.domain.models import NormalizedBrief
from specforge.pipeline.intake import dedupe

BUDGET_PATTERN = re.compile(
    (
        r"(\$[\d,]+(?:\s*-\s*\$[\d,]+)?[kKmM]?|"
        r"under \$[\d,]+[kKmM]?|below \$[\d,]+[kKmM]?|"
        r"бюджет\s+до\s+\d+[\s\xa0]?(?:тыс|к|млн)?(?:\s*руб|\s*₽)?|"
        r"до\s+\d+[\s\xa0]?(?:тыс|к|млн)?(?:\s*руб|\s*₽))"
    ),
    re.IGNORECASE,
)
LOW_BUDGET_HINT_PATTERNS = (
    re.compile(
        r"\b(?:tight|lean|low|small)\s+budget\b|"
        r"\bbudget\s+(?:is\s+)?(?:very\s+)?(?:limited|tight|lean|small|low)\b|"
        r"\bbudget cap\b|"
        r"\bbootstrap\b|"
        r"\bcheap\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bбюджет\s+(?:очень\s+)?(?:маленький|ограничен|небольшой)\b|"
        r"\bограничен\s+бюджет\b|"
        r"\bденег\s+мало\b|"
        r"\bхотим\s+недорого\b|"
        r"\bдешево\b|"
        r"\bнедорого\b|"
        r"\bэкономно\b",
        re.IGNORECASE,
    ),
)
TIMELINE_PATTERN = re.compile(
    (
        r"(\d+\s+(?:days|day|weeks|week|months|month|quarters|quarter)"
        r"|\d+\s+(?:дней|дня|день|недель|недели|неделю|месяцев|месяца|месяц)"
        r"|this quarter|next quarter|asap|next month|срочно|как можно скорее|за \d+\s+\w+)"
    ),
    re.IGNORECASE,
)
TEAM_PATTERN = re.compile(
    (
        r"(\bsolo founder\b|\bjust me\b|\bjust two of us\b|"
        r"\bteam of (?:\d+|one|two|three)\b|"
        r"\b(?:\d+|one|two|three)[-\s]?(?:person|people|engineers|engineer|developers|developer)\b|"
        r"\bme (?:and|plus) one contractor\b|\bone contractor and me\b|"
        r"\bтолько я\b|\bя один\b|\bнас двое\b|\bкоманда(?:\s+из)?\s+(?:\d+|двух|трех|двое)\b|"
        r"\b\d+\s+(?:человек|разработчиков|разработчика)\b)"
    ),
    re.IGNORECASE,
)
NUMERIC_PATTERN = re.compile(r"\b\d+(?:%|x)?\b")
NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "двух": 2,
    "трех": 3,
    "двое": 2,
}
POST_MVP_PATTERN = re.compile(r"\bpost[-\s]?mvp\b|\bпосле\s+mvp\b", re.IGNORECASE)
PHASED_SCOPE_PATTERN = re.compile(
    r"\bnice[-\s]?to[-\s]?have\b|"
    r"\bfor later\b|"
    r"\blater\b|"
    r"\bphase\s*2\b|"
    r"\bfuture phase\b|"
    r"\bpost[-\s]?mvp\b|"
    r"\bпотом\b|"
    r"\bпозже\b|"
    r"\bна потом\b|"
    r"\bв следующ(?:ей|ем)\s+фаз[еуы]\b|"
    r"\bпосле\s+mvp\b",
    re.IGNORECASE,
)


def extract_first_match(pattern: re.Pattern[str], text: str) -> str | None:
    """Return the first regex match if it exists."""

    match = pattern.search(text)
    return match.group(1) if match else None


def infer_team_size(text: str) -> str | None:
    """Infer a team size or staffing hint from text."""

    match = TEAM_PATTERN.search(text)
    if not match:
        fallback = re.search(
            r"команда(?:\s+\w+){0,3}\s+(\d+|двух|трех|двое)\s+(?:человек|разработчиков|разработчика)",
            text.lower(),
        )
        if fallback:
            value = fallback.group(1)
            if value.isdigit():
                return f"{value} people"
            return f"{NUMBER_WORDS.get(value, 99)} people"
        return None
    value = match.group(1).lower()
    if value in {"solo founder", "just me"}:
        return "1 person"
    if value in {"только я", "я один"}:
        return "1 person"
    if value in {"just two of us", "нас двое"}:
        return "2 people"
    if value in {"me and one contractor", "me plus one contractor", "one contractor and me"}:
        return "2 people"
    if value.startswith("команда из "):
        digits = re.search(r"(\d+)", value)
        return f"{digits.group(1)} people" if digits else value
    if value.startswith("команда "):
        digits = re.search(r"(\d+)", value)
        if digits:
            return f"{digits.group(1)} people"
        for word, number in NUMBER_WORDS.items():
            if word in value:
                return f"{number} people"
    if value.startswith("team of "):
        digits = re.search(r"(\d+)", value)
        if digits:
            return f"{digits.group(1)} people"
        for word, number in NUMBER_WORDS.items():
            if word in value:
                return f"{number} people"
    for word, number in NUMBER_WORDS.items():
        if word in value:
            return f"{number} people"
    return value


def infer_budget_hint(text: str) -> str | None:
    """Infer a human-facing budget hint when no numeric range was captured."""

    numeric = extract_first_match(BUDGET_PATTERN, text)
    if numeric:
        return numeric
    for pattern in LOW_BUDGET_HINT_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0).strip(" .,;:")
    return None


def infer_platform_hints(lowered: str) -> list[str]:
    """Infer platform hints from direct keywords."""

    hints = []
    keyword_map = {
        r"\blocal-first\b": "local-first",
        r"\boffline\b": "offline-friendly",
        r"\bофлайн\b": "offline-friendly",
        r"\bлокальн": "local-first",
        r"\bbrowser\b": "browser-ui-planned",
        r"\bweb\b": "web",
        r"\bвеб\b": "web",
        r"\bmobile\b": "mobile",
        r"\bмобиль": "mobile",
        r"\bios\b": "mobile",
        r"\bandroid\b": "mobile",
        r"\bdesktop\b": "desktop",
        r"\bдесктоп\b": "desktop",
        r"\bcli\b": "cli",
        r"\bapi\b": "api",
        r"\binternal tool\b": "internal-tool",
        r"\bвнутренн(?:ий|его)\s+инструмент": "internal-tool",
    }
    for pattern, label in keyword_map.items():
        if re.search(pattern, lowered):
            hints.append(label)
    return dedupe(hints)


def infer_audience_hint(lowered: str) -> str | None:
    """Infer whether the brief leans B2B, B2C, or internal."""

    if (
        "internal" in lowered
        or "ops team" in lowered
        or "operations team" in lowered
        or "внутрен" in lowered
        or "операцион" in lowered
    ):
        return "internal"
    if any(
        word in lowered
        for word in ["b2b", "clients", "agency", "enterprise", "клиент", "агентств", "b2b"]
    ):
        return "b2b"
    if any(word in lowered for word in ["b2c", "consumers", "пользовател", "потребител"]):
        return "b2c"
    return None


def infer_tradeoffs(lowered: str) -> list[str]:
    """Infer coarse delivery tradeoff hints from wording."""

    tradeoffs = []
    if any(
        word in lowered
        for word in ["fast", "quick", "asap", "mvp", "prototype", "быстро", "срочно", "быстрый"]
    ):
        tradeoffs.append("speed prioritized")
    if any(pattern.search(lowered) for pattern in LOW_BUDGET_HINT_PATTERNS) or any(
        word in lowered for word in ["under $", "below $", "бюджет до ", "до $"]
    ):
        tradeoffs.append("budget prioritized")
    if any(
        word in lowered
        for word in [
            "quality",
            "reliable",
            "accurate",
            "polished",
            "качеств",
            "надежн",
            "полирован",
        ]
    ):
        tradeoffs.append("quality prioritized")
    return tradeoffs


def contains_vague_goals(goals: list[str]) -> bool:
    """Return whether the current goals are still too vague."""

    vague_terms = [
        "better",
        "easier",
        "modern",
        "powerful",
        "innovative",
        "premium",
        "feature-rich",
        "all-in-one",
        "удобн",
        "мощн",
        "современн",
        "все в одном",
    ]
    return any(any(term in goal.lower() for term in vague_terms) for goal in goals)


def has_success_signal(brief: NormalizedBrief) -> bool:
    """Return whether the brief suggests measurable success."""

    if any(NUMERIC_PATTERN.search(goal) for goal in brief.goals):
        return True
    lowered = brief.normalized_text.lower()
    return any(
        word in lowered
        for word in [
            "success means",
            "metric",
            "kpi",
            "reduce",
            "increase",
            "критер",
            "метрик",
            "успех",
            "сниз",
            "увелич",
        ]
    )


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
        "подписк",
        "выручк",
        "платн",
        "монетиза",
        "тариф",
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
            "multiple roles",
            "admin",
            "billing",
            "integrations",
            "workflow automation",
            "approval flow",
            "permissions",
            "role",
            "все в одном",
            "несколько ролей",
            "админ",
            "биллинг",
            "интеграц",
            "согласован",
            "доступ",
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
            "энтерпрайз",
            "аудит",
            "роли",
            "комплаенс",
        ]
    )


def count_integration_signals(lowered: str) -> int:
    """Count integration-like scope markers for overloaded first releases."""

    families = {
        "integration": ["integration", "integrations", "интеграц"],
        "crm": ["salesforce", "hubspot", "crm", "erp"],
        "messaging": ["slack", "email", "почт"],
        "calendar": ["calendar", "календар"],
        "billing": ["stripe", "billing", "биллинг"],
        "analytics": ["analytics", "аналитик", "reporting", "reports", "отчет"],
        "admin": ["admin", "permissions", "role", "roles", "админ", "доступ", "роли"],
        "enterprise_controls": ["audit", "sso", "compliance", "аудит", "комплаенс"],
    }
    return sum(1 for markers in families.values() if any(marker in lowered for marker in markers))


def has_low_budget_signal(text: str, budget_text: str | None = None) -> bool:
    """Return whether the brief points to a materially tight budget."""

    lowered = text.lower()
    budget_lowered = (budget_text or "").lower()
    if any(pattern.search(budget_lowered or lowered) for pattern in LOW_BUDGET_HINT_PATTERNS):
        return True
    money_source = budget_lowered or lowered
    match = re.search(r"\$([\d,]+)([kKmM]?)", money_source)
    if not match:
        return False
    amount = Decimal(match.group(1).replace(",", ""))
    suffix = match.group(2).lower()
    if suffix == "k":
        amount *= 1000
    elif suffix == "m":
        amount *= 1_000_000
    return amount <= 20000


def has_simple_mvp_signal(lowered: str) -> bool:
    """Return whether the brief frames the first release as a simple MVP."""

    cleaned = POST_MVP_PATTERN.sub("", lowered)
    return any(
        word in cleaned
        for word in [
            "mvp",
            "minimal",
            "prototype",
            "simple mvp",
            "simple prototype",
            "lean mvp",
            "basic mvp",
            "простой mvp",
            "минимальн",
            "прототип",
            "простое приложение",
        ]
    )


def has_phased_scope_signal(lowered: str) -> bool:
    """Return whether secondary scope is explicitly deferred to a later phase."""

    return bool(PHASED_SCOPE_PATTERN.search(lowered))


def has_short_timeline_signal(text: str, timeline_text: str | None = None) -> bool:
    """Return whether the brief asks for a notably compressed timeline."""

    lowered = text.lower()
    timeline_lowered = (timeline_text or "").lower()
    if any(
        term in timeline_lowered or term in lowered
        for term in [
            "asap",
            "urgent",
            "quickly",
            "launch quickly",
            "move fast",
            "rush",
            "within ",
            "short timeline",
            "срочно",
            "как можно скорее",
            "быстро",
            "в короткий срок",
        ]
    ):
        return True
    match = re.search(
        r"(\d+)\s*(day|days|week|weeks|день|дня|дней|недел[яьию]?)",
        timeline_lowered or lowered,
    )
    if not match:
        return False
    amount = int(match.group(1))
    unit = match.group(2)
    if "day" in unit or "д" in unit:
        return amount <= 21
    return amount <= 6


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
            "персональные данные",
            "финансов",
            "комплаенс",
            "аудит",
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
            "безопас",
            "шифрован",
            "аудит",
        ]
    )


def has_owner_signal(lowered: str) -> bool:
    """Return whether an owner/operator signal exists for internal tools."""

    return any(
        word in lowered
        for word in [
            "owner",
            "admin",
            "operations lead",
            "support lead",
            "maintain",
            "владел",
            "админ",
            "поддержива",
            "отвечает",
        ]
    )


def infer_team_size_count(team_size: str | None) -> int:
    """Reduce a team-size string to a rough integer count."""

    if not team_size:
        return 99
    match = re.search(r"(\d+)", team_size)
    if match:
        return int(match.group(1))
    for word, number in NUMBER_WORDS.items():
        if word in team_size:
            return number
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
