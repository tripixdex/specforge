"""Small locale helpers for deterministic English and Russian output."""

from __future__ import annotations

import re
from typing import Literal

Locale = Literal["en", "ru"]

CYRILLIC_PATTERN = re.compile(r"[А-Яа-яЁё]")

CATEGORY_LABELS: dict[str, dict[Locale, str]] = {
    "audience": {"en": "Audience", "ru": "Аудитория"},
    "budget": {"en": "Budget", "ru": "Бюджет"},
    "compliance_security": {"en": "Security and compliance", "ru": "Безопасность и комплаенс"},
    "delivery": {"en": "Delivery", "ru": "Поставка"},
    "deployment": {"en": "Deployment", "ru": "Развертывание"},
    "fast-cheap-feature-rich": {
        "en": "Fast, cheap, and feature-rich at once",
        "ru": "Быстро, дешево и широко по функционалу сразу",
    },
    "goals": {"en": "Goals", "ru": "Цели"},
    "minimal-mvp-vs-enterprise-scope": {
        "en": "Minimal MVP vs enterprise scope",
        "ru": "Минимальный MVP против enterprise-объема",
    },
    "monetization": {"en": "Monetization", "ru": "Монетизация"},
    "ownership_operations": {"en": "Ownership and operations", "ru": "Владелец и эксплуатация"},
    "platform": {"en": "Platform", "ru": "Платформа"},
    "pricing": {"en": "Pricing", "ru": "Ценообразование"},
    "scope": {"en": "Scope", "ru": "Объем"},
    "small-team-aggressive-deadline-broad-scope": {
        "en": "Small team, short deadline, broad scope",
        "ru": "Маленькая команда, короткий срок, широкий объем",
    },
    "success_criteria": {"en": "Success criteria", "ru": "Критерии успеха"},
    "target_user": {"en": "Target user", "ru": "Целевой пользователь"},
    "timeline": {"en": "Timeline", "ru": "Сроки"},
}


def detect_language(text: str) -> Locale:
    """Infer whether input should render in English or Russian."""

    return "ru" if CYRILLIC_PATTERN.search(text) else "en"


def category_label(category: str, locale: Locale) -> str:
    """Return a human-facing category label in the requested locale."""

    localized = CATEGORY_LABELS.get(category, {})
    if locale in localized:
        return localized[locale]
    if locale == "ru":
        return category.replace("-", " ")
    return category.replace("-", " ").title()
