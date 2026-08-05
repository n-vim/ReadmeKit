"""Utility helpers used throughout ReadmeKit."""

from __future__ import annotations

import re
from pathlib import Path

_WORD_RE = re.compile(r"[A-Za-z0-9]+")


def slugify(value: str) -> str:
    """Create a safe repository slug from a string."""

    words = _WORD_RE.findall(value.lower())
    return "-".join(words) if words else "project"


def package_slug(value: str) -> str:
    """Create a safe Python package name from a string."""

    slug = slugify(value).replace("-", "_")
    if slug and slug[0].isdigit():
        return f"project_{slug}"
    return slug or "project"


def titleize(value: str) -> str:
    """Turn a slug-like value into a readable title."""

    return " ".join(word.capitalize() for word in re.split(r"[-_\s]+", value) if word)


def relative_file_list(root: Path, max_files: int = 200) -> tuple[str, ...]:
    """Return a small, stable list of files relative to a repository root."""

    ignored_parts = {
        ".git",
        ".venv",
        "venv",
        "env",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "node_modules",
        "dist",
        "build",
    }
    files: list[str] = []
    for path in sorted(root.rglob("*")):
        if len(files) >= max_files:
            break
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        if any(part in ignored_parts for part in rel.parts):
            continue
        files.append(rel.as_posix())
    return tuple(files)


def safe_read_text(path: Path) -> str | None:
    """Read a text file safely, returning None when it cannot be read."""

    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def normalize_license(value: str | None) -> str:
    """Normalize a license value into a clean display name."""

    if not value:
        return "MIT"
    text = value.strip()
    if text.upper() == "MIT":
        return "MIT"
    if text.lower() in {"apache-2.0", "apache 2.0"}:
        return "Apache-2.0"
    if text.lower() in {"bsd-3-clause", "bsd 3-clause"}:
        return "BSD-3-Clause"
    return text


def markdown_escape(value: str) -> str:
    """Escape table-sensitive characters for Markdown tables."""

    return value.replace("|", "\\|").strip()


def ensure_trailing_newline(value: str) -> str:
    """Ensure generated files end with exactly one newline."""

    return value.rstrip() + "\n"
