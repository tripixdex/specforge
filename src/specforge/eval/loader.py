"""Corpus loading for the local evaluation harness."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import TypeAdapter

from specforge.eval.models import EvalCase

EVAL_ROOT = Path(__file__).resolve().parents[3] / "eval"
CORPUS_FILES = (
    "founder_cases.json",
    "client_cases.json",
    "internal_cases.json",
    "edge_cases.json",
)


def corpus_paths() -> list[Path]:
    """Return the expected corpus files."""

    return [EVAL_ROOT / file_name for file_name in CORPUS_FILES]


def load_eval_cases() -> tuple[list[EvalCase], list[Path]]:
    """Load and validate the Stage 5 eval corpus."""

    adapter = TypeAdapter(list[EvalCase])
    cases: list[EvalCase] = []
    paths = corpus_paths()
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        cases.extend(adapter.validate_python(payload))
    seen: set[str] = set()
    for case in cases:
        if case.case_id in seen:
            raise ValueError(f"Duplicate eval case id: {case.case_id}")
        seen.add(case.case_id)
    return cases, paths
