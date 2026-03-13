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
        "ru": "Минимальный MVP против корпоративного объема",
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

PRODUCT_TYPE_LABELS: dict[str, dict[Locale, str]] = {
    "internal tool": {"en": "internal tool", "ru": "внутренний инструмент"},
    "dashboard": {"en": "dashboard", "ru": "дашборд"},
    "marketplace": {"en": "marketplace", "ru": "маркетплейс"},
    "mobile app": {"en": "mobile app", "ru": "мобильное приложение"},
    "web app": {"en": "web app", "ru": "веб-приложение"},
    "portal": {"en": "portal", "ru": "портал"},
    "api": {"en": "API product", "ru": "API-продукт"},
    "automation tool": {"en": "automation tool", "ru": "инструмент автоматизации"},
    "software tool": {"en": "software tool", "ru": "программный инструмент"},
    "software app": {"en": "software app", "ru": "программное приложение"},
}

AUDIENCE_LABELS: dict[str, dict[Locale, str]] = {
    "founders": {"en": "founders", "ru": "фаундеры"},
    "small businesses": {"en": "small businesses", "ru": "малый бизнес"},
    "clients": {"en": "clients", "ru": "клиенты"},
    "agencies": {"en": "agencies", "ru": "агентства"},
    "consultants": {"en": "consultants", "ru": "консультанты"},
    "operations team": {"en": "operations team", "ru": "операционная команда"},
    "internal team": {"en": "internal team", "ru": "внутренняя команда"},
    "sales team": {"en": "sales team", "ru": "команда продаж"},
    "support team": {"en": "support team", "ru": "команда поддержки"},
}

AUDIENCE_MODE_LABELS: dict[str, dict[Locale, str]] = {
    "internal": {"en": "internal", "ru": "внутренний"},
    "b2b": {"en": "B2B", "ru": "B2B"},
    "b2c": {"en": "B2C", "ru": "B2C"},
}

PLATFORM_HINT_LABELS: dict[str, dict[Locale, str]] = {
    "local-first": {"en": "local-first", "ru": "локальная работа"},
    "offline-friendly": {"en": "offline-friendly", "ru": "офлайн-режим"},
    "browser-ui-planned": {"en": "browser UI", "ru": "браузерный интерфейс"},
    "web": {"en": "web", "ru": "веб"},
    "mobile": {"en": "mobile", "ru": "мобильное приложение"},
    "desktop": {"en": "desktop", "ru": "десктоп"},
    "cli": {"en": "CLI", "ru": "CLI"},
    "api": {"en": "API", "ru": "API"},
    "internal-tool": {"en": "internal tool", "ru": "внутренний инструмент"},
}

TRADEOFF_LABELS: dict[str, dict[Locale, str]] = {
    "speed prioritized": {"en": "speed prioritized", "ru": "приоритет скорости"},
    "budget prioritized": {"en": "budget prioritized", "ru": "приоритет бюджета"},
    "quality prioritized": {"en": "quality prioritized", "ru": "приоритет качества"},
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


def display_product_type(value: str | None, locale: Locale) -> str | None:
    """Return a localized product-type label for human-facing output."""

    if not value:
        return None
    localized = PRODUCT_TYPE_LABELS.get(value, {})
    return localized.get(locale, value)


def display_audience(values: list[str], locale: Locale) -> list[str]:
    """Return localized audience labels for human-facing output."""

    rendered = []
    for value in values:
        localized = AUDIENCE_LABELS.get(value, {})
        rendered.append(localized.get(locale, value))
    return rendered


def display_audience_mode(value: str | None, locale: Locale) -> str | None:
    """Return a localized audience-mode label for human-facing output."""

    if not value:
        return None
    localized = AUDIENCE_MODE_LABELS.get(value, {})
    return localized.get(locale, value)


def display_platform_hints(values: list[str], locale: Locale) -> list[str]:
    """Return localized platform-hint labels for human-facing output."""

    rendered = []
    for value in values:
        localized = PLATFORM_HINT_LABELS.get(value, {})
        rendered.append(localized.get(locale, value))
    return rendered


def display_tradeoffs(values: list[str], locale: Locale) -> list[str]:
    """Return localized tradeoff labels for human-facing output."""

    rendered = []
    for value in values:
        localized = TRADEOFF_LABELS.get(value, {})
        rendered.append(localized.get(locale, value))
    return rendered


def display_team_size(value: str | None, locale: Locale) -> str | None:
    """Return a localized team-size label for human-facing output."""

    if not value or locale == "en":
        return value
    match = re.search(r"(\d+)", value)
    if not match:
        return value
    count = int(match.group(1))
    remainder_10 = count % 10
    remainder_100 = count % 100
    if remainder_10 == 1 and remainder_100 != 11:
        noun = "человек"
    elif remainder_10 in {2, 3, 4} and remainder_100 not in {12, 13, 14}:
        noun = "человека"
    else:
        noun = "человек"
    return f"{count} {noun}"
