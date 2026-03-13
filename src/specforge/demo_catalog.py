"""Bundled demo brief registry for local surfaces."""

from __future__ import annotations

from pathlib import Path

from specforge.input_validation import validate_demo_name

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DEMO_NAME = "founder-app-idea"
DEMO_BRIEFS = {
    "founder-app-idea": Path("examples/founder_app_idea.txt"),
    "contradictory-founder-brief": Path("examples/contradictory_founder_brief.txt"),
    "agency-client-brief": Path("examples/agency_client_brief.txt"),
    "internal-operations-tool": Path("examples/internal_operations_tool_brief.txt"),
}
DEMO_LABELS = {
    "founder-app-idea": "Founder scope tool",
    "contradictory-founder-brief": "Contradictory founder brief",
    "agency-client-brief": "Agency client brief",
    "internal-operations-tool": "Internal operations tool",
}


def default_demo_name() -> str:
    """Return the default bundled demo key."""

    return DEFAULT_DEMO_NAME


def available_demo_names() -> list[str]:
    """Return the ordered bundled demo identifiers."""

    return list(DEMO_BRIEFS)


def demo_options() -> list[tuple[str, str]]:
    """Return UI-friendly demo labels."""

    return [(name, DEMO_LABELS[name]) for name in available_demo_names()]


def resolve_demo_name(name: str) -> str:
    """Validate and normalize a bundled demo identifier."""

    return validate_demo_name(name, set(DEMO_BRIEFS))


def load_demo_brief(demo_name: str) -> tuple[str, str, Path]:
    """Load one bundled demo brief and return its title and absolute path."""

    resolved_name = resolve_demo_name(demo_name)
    relative_path = DEMO_BRIEFS[resolved_name]
    absolute_path = REPO_ROOT / relative_path
    text = absolute_path.read_text(encoding="utf-8")
    title = DEMO_LABELS[resolved_name].title()
    return title, text, absolute_path
