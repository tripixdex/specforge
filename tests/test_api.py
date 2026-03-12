import shutil
from pathlib import Path

from fastapi.testclient import TestClient

from specforge.api.app import app

client = TestClient(app)
REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_ROOT = REPO_ROOT / "outputs"


def test_health_happy_path() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app": "specforge",
        "stage": "stage-5-6-pre-audit-polish",
    }


def test_analyze_happy_path() -> None:
    response = client.post(
        "/analyze",
        json={
            "brief_text": (
                "Founder Tool\nGoals:\n- Help founders scope work\n"
                "Constraints:\n- Keep it local-first\n"
            ),
            "title": "Founder Tool",
            "metadata": {"owner": "demo"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["brief"]["title"] == "Founder Tool"
    assert body["analysis_mode"] == "deterministic"
    assert "counts" in body
    assert body["counts"]["assumptions"] >= 1
    assert isinstance(body["top_open_questions"], list)


def test_generate_happy_path_and_safe_output_label() -> None:
    output_dir = OUTPUTS_ROOT / "api-demo-bundle"
    if output_dir.exists():
        shutil.rmtree(output_dir)

    response = client.post(
        "/generate",
        json={
            "brief_text": (
                "Internal Ops Tool\nGoals:\n- Reduce reporting work\n"
                "Constraints:\n- Keep it local-first\n- Budget under $10k\n"
            ),
            "title": "Internal Ops Tool",
            "output_label": "API Demo Bundle",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["output_path"].endswith("outputs/api-demo-bundle")
    assert Path(body["output_path"]).is_dir()
    assert (Path(body["output_path"]) / "summary.json").exists()
    assert "analysis_report.md" in body["artifact_files"]


def test_analyze_rejects_empty_brief() -> None:
    response = client.post("/analyze", json={"brief_text": "   "})

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"


def test_analyze_rejects_excessive_brief() -> None:
    response = client.post("/analyze", json={"brief_text": "x" * 20001})

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"


def test_generate_rejects_unsafe_output_label() -> None:
    response = client.post(
        "/generate",
        json={
            "brief_text": "Need a simple local API",
            "output_label": "../escape",
        },
    )

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"


def test_generate_accepts_trimmed_output_label() -> None:
    response = client.post(
        "/generate",
        json={
            "brief_text": "Need a simple local API",
            "output_label": "  API Trimmed Bundle  ",
        },
    )

    assert response.status_code == 200
    assert response.json()["output_path"].endswith("outputs/api-trimmed-bundle")


def test_demo_returns_sample_analysis() -> None:
    response = client.get("/demo")

    assert response.status_code == 200
    body = response.json()
    assert body["demo_name"] == "founder-app-idea"
    assert body["sample_analysis"]["analysis_mode"] == "deterministic"
    assert "founder-app-idea" in body["available_demos"]
