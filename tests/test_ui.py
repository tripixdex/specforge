from fastapi.testclient import TestClient

from specforge.api.app import app

client = TestClient(app)


def test_ui_home_route_is_available() -> None:
    response = client.get("/ui")

    assert response.status_code == 200
    assert "SpecForge" in response.text
    assert "Stage 5.9" not in response.text
    assert "Run analysis" in response.text
    assert "New brief" in response.text


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
    assert "Guided results" in response.text
    assert "Ambiguity findings" in response.text
    assert "Recommended MVP cut" in response.text


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
    assert "Generated bundle" in response.text
    assert "analysis_report.md" in response.text
    assert "outputs/ui-smoke-demo" in response.text
    assert "summary.json" not in response.text
    assert "Bundle technical details" in response.text


def test_ui_invalid_demo_selection_is_visible() -> None:
    response = client.get("/ui?demo=does-not-exist")

    assert response.status_code == 200
    assert "Unknown demo" in response.text
    assert "Founder app idea" in response.text


def test_ui_short_brief_shows_humane_clarification_state() -> None:
    response = client.post(
        "/ui/analyze",
        data={
            "title": "",
            "brief_text": "хочу приложение",
            "demo_name": "founder-app-idea",
        },
    )

    assert response.status_code == 200
    assert "Нужно чуть больше контекста" in response.text
    assert "Кто основной пользователь?" in response.text


def test_ui_new_brief_clears_previous_results() -> None:
    response = client.post(
        "/ui/new",
        data={
            "demo_name": "founder-app-idea",
            "previous_brief_text": "хочу приложение",
        },
    )

    assert response.status_code == 200
    assert "Start with analysis" not in response.text
    assert "Начните с анализа" in response.text
    assert "Guided Results" not in response.text


def test_ui_russian_results_localize_count_labels_and_lang() -> None:
    response = client.post(
        "/ui/analyze",
        data={
            "title": "Русский бриф",
            "brief_text": (
                "Нужен простой MVP за 2 недели.\n"
                "Бюджет до $8k.\n"
                "Нужны веб и мобильное приложение, CRM и Slack.\n"
            ),
            "demo_name": "founder-app-idea",
            "output_label": "",
        },
    )

    assert response.status_code == 200
    assert '<html lang="ru">' in response.text
    assert "Противоречия" in response.text
    assert "Основания:" in response.text
    assert "Missing decisions" not in response.text
