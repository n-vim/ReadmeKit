from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from readmekit.cli import app
from readmekit.config import load_config, options_from_config
from readmekit.models import ReadmeStyle

runner = CliRunner()


def test_load_config_and_options(tmp_path: Path) -> None:
    (tmp_path / ".readmekit.yaml").write_text(
        """
author: Nitish Vimal
license: MIT
style: detailed
include_code_of_conduct: false
""".strip(),
        encoding="utf-8",
    )

    config = load_config(tmp_path)
    options = options_from_config(config)

    assert options.author == "Nitish Vimal"
    assert options.style == ReadmeStyle.DETAILED
    assert options.include_code_of_conduct is False


def test_cli_init_creates_config(tmp_path: Path) -> None:
    result = runner.invoke(app, ["init", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / ".readmekit.yaml").exists()
    assert "Created" in result.output


def test_cli_inspect_detects_project(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
name = "cli-demo"
description = "CLI demo project."
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["inspect", str(tmp_path)])

    assert result.exit_code == 0
    assert "cli-demo" in result.output or "Cli-Demo" in result.output
    assert "python" in result.output


def test_cli_readme_print_outputs_markdown(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
name = "cli-demo"
description = "CLI demo project."
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["readme", str(tmp_path), "--print"])

    assert result.exit_code == 0
    assert "# Cli Demo" in result.output or "# Cli-Demo" in result.output
    assert "CLI demo project." in result.output
