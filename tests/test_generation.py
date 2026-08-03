from __future__ import annotations

from pathlib import Path

from readmekit.detector import detect_project
from readmekit.generator import generate_all, generate_document, write_document, write_documents
from readmekit.models import DocumentKind, GeneratorOptions, ReadmeStyle


def make_python_project(path: Path) -> None:
    (path / "pyproject.toml").write_text(
        """
[project]
name = "sample-cli"
description = "A sample command-line project."
requires-python = ">=3.9"
license = { text = "MIT" }
authors = [{ name = "Nitish Vimal" }]
dependencies = ["typer>=0.12", "rich>=13"]

[project.optional-dependencies]
dev = ["pytest>=8", "ruff>=0.5"]

[project.scripts]
sample = "sample.cli:app"
""".strip(),
        encoding="utf-8",
    )
    (path / "src" / "sample").mkdir(parents=True)
    (path / "src" / "sample" / "__init__.py").write_text("", encoding="utf-8")
    (path / "tests").mkdir()
    (path / "tests" / "test_sample.py").write_text("def test_ok(): assert True\n", encoding="utf-8")


def test_generate_readme_contains_project_specific_sections(tmp_path: Path) -> None:
    make_python_project(tmp_path)
    meta = detect_project(tmp_path)

    document = generate_document(
        DocumentKind.README,
        meta,
        GeneratorOptions(style=ReadmeStyle.PROFESSIONAL, author="Nitish Vimal"),
    )

    assert document.relative_path == Path("README.md")
    assert "# Sample-Cli" in document.content or "# Sample Cli" in document.content
    assert "A sample command-line project." in document.content
    assert "sample --help" in document.content
    assert "Nitish Vimal" in document.content


def test_generate_all_includes_github_templates(tmp_path: Path) -> None:
    make_python_project(tmp_path)
    meta = detect_project(tmp_path)

    documents = generate_all(meta, GeneratorOptions())
    paths = {doc.relative_path.as_posix() for doc in documents}

    assert "README.md" in paths
    assert "CONTRIBUTING.md" in paths
    assert "SECURITY.md" in paths
    assert "CODE_OF_CONDUCT.md" in paths
    assert ".github/ISSUE_TEMPLATE/bug_report.md" in paths
    assert ".github/ISSUE_TEMPLATE/feature_request.md" in paths
    assert ".github/pull_request_template.md" in paths


def test_write_document_skips_existing_file_without_force(tmp_path: Path) -> None:
    make_python_project(tmp_path)
    meta = detect_project(tmp_path)
    document = generate_document(DocumentKind.README, meta, GeneratorOptions())
    (tmp_path / "README.md").write_text("original\n", encoding="utf-8")

    result = write_document(tmp_path, document, force=False)

    assert result.skipped is True
    assert result.written is False
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "original\n"


def test_write_document_overwrites_with_force(tmp_path: Path) -> None:
    make_python_project(tmp_path)
    meta = detect_project(tmp_path)
    document = generate_document(DocumentKind.README, meta, GeneratorOptions())
    (tmp_path / "README.md").write_text("original\n", encoding="utf-8")

    result = write_document(tmp_path, document, force=True)

    assert result.written is True
    assert "Sample" in (tmp_path / "README.md").read_text(encoding="utf-8")


def test_dry_run_does_not_write_file(tmp_path: Path) -> None:
    make_python_project(tmp_path)
    meta = detect_project(tmp_path)
    document = generate_document(DocumentKind.SECURITY, meta, GeneratorOptions())

    result = write_document(tmp_path, document, dry_run=True)

    assert result.written is False
    assert result.reason == "dry run"
    assert not (tmp_path / "SECURITY.md").exists()


def test_write_documents_creates_nested_github_templates(tmp_path: Path) -> None:
    make_python_project(tmp_path)
    meta = detect_project(tmp_path)
    docs = [
        generate_document(DocumentKind.BUG_REPORT, meta, GeneratorOptions()),
        generate_document(DocumentKind.PULL_REQUEST, meta, GeneratorOptions()),
    ]

    results = write_documents(tmp_path, docs)

    assert all(result.written for result in results)
    assert (tmp_path / ".github" / "ISSUE_TEMPLATE" / "bug_report.md").exists()
    assert (tmp_path / ".github" / "pull_request_template.md").exists()
