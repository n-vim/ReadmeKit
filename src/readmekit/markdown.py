"""Markdown helpers for generated documentation."""

from __future__ import annotations

from collections.abc import Iterable

from .utils import markdown_escape


def heading(level: int, text: str) -> str:
    """Create a Markdown heading."""

    return f"{'#' * level} {text}"


def bullet(items: Iterable[str]) -> str:
    """Create a Markdown bullet list."""

    values = [item.strip() for item in items if item.strip()]
    return "\n".join(f"- {item}" for item in values)


def numbered(items: Iterable[str]) -> str:
    """Create a Markdown numbered list."""

    values = [item.strip() for item in items if item.strip()]
    return "\n".join(f"{index}. {item}" for index, item in enumerate(values, start=1))


def table(headers: tuple[str, ...], rows: Iterable[tuple[str, ...]]) -> str:
    """Create a GitHub-flavored Markdown table."""

    header = "| " + " | ".join(markdown_escape(item) for item in headers) + " |"
    divider = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(markdown_escape(value) for value in row) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def fenced(language: str, content: str) -> str:
    """Create a fenced Markdown block."""

    return f"```{language}\n{content.rstrip()}\n```"


def badge(label: str, message: str, color: str, logo: str | None = None) -> str:
    """Create a shields.io badge."""

    safe_label = label.replace("-", "--").replace(" ", "%20")
    safe_message = message.replace("-", "--").replace(" ", "%20")
    url = f"https://img.shields.io/badge/{safe_label}-{safe_message}-{color}?style=flat"
    if logo:
        url += f"&logo={logo}&logoColor=white"
    return f"![{label}: {message}]({url})"


def join_sections(*sections: str) -> str:
    """Join non-empty Markdown sections with a standard separator."""

    return "\n\n---\n\n".join(section.strip() for section in sections if section.strip())
