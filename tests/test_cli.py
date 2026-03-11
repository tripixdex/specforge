import os
import subprocess
import sys
from pathlib import Path


def test_cli_analyze_happy_path(tmp_path: Path) -> None:
    input_path = tmp_path / "brief.txt"
    input_path.write_text(
        "Need something modern for everyone. Maybe web or mobile.\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd() / "src")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "specforge.cli",
            "analyze",
            "--input",
            str(input_path),
        ],
        capture_output=True,
        env=env,
        text=True,
        check=True,
    )

    assert "Ambiguities:" in result.stdout
    assert "Recommended MVP cut:" in result.stdout


def test_cli_generate_happy_path(tmp_path: Path) -> None:
    input_path = tmp_path / "brief.txt"
    input_path.write_text(
        "Founder Tool\nGoals:\n- Help founders scope work\nConstraints:\n- Budget under $20k\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd() / "src")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "specforge.cli",
            "generate",
            "--input",
            str(input_path),
            "--output-root",
            str(tmp_path / "out"),
            "--run-label",
            "cli-happy-path",
        ],
        capture_output=True,
        env=env,
        text=True,
        check=True,
    )

    assert "Output:" in result.stdout
    output_line = result.stdout.splitlines()[0]
    output_dir = Path(output_line.replace("Output: ", "", 1))
    assert output_dir.exists()
    assert (output_dir / "analysis_report.md").exists()


def test_cli_rejects_empty_input(tmp_path: Path) -> None:
    input_path = tmp_path / "empty.txt"
    input_path.write_text("   \n", encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd() / "src")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "specforge.cli",
            "analyze",
            "--input",
            str(input_path),
        ],
        capture_output=True,
        env=env,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "brief_text must not be empty" in result.stderr
