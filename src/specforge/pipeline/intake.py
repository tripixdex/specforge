"""Deterministic intake normalization for SpecForge."""

from __future__ import annotations

import re

from specforge.domain.models import NormalizedBrief, RawBrief
from specforge.pipeline.naming import derive_title

SECTION_NAMES = {
    "goal": "goals",
    "goals": "goals",
    "цель": "goals",
    "цели": "goals",
    "non-goal": "non_goals",
    "non-goals": "non_goals",
    "не цель": "non_goals",
    "не-цель": "non_goals",
    "constraints": "constraints",
    "constraint": "constraints",
    "ограничения": "constraints",
    "ограничение": "constraints",
    "audience": "audience",
    "users": "audience",
    "user": "audience",
    "аудитория": "audience",
    "пользователи": "audience",
    "пользователь": "audience",
    "notes": "notes",
    "заметки": "notes",
    "references": "references",
    "refs": "references",
    "ссылки": "references",
    "risks": "risks",
    "риски": "risks",
}

BULLET_PATTERN = re.compile(r"^(?:[-*•]|\d+\.)\s+(?P<value>.+)$")
SECTION_PATTERN = re.compile(r"^(?P<name>[^:]{1,40}):\s*(?P<value>.*)$")
URL_PATTERN = re.compile(r"https?://\S+")


def create_raw_brief(
    source_text: str,
    *,
    title: str | None = None,
    metadata: dict[str, str] | None = None,
) -> RawBrief:
    """Build a `RawBrief` from text and optional metadata."""

    cleaned_text = normalize_text(source_text)
    raw_title = derive_title(cleaned_text, provided_title=title)
    raw_metadata = metadata or {}
    return RawBrief(
        title=raw_title,
        source_text=cleaned_text,
        source_type=raw_metadata.get("source_type", "freeform-notes"),
        product_type=raw_metadata.get("product_type"),
        metadata=raw_metadata,
    )


def normalize_brief(raw_brief: RawBrief) -> NormalizedBrief:
    """Convert a raw brief into a deterministic structured form."""

    normalized_text = normalize_text(raw_brief.source_text)
    sections = collect_sections(normalized_text)
    explicit_constraints = dedupe(
        raw_brief.constraints.explicit_constraints
        + sections["constraints"]
        + infer_constraint_lines(normalized_text)
    )
    notes = dedupe(raw_brief.notes + sections["notes"])
    references = dedupe(
        raw_brief.references + sections["references"] + URL_PATTERN.findall(normalized_text)
    )
    risks = dedupe(sections["risks"])
    product_type = raw_brief.product_type or infer_product_type(normalized_text)
    audience = dedupe(raw_brief.audience + sections["audience"] + infer_audience(normalized_text))
    goals = dedupe(raw_brief.goals + sections["goals"] + infer_goals(normalized_text))
    non_goals = dedupe(
        raw_brief.non_goals
        + raw_brief.constraints.non_goals
        + sections["non_goals"]
        + infer_non_goals(normalized_text)
    )
    summary = summarize_text(normalized_text)
    constraints = raw_brief.constraints.model_copy(
        update={
            "explicit_constraints": explicit_constraints,
            "non_goals": non_goals,
            "notes": dedupe(raw_brief.constraints.notes + notes),
        }
    )

    return NormalizedBrief(
        title=raw_brief.title,
        source_text=raw_brief.source_text,
        normalized_text=normalized_text,
        summary=summary,
        product_type=product_type,
        audience=audience,
        goals=goals,
        non_goals=non_goals,
        constraints=constraints,
        risks=risks,
        notes=notes,
        references=references,
    )


def normalize_text(text: str) -> str:
    """Normalize whitespace while preserving line-based structure."""

    lines = [re.sub(r"\s+", " ", line).strip() for line in text.replace("\r\n", "\n").split("\n")]
    compact_lines: list[str] = []
    previous_blank = False
    for line in lines:
        if not line:
            if not previous_blank:
                compact_lines.append("")
            previous_blank = True
            continue
        compact_lines.append(line)
        previous_blank = False
    return "\n".join(compact_lines).strip()


def collect_sections(text: str) -> dict[str, list[str]]:
    """Parse obvious colon-based sections and bullets."""

    sections = {name: [] for name in set(SECTION_NAMES.values())}
    current_section: str | None = None

    for line in text.splitlines():
        header_match = SECTION_PATTERN.match(line)
        if header_match:
            section_name = SECTION_NAMES.get(header_match.group("name").strip().lower())
            if section_name:
                current_section = section_name
                value = header_match.group("value").strip()
                if value:
                    sections[current_section].append(value)
                continue

        bullet_match = BULLET_PATTERN.match(line)
        if bullet_match and current_section:
            sections[current_section].append(bullet_match.group("value").strip())
            continue

        if current_section and line:
            sections[current_section].append(line)

    return {key: dedupe(value) for key, value in sections.items()}


def infer_title(text: str) -> str:
    """Use the first non-empty line as the fallback title."""

    return derive_title(text)


def infer_product_type(text: str) -> str | None:
    """Infer a coarse product type from obvious keywords."""

    lowered = text.lower()
    keyword_map = [
        ("internal tool", "internal tool"),
        ("внутренний инструмент", "internal tool"),
        ("dashboard", "dashboard"),
        ("дашборд", "dashboard"),
        ("marketplace", "marketplace"),
        ("маркетплейс", "marketplace"),
        ("mobile app", "mobile app"),
        ("мобильное приложение", "mobile app"),
        ("web app", "web app"),
        ("веб-приложение", "web app"),
        ("portal", "portal"),
        ("портал", "portal"),
        ("api", "api"),
        ("automation", "automation tool"),
        ("автоматиза", "automation tool"),
        ("tool", "software tool"),
        ("инструмент", "software tool"),
        ("app", "software app"),
        ("приложение", "software app"),
    ]
    for keyword, product_type in keyword_map:
        if keyword in lowered:
            return product_type
    return None


def infer_audience(text: str) -> list[str]:
    """Infer likely user groups from plain-language mentions."""

    lowered = text.lower()
    audience = []
    keyword_map = {
        "founders": "founders",
        "фаундер": "founders",
        "основател": "founders",
        "small businesses": "small businesses",
        "малый бизнес": "small businesses",
        "clients": "clients",
        "клиенты": "clients",
        "agencies": "agencies",
        "агентств": "agencies",
        "consultants": "consultants",
        "консультант": "consultants",
        "operations team": "operations team",
        "ops team": "operations team",
        "операционн": "operations team",
        "internal team": "internal team",
        "внутренняя команда": "internal team",
        "sales team": "sales team",
        "отдел продаж": "sales team",
        "support team": "support team",
        "поддержк": "support team",
    }
    for keyword, label in keyword_map.items():
        if keyword in lowered:
            audience.append(label)
    return dedupe(audience)


def infer_goals(text: str) -> list[str]:
    """Infer goal statements from obvious directive language."""

    goals: list[str] = []
    goal_markers = [
        "goal",
        "need to",
        "must",
        "should",
        "want to",
        "success means",
        "нужно",
        "надо",
        "хочу",
        "должно",
        "цель",
        "успех",
    ]
    excluded_markers = [
        "budget",
        "timeline",
        "deadline",
        "team",
        "reference",
        "local-first",
        "non-goal",
        "не цель",
        "no ",
        "don't",
        "avoid",
    ]
    for line in text.splitlines():
        lowered = line.lower()
        if line.endswith(":"):
            continue
        if any(marker in lowered for marker in goal_markers):
            if not any(marker in lowered for marker in excluded_markers):
                goals.append(clean_lead_in(line))
    return dedupe(goals)


def infer_non_goals(text: str) -> list[str]:
    """Infer explicit non-goals from negative language."""

    non_goals: list[str] = []
    markers = [
        "non-goal",
        "non goal",
        "do not",
        "don't",
        "avoid",
        "no ",
        "не цель",
        "избегать",
        "не нужно",
        "не надо",
    ]
    for line in text.splitlines():
        lowered = line.lower()
        if line.endswith(":"):
            continue
        if any(marker in lowered for marker in markers):
            non_goals.append(clean_lead_in(line))
    return dedupe(non_goals)


def infer_constraint_lines(text: str) -> list[str]:
    """Capture lines that look like explicit project constraints."""

    constraint_lines: list[str] = []
    markers = [
        "budget",
        "бюджет",
        "timeline",
        "срок",
        "deadline",
        "дедлайн",
        "team",
        "команда",
        "local-first",
        "локально",
        "offline",
        "офлайн",
        "must",
        "должно",
        "cannot",
        "can't",
        "нельзя",
    ]
    for line in text.splitlines():
        lowered = line.lower()
        if any(marker in lowered for marker in markers):
            constraint_lines.append(clean_lead_in(line))
    return dedupe(constraint_lines)


def summarize_text(text: str, limit: int = 240) -> str:
    """Create a compact deterministic summary from the first sentences."""

    compact = text.replace("\n", " ")
    compact = re.sub(r"\s+", " ", compact).strip()
    if len(compact) <= limit:
        return compact
    truncated = compact[:limit].rsplit(" ", 1)[0].strip()
    return f"{truncated}..."


def clean_lead_in(value: str) -> str:
    """Remove list markers and preserve the rest of the sentence."""

    cleaned = BULLET_PATTERN.sub(r"\g<value>", value).strip()
    return cleaned.rstrip(".")


def dedupe(values: list[str]) -> list[str]:
    """Deduplicate values while preserving order."""

    seen: set[str] = set()
    items: list[str] = []
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            items.append(cleaned)
    return items
