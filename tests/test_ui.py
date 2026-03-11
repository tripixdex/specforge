from fastapi.testclient import TestClient

from specforge.api.app import app

client = TestClient(app)


def test_ui_home_route_is_available() -> None:
    response = client.get("/ui")

    assert response.status_code == 200
    assert "SpecForge Stage 4" in response.text
    assert "Run analysis" in response.text


def test_ui_analyze_renders_guided_results() -> None:
    response = client.post(
        "/ui/analyze",
        data={
            "title": "Founder Tool",
            "brief_text": (
                "Founder Tool\nGoals:\n- Help founders scope work\n"
                "Constraints:\n- Keep it local-first\n"
            ),
            "demo_name": "founder-app-idea",
            "output_label": "",
        },
    )

    assert response.status_code == 200
    assert "Guided Results" in response.text
    assert "Ambiguity Findings" in response.text
    assert "Recommended MVP Cut" in response.text


def test_ui_generate_renders_artifact_preview() -> None:
    response = client.post(
        "/ui/generate",
        data={
            "title": "Internal Ops Tool",
            "brief_text": (
                "Internal Ops Tool\nGoals:\n- Reduce reporting work\n"
                "Constraints:\n- Keep it local-first\n- Budget under $10k\n"
            ),
            "demo_name": "internal-operations-tool",
            "output_label": "ui-smoke-demo",
        },
    )

    assert response.status_code == 200
    assert "Generated Bundle" in response.text
    assert "analysis_report.md" in response.text
    assert "outputs/ui-smoke-demo" in response.text
