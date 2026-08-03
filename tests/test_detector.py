from __future__ import annotations

from pathlib import Path

from readmekit.detector import detect_project
from readmekit.models import ProjectType


def test_detect_python_project_from_pyproject(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
name = "demo-tool"
description = "A demo Python tool."
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [{ name = "Nitish Vimal" }]
dependencies = ["typer>=0.12"]

[project.scripts]
demo = "demo.cli:app"
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_demo.py").write_text("def test_ok(): assert True\n", encoding="utf-8")

    meta = detect_project(tmp_path)

    assert meta.project_type == ProjectType.PYTHON
    assert meta.package_name == "demo-tool"
    assert meta.description == "A demo Python tool."
    assert meta.python_version == ">=3.10"
    assert meta.entry_points == ("demo",)
    assert meta.has_tests is True
    assert "typer>=0.12" in meta.dependencies.runtime


def test_detect_node_project_from_package_json(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(
        '{"name":"demo-app","description":"A demo app.","license":"MIT","dependencies":{"react":"latest"}}',
        encoding="utf-8",
    )

    meta = detect_project(tmp_path)

    assert meta.project_type == ProjectType.NODE
    assert meta.package_name == "demo-app"
    assert meta.description == "A demo app."
    assert "react" in meta.dependencies.runtime


def test_detect_general_project_uses_folder_name(tmp_path: Path) -> None:
    meta = detect_project(tmp_path)

    assert meta.project_type == ProjectType.GENERAL
    assert meta.name == tmp_path.name
    assert meta.license_name == "MIT"
