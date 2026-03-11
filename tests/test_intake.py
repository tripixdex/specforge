from specforge.pipeline.intake import create_raw_brief, normalize_brief


def test_intake_normalization_extracts_sections_and_whitespace() -> None:
    text = """
    Founder App Idea

    Goals:
    - Help founders turn messy notes into a plan
    - Keep everything local-first

    Non-Goals:
    - No cloud sync

    Constraints:
    - Budget under $15k
    - Need a usable draft in 4 weeks

    Notes:
    - Maybe web app first
    """

    raw = create_raw_brief(text)
    brief = normalize_brief(raw)

    assert raw.title == "Founder App Idea"
    assert "Help founders turn messy notes into a plan" in brief.goals
    assert "No cloud sync" in brief.non_goals
    assert "Budget under $15k" in brief.constraints.explicit_constraints
    assert "Maybe web app first" in brief.notes
    assert "Goals:" not in brief.goals
    assert "Non-Goals:" not in brief.non_goals
    assert "\n\n\n" not in brief.normalized_text
