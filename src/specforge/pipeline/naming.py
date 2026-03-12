"""Deterministic title and filesystem naming helpers."""

from __future__ import annotations

import re
from datetime import UTC, datetime

from specforge.pipeline.language import Locale, detect_language

CYRILLIC_TO_LATIN = str.maketrans(
    {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }
)

WEAK_TITLES = {
    "brief",
    "untitled brief",
    "product brief",
    "new brief",
    "idea",
    "app",
    "application",
    "бриф",
    "идея",
    "приложение",
    "без названия",
    "новый бриф",
}

TITLE_STOPWORDS = {
    "en": {"need", "want", "build", "make", "create", "simple", "new"},
    "ru": {"хочу", "нужно", "надо", "сделать", "создать", "простой", "новый"},
}

PRODUCT_FALLBACKS = [
    ("internal tool", {"en": "Internal operations tool", "ru": "Внутренний рабочий инструмент"}),
    ("dashboard", {"en": "Planning dashboard", "ru": "Планировочный дашборд"}),
    ("portal", {"en": "Client portal idea", "ru": "Идея клиентского портала"}),
    ("marketplace", {"en": "Marketplace idea", "ru": "Идея маркетплейса"}),
    ("api", {"en": "API product brief", "ru": "Бриф по API-продукту"}),
    ("automation", {"en": "Automation tool brief", "ru": "Бриф по инструменту автоматизации"}),
    ("mobile app", {"en": "Mobile app brief", "ru": "Бриф по мобильному приложению"}),
    ("web app", {"en": "Web app brief", "ru": "Бриф по веб-приложению"}),
    ("tool", {"en": "Software tool brief", "ru": "Бриф по программному инструменту"}),
    ("app", {"en": "Software app brief", "ru": "Бриф по приложению"}),
]


def derive_title(source_text: str, provided_title: str | None = None) -> str:
    """Return a concise deterministic title from explicit or inferred input."""

    candidate = clean_title_candidate(provided_title or "")
    if candidate and not is_weak_title(candidate):
        return candidate

    locale = detect_language(source_text)
    for line in source_text.splitlines():
        cleaned = clean_title_candidate(line)
        if cleaned and not is_weak_title(cleaned):
            return cleaned

    inferred = infer_product_title(source_text, locale)
    if inferred:
        return inferred
    return default_title(locale)


def clean_title_candidate(value: str) -> str:
    """Normalize a human-facing title candidate."""

    cleaned = re.sub(r"\s+", " ", value).strip(" -:_\t")
    if not cleaned:
        return ""
    cleaned = cleaned.rstrip(".")
    words = cleaned.split()
    if len(words) > 8:
        cleaned = " ".join(words[:8])
    return cleaned[:80].strip()


def is_weak_title(title: str) -> bool:
    """Return whether a title is too generic for output naming."""

    normalized = re.sub(r"\s+", " ", title).strip().lower()
    if not normalized or normalized in WEAK_TITLES:
        return True
    words = re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", normalized)
    if len(words) <= 1 and normalized in {"app", "tool", "idea", "бриф", "идея"}:
        return True
    if len(words) <= 2 and all(
        word in TITLE_STOPWORDS[detect_language(normalized)] for word in words
    ):
        return True
    return len(normalized) < 4


def default_bundle_name(title: str) -> str:
    """Create a timestamped default bundle name."""

    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    stem = slugify(title) or "specforge-brief"
    return f"{stem}-{timestamp}"


def slugify(value: str) -> str:
    """Create a filesystem-safe directory name with Cyrillic transliteration."""

    transliterated = transliterate(value).lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", transliterated).strip("-")
    return slug or "specforge-output"


def transliterate(value: str) -> str:
    """Transliterate Cyrillic text to ASCII for output folders."""

    lowered = value.lower()
    return lowered.translate(CYRILLIC_TO_LATIN)


def infer_product_title(source_text: str, locale: Locale) -> str | None:
    """Pick a deterministic fallback title from coarse product keywords."""

    lowered = source_text.lower()
    for keyword, labels in PRODUCT_FALLBACKS:
        if keyword in lowered:
            return labels[locale]
    if locale == "ru" and "прилож" in lowered:
        return "Бриф по приложению"
    if locale == "ru" and "сервис" in lowered:
        return "Бриф по сервису"
    return None


def default_title(locale: Locale) -> str:
    """Return a locale-specific generic title."""

    return "Новый продуктовый бриф" if locale == "ru" else "New product brief"
