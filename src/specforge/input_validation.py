"""Shared local input validation helpers."""

from __future__ import annotations

from pathlib import Path

MAX_BRIEF_LENGTH = 20_000
MAX_LABEL_LENGTH = 64
MAX_TITLE_LENGTH = 120
MAX_METADATA_ENTRIES = 20


def normalize_brief_text(value: str) -> str:
    """Reject empty or oversized brief text."""

    stripped = value.strip()
    if not stripped:
        raise ValueError("brief_text must not be empty")
    if len(stripped) > MAX_BRIEF_LENGTH:
        raise ValueError(f"brief_text must be at most {MAX_BRIEF_LENGTH} characters")
    return stripped


def normalize_optional_text(value: str | None, *, field_name: str, max_length: int) -> str | None:
    """Strip optional text fields and enforce a compact size limit."""

    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    if len(stripped) > max_length:
        raise ValueError(f"{field_name} must be at most {max_length} characters")
    return stripped


def normalize_metadata(value: dict[str, str]) -> dict[str, str]:
    """Keep metadata small and stringly typed."""

    if len(value) > MAX_METADATA_ENTRIES:
        raise ValueError(f"metadata may include at most {MAX_METADATA_ENTRIES} entries")
    return {
        str(key).strip(): str(item).strip()
        for key, item in value.items()
        if str(key).strip()
    }


def validate_demo_name(name: str, allowed_names: set[str]) -> str:
    """Reject unknown bundled demo identifiers."""

    candidate = normalize_optional_text(name, field_name="demo_name", max_length=80)
    if candidate is None:
        raise ValueError("demo_name must not be empty")
    if candidate not in allowed_names:
        raise ValueError(
            f"Unknown demo '{candidate}'. Choose one of: {', '.join(sorted(allowed_names))}"
        )
    return candidate


def load_validated_text_file(path: Path) -> str:
    """Read a local text file and apply the shared brief-size guardrails."""

    return normalize_brief_text(path.read_text(encoding="utf-8"))
