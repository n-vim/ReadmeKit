"""Document builders for ReadmeKit."""

from __future__ import annotations

from pathlib import Path

from .markdown import badge, bullet, fenced, heading, join_sections, numbered, table
from .models import DocumentKind, GeneratedDocument, GeneratorOptions, ProjectMetadata, ProjectType, ReadmeStyle
from .utils import ensure_trailing_newline


def build_readme(meta: ProjectMetadata, options: GeneratorOptions) -> GeneratedDocument:
    """Build a polished README document for a detected project."""

    badges = _badges(meta)
    sections: list[str] = [_readme_hero(meta, badges)]
    sections.append(_overview(meta))
    sections.append(_features(meta, options.style))
    sections.append(_installation(meta))
    sections.append(_usage(meta))

    if options.style in {ReadmeStyle.PROFESSIONAL, ReadmeStyle.DETAILED}:
        sections.append(_commands(meta))
        sections.append(_configuration(meta))
        sections.append(_project_structure(meta))
        sections.append(_built_with(meta))
        sections.append(_development(meta))

    if options.style == ReadmeStyle.DETAILED:
        sections.append(_quality_notes(meta))
        sections.append(_faq(meta))

    sections.extend([_roadmap(meta), _contributing_short(), _author(meta, options), _license(meta)])
    content = join_sections(*sections)
    return GeneratedDocument(DocumentKind.README, Path("README.md"), ensure_trailing_newline(content))


def build_contributing(meta: ProjectMetadata, options: GeneratorOptions) -> GeneratedDocument:
    """Build CONTRIBUTING.md."""

    content = join_sections(
        heading(1, f"Contributing to {meta.display_name}"),
        "\n".join(
            [
                "Thank you for your interest in contributing.",
                "",
                f"{meta.display_name} is meant to stay useful, readable, and easy to maintain. Contributions are welcome, but every change should keep the project simple and practical.",
            ]
        ),
        heading(2, "Ways to Contribute")
        + "\n\n"
        + bullet(
            [
                "Fix bugs or broken behavior",
                "Improve documentation and examples",
                "Add tests for existing behavior",
                "Improve CLI messages and error handling",
                "Suggest practical features",
                "Refactor code when it improves readability",
            ]
        ),
        heading(2, "Development Setup")
        + "\n\n"
        + "Clone the repository and install it locally:\n\n"
        + fenced(
            "bash",
            f"git clone {meta.repository_url}.git\ncd {meta.name}\npython -m pip install -e \".[dev]\"",
        ),
        heading(2, "Running the Project")
        + "\n\n"
        + _project_run_example(meta),
        heading(2, "Testing and Quality Checks")
        + "\n\n"
        + fenced("bash", _quality_commands(meta)),
        heading(2, "Pull Request Guidelines")
        + "\n\n"
        + bullet(
            [
                "Keep pull requests focused on one clear change",
                "Explain what changed and why it is needed",
                "Add or update tests when behavior changes",
                "Update documentation when user-facing behavior changes",
                "Avoid unrelated formatting changes",
                "Do not commit cache, build, environment, or secret files",
            ]
        ),
        heading(2, "Commit Message Style")
        + "\n\n"
        + "Use clear commit messages that describe the change.\n\n"
        + fenced(
            "text",
            "Add markdown generation tests\nFix config loading for empty YAML files\nImprove CLI output for skipped files",
        ),
        heading(2, "Issue Guidelines")
        + "\n\n"
        + bullet(
            [
                "Use a clear and specific title",
                "Describe the expected behavior",
                "Describe the actual behavior",
                "Include steps to reproduce bugs",
                "Include your operating system and Python version when relevant",
                "For feature requests, explain the problem before the proposed solution",
            ]
        ),
        heading(2, "What to Avoid")
        + "\n\n"
        + bullet(
            [
                "Large rewrites without discussion",
                "Heavy dependencies without a strong reason",
                "Overly complex abstractions",
                "Generated files that do not belong in the repository",
                "Secrets, tokens, passwords, or private data",
            ]
        ),
        heading(2, "License")
        + "\n\n"
        + f"By contributing, you agree that your contributions will be licensed under the {meta.license_name} License.",
    )
    return GeneratedDocument(DocumentKind.CONTRIBUTING, Path("CONTRIBUTING.md"), ensure_trailing_newline(content))


def build_security(meta: ProjectMetadata, options: GeneratorOptions) -> GeneratedDocument:
    """Build SECURITY.md."""

    content = join_sections(
        heading(1, "Security Policy"),
        f"Security matters for {meta.display_name}. This document explains how to report vulnerabilities and how security-related issues are handled.",
        heading(2, "Supported Versions")
        + "\n\n"
        + table(("Version", "Supported"), (("Latest release", "Yes"), ("main branch", "Yes"), ("Older releases", "No"))),
        heading(2, "Reporting a Vulnerability")
        + "\n\n"
        + "Please do not report security vulnerabilities through public GitHub issues. Use GitHub's private vulnerability reporting feature if it is available for this repository. If private reporting is not available, open a public issue asking for a private contact method without sharing technical details."
        + "\n\n"
        + "When reporting, include safe details such as:\n\n"
        + bullet(
            [
                "A short summary of the issue",
                "The affected area of the project",
                "The version or commit tested",
                "Steps to reproduce the issue",
                "The possible impact",
                "Any suggested fix, if you have one",
            ]
        ),
        heading(2, "What Counts as a Security Issue")
        + "\n\n"
        + bullet(
            [
                "Unexpected reading or writing of files outside the target project",
                "Path traversal problems",
                "Unsafe handling of generated output paths",
                "Accidental exposure of secrets in generated documentation",
                "Command execution that the user did not explicitly request",
                "Dependency behavior that creates a clear security risk",
            ]
        ),
        heading(2, "Security Expectations")
        + "\n\n"
        + bullet(
            [
                "Do not expose secrets, tokens, private keys, or passwords",
                "Do not execute untrusted project code during normal documentation generation",
                "Do not upload repository contents to external services",
                "Write files only where the user requested",
                "Fail safely with clear error messages",
                "Keep dependencies minimal and maintained",
            ]
        ),
        heading(2, "Sensitive Information")
        + "\n\n"
        + "Never include real credentials in issues, pull requests, examples, tests, or generated documentation. If sensitive data is accidentally committed or posted, remove it immediately and rotate the affected secret.",
        heading(2, "Responsible Disclosure")
        + "\n\n"
        + numbered(
            [
                "Report the issue privately.",
                "Allow reasonable time for investigation and fixes.",
                "Help verify the fix if possible.",
                "Avoid publishing exploit details before a fix is available.",
            ]
        ),
        heading(2, "Thank You")
        + "\n\n"
        + "Thank you for helping keep this project safe and trustworthy.",
    )
    return GeneratedDocument(DocumentKind.SECURITY, Path("SECURITY.md"), ensure_trailing_newline(content))


def build_code_of_conduct(meta: ProjectMetadata, options: GeneratorOptions) -> GeneratedDocument:
    """Build CODE_OF_CONDUCT.md."""

    content = join_sections(
        heading(1, "Code of Conduct"),
        f"{meta.display_name} welcomes respectful and constructive participation from everyone.",
        heading(2, "Our Standards")
        + "\n\n"
        + bullet(
            [
                "Use welcoming and inclusive language",
                "Respect different viewpoints and experience levels",
                "Give and receive feedback constructively",
                "Focus on what is best for the project and its users",
                "Show patience with new contributors",
            ]
        ),
        heading(2, "Unacceptable Behavior")
        + "\n\n"
        + bullet(
            [
                "Harassment, insults, or personal attacks",
                "Discriminatory language or behavior",
                "Publishing private information without permission",
                "Spam or repeated off-topic comments",
                "Any behavior that makes the project unsafe or unwelcoming",
            ]
        ),
        heading(2, "Enforcement")
        + "\n\n"
        + "Maintainers may remove comments, close issues, block users, or take other reasonable action when behavior harms the project or community.",
        heading(2, "Scope")
        + "\n\n"
        + "This code of conduct applies to project spaces such as issues, pull requests, discussions, and other community interactions connected to the repository.",
    )
    return GeneratedDocument(DocumentKind.CODE_OF_CONDUCT, Path("CODE_OF_CONDUCT.md"), ensure_trailing_newline(content))


def build_bug_report(meta: ProjectMetadata, options: GeneratorOptions) -> GeneratedDocument:
    """Build a GitHub bug report issue template."""

    content = """---
name: Bug report
about: Report something that is not working correctly
title: "Bug: "
labels: bug
assignees: ""
---

## Description

Describe the bug clearly.

## Steps to Reproduce

1. 
2. 
3. 

## Expected Behavior

Describe what you expected to happen.

## Actual Behavior

Describe what actually happened.

## Environment

- OS:
- Python version:
- Project version or commit:

## Additional Context

Add any extra details, screenshots, or command output that may help.
"""
    return GeneratedDocument(
        DocumentKind.BUG_REPORT,
        Path(".github/ISSUE_TEMPLATE/bug_report.md"),
        ensure_trailing_newline(content),
    )


def build_feature_request(meta: ProjectMetadata, options: GeneratorOptions) -> GeneratedDocument:
    """Build a GitHub feature request issue template."""

    content = """---
name: Feature request
about: Suggest a useful improvement
title: "Feature: "
labels: enhancement
assignees: ""
---

## Problem

Describe the problem or limitation this feature would solve.

## Proposed Solution

Describe the solution you would like to see.

## Alternatives Considered

Mention any other approaches you considered.

## Additional Context

Add examples, screenshots, links, or extra details if helpful.
"""
    return GeneratedDocument(
        DocumentKind.FEATURE_REQUEST,
        Path(".github/ISSUE_TEMPLATE/feature_request.md"),
        ensure_trailing_newline(content),
    )


def build_pull_request_template(meta: ProjectMetadata, options: GeneratorOptions) -> GeneratedDocument:
    """Build a GitHub pull request template."""

    content = """## Summary

Describe what this pull request changes.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactor
- [ ] Test update
- [ ] Other

## Checklist

- [ ] I tested my changes locally
- [ ] I updated documentation when needed
- [ ] I added or updated tests when needed
- [ ] I kept the change focused and readable
- [ ] I did not commit secrets, cache files, or build outputs

## Notes

Add any extra context for reviewers.
"""
    return GeneratedDocument(
        DocumentKind.PULL_REQUEST,
        Path(".github/pull_request_template.md"),
        ensure_trailing_newline(content),
    )


def build_documents(meta: ProjectMetadata, options: GeneratorOptions) -> list[GeneratedDocument]:
    """Build the full default documentation set."""

    docs = [build_readme(meta, options), build_contributing(meta, options), build_security(meta, options)]
    if options.include_code_of_conduct:
        docs.append(build_code_of_conduct(meta, options))
    if options.include_issue_templates:
        docs.extend([build_bug_report(meta, options), build_feature_request(meta, options)])
    if options.include_pull_request_template:
        docs.append(build_pull_request_template(meta, options))
    return docs


def _readme_hero(meta: ProjectMetadata, badges: str) -> str:
    return f"""<div align=\"center\">

# {meta.display_name}

**{meta.description}**

<br>

{badges}

</div>"""


def _badges(meta: ProjectMetadata) -> str:
    items = [badge("License", meta.license_name, "green")]
    if meta.project_type == ProjectType.PYTHON:
        items.insert(0, badge("Python", (meta.python_version or "3.9+").replace(">=", ""), "3776AB", "python"))
    elif meta.project_type == ProjectType.NODE:
        items.insert(0, badge("Node", "Project", "339933", "node.js"))
    elif meta.project_type == ProjectType.RUST:
        items.insert(0, badge("Rust", "Project", "000000", "rust"))
    elif meta.project_type == ProjectType.GO:
        items.insert(0, badge("Go", "Project", "00ADD8", "go"))
    if meta.package_manager:
        items.append(badge("Package Manager", meta.package_manager, "blue"))
    return "\n".join(items)


def _overview(meta: ProjectMetadata) -> str:
    return f"""## Overview

{meta.display_name} is a {meta.project_type.value} project built with a focus on clean structure, practical usage, and maintainable documentation.

This repository is organized so developers can understand the project quickly, install it locally, run it, test it, and contribute without guessing how the codebase works."""


def _features(meta: ProjectMetadata, style: ReadmeStyle) -> str:
    base = [
        "Clear project structure",
        "Professional documentation layout",
        "Simple setup and usage flow",
    ]
    if meta.project_type == ProjectType.PYTHON:
        base.extend(["Python package-friendly layout", "Test-ready development workflow"])
    if meta.has_ci:
        base.append("Continuous integration support")
    if meta.has_docs:
        base.append("Dedicated documentation folder")
    if style == ReadmeStyle.DETAILED:
        base.extend(["Contributor-friendly project files", "Room for future extension"])
    return heading(2, "Features") + "\n\n" + bullet(base)


def _installation(meta: ProjectMetadata) -> str:
    if meta.project_type == ProjectType.PYTHON:
        body = fenced(
            "bash",
            f"git clone {meta.repository_url}.git\ncd {meta.name}\npython -m pip install -e .",
        )
        if meta.dependencies.development:
            body += "\n\nFor development:\n\n" + fenced("bash", "python -m pip install -e \".[dev]\"")
        return heading(2, "Installation") + "\n\n" + body
    if meta.project_type == ProjectType.NODE:
        command = "npm install"
        if meta.package_manager == "pnpm":
            command = "pnpm install"
        elif meta.package_manager == "Yarn":
            command = "yarn install"
        return heading(2, "Installation") + "\n\n" + fenced(
            "bash", f"git clone {meta.repository_url}.git\ncd {meta.name}\n{command}"
        )
    if meta.project_type == ProjectType.RUST:
        return heading(2, "Installation") + "\n\n" + fenced(
            "bash", f"git clone {meta.repository_url}.git\ncd {meta.name}\ncargo build"
        )
    if meta.project_type == ProjectType.GO:
        return heading(2, "Installation") + "\n\n" + fenced(
            "bash", f"git clone {meta.repository_url}.git\ncd {meta.name}\ngo mod download"
        )
    return heading(2, "Installation") + "\n\n" + fenced(
        "bash", f"git clone {meta.repository_url}.git\ncd {meta.name}"
    )


def _usage(meta: ProjectMetadata) -> str:
    if meta.entry_points:
        examples = "\n".join(f"{entry} --help" for entry in meta.entry_points[:3])
        return heading(2, "Usage") + "\n\n" + "Run the CLI help command to see available options:\n\n" + fenced("bash", examples)
    if meta.project_type == ProjectType.PYTHON:
        package = meta.package_name or meta.slug.replace("-", "_")
        return heading(2, "Usage") + "\n\n" + fenced("bash", f"python -m {package}")
    if meta.project_type == ProjectType.NODE:
        return heading(2, "Usage") + "\n\n" + fenced("bash", "npm run start")
    if meta.project_type == ProjectType.RUST:
        return heading(2, "Usage") + "\n\n" + fenced("bash", "cargo run")
    if meta.project_type == ProjectType.GO:
        return heading(2, "Usage") + "\n\n" + fenced("bash", "go run .")
    return heading(2, "Usage") + "\n\n" + "Use the project files in this repository as the main starting point."


def _commands(meta: ProjectMetadata) -> str:
    if not meta.entry_points:
        return ""
    rows = tuple((f"`{entry} --help`", "Show available command-line options") for entry in meta.entry_points)
    return heading(2, "Commands") + "\n\n" + table(("Command", "Description"), rows)


def _configuration(meta: ProjectMetadata) -> str:
    files = [file for file in meta.detected_files if file.endswith((".yaml", ".yml", ".toml", ".json", ".ini"))]
    if not files:
        return heading(2, "Configuration") + "\n\n" + "This project can be extended with configuration files as needed."
    return heading(2, "Configuration") + "\n\n" + "Important configuration files detected:\n\n" + bullet(
        f"`{file}`" for file in files[:8]
    )


def _project_structure(meta: ProjectMetadata) -> str:
    tree = _tree_from_files(meta.detected_files)
    return heading(2, "Project Structure") + "\n\n" + fenced("text", tree)


def _tree_from_files(files: tuple[str, ...]) -> str:
    if not files:
        return "."
    selected = [file for file in files if not file.startswith((".git/", ".venv/"))][:28]
    roots: dict[str, list[str]] = {}
    for file in selected:
        parts = file.split("/")
        if len(parts) == 1:
            roots.setdefault("", []).append(parts[0])
        else:
            roots.setdefault(parts[0], []).append("/".join(parts[1:]))
    lines = ["."]
    for root, children in sorted(roots.items(), key=lambda item: item[0]):
        if root == "":
            for child in sorted(children):
                lines.append(f"├── {child}")
            continue
        lines.append(f"├── {root}/")
        for child in sorted(children[:6]):
            lines.append(f"│   ├── {child}")
    return "\n".join(lines)


def _built_with(meta: ProjectMetadata) -> str:
    rows: list[tuple[str, str]] = []
    if meta.project_type == ProjectType.PYTHON:
        rows.append(("Python", "Main programming language"))
        if meta.package_manager:
            rows.append((meta.package_manager, "Package installation and dependency workflow"))
    elif meta.project_type == ProjectType.NODE:
        rows.append(("JavaScript / TypeScript", "Main runtime ecosystem"))
        rows.append((meta.package_manager or "npm", "Package management"))
    elif meta.project_type == ProjectType.RUST:
        rows.append(("Rust", "Main programming language"))
        rows.append(("Cargo", "Build and package manager"))
    elif meta.project_type == ProjectType.GO:
        rows.append(("Go", "Main programming language"))
        rows.append(("Go modules", "Dependency management"))
    else:
        rows.append(("Markdown", "Documentation"))
    if meta.dependencies.runtime:
        rows.append(("Runtime dependencies", ", ".join(meta.dependencies.runtime[:5])))
    return heading(2, "Built With") + "\n\n" + table(("Tool", "Purpose"), tuple(rows))


def _development(meta: ProjectMetadata) -> str:
    return heading(2, "Development") + "\n\n" + fenced("bash", _quality_commands(meta))


def _quality_commands(meta: ProjectMetadata) -> str:
    if meta.project_type == ProjectType.PYTHON:
        commands = ["pytest"] if meta.has_tests else ["python -m compileall ."]
        if "ruff" in " ".join(meta.dependencies.development).lower() or "pyproject.toml" in meta.detected_files:
            commands.append("ruff check .")
        return "\n".join(commands)
    if meta.project_type == ProjectType.NODE:
        return "npm test"
    if meta.project_type == ProjectType.RUST:
        return "cargo test\ncargo clippy"
    if meta.project_type == ProjectType.GO:
        return "go test ./..."
    return "# Add project-specific development commands here"


def _quality_notes(meta: ProjectMetadata) -> str:
    notes = [
        "Keep generated and cache files out of the repository.",
        "Prefer small, focused pull requests.",
        "Update documentation when user-facing behavior changes.",
    ]
    if not meta.has_tests:
        notes.append("Add tests as the project grows.")
    if not meta.has_ci:
        notes.append("Add a CI workflow to run checks automatically.")
    return heading(2, "Quality Notes") + "\n\n" + bullet(notes)


def _faq(meta: ProjectMetadata) -> str:
    return heading(2, "FAQ") + "\n\n" + "**Who is this project for?**\n\nDevelopers who want a clean and practical project they can understand, run, and improve.\n\n**Is this project production-ready?**\n\nThe repository is designed to be a strong base and should be reviewed for your specific use case before production use."


def _roadmap(meta: ProjectMetadata) -> str:
    return heading(2, "Roadmap") + "\n\n" + bullet(
        [
            "Improve documentation examples",
            "Add more tests around important behavior",
            "Refine error handling and edge cases",
            "Keep the project lightweight and maintainable",
        ]
    )


def _contributing_short() -> str:
    return heading(2, "Contributing") + "\n\n" + "Contributions are welcome. Please open an issue or pull request with a clear explanation of your change."


def _author(meta: ProjectMetadata, options: GeneratorOptions) -> str:
    author = options.author or meta.author
    return heading(2, "Author") + "\n\n" + f"Created by **{author}**."


def _license(meta: ProjectMetadata) -> str:
    return heading(2, "License") + "\n\n" + f"This project is licensed under the {meta.license_name} License."


def _project_run_example(meta: ProjectMetadata) -> str:
    if meta.entry_points:
        return fenced("bash", f"{meta.entry_points[0]} --help")
    if meta.project_type == ProjectType.PYTHON:
        return fenced("bash", "python -m pytest")
    if meta.project_type == ProjectType.NODE:
        return fenced("bash", "npm run start")
    return "Use the commands documented in the README to run the project locally."
