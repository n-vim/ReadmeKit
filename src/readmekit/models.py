"""Data models for detected repositories and generated documents."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class ProjectType(str, Enum):
    """Supported project type guesses."""

    PYTHON = "python"
    NODE = "node"
    RUST = "rust"
    GO = "go"
    GENERAL = "general"


class DocumentKind(str, Enum):
    """Documentation files ReadmeKit can create."""

    README = "readme"
    CONTRIBUTING = "contributing"
    SECURITY = "security"
    CODE_OF_CONDUCT = "code_of_conduct"
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    PULL_REQUEST = "pull_request"


class ReadmeStyle(str, Enum):
    """Supported README writing styles."""

    MINIMAL = "minimal"
    PROFESSIONAL = "professional"
    DETAILED = "detailed"


@dataclass(frozen=True)
class DependencyInfo:
    """Dependencies detected from a project."""

    runtime: tuple[str, ...] = ()
    development: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProjectMetadata:
    """Normalized information about a repository."""

    root: Path
    name: str
    slug: str
    description: str
    project_type: ProjectType
    package_name: str | None = None
    author: str = "Nitish Vimal"
    license_name: str = "MIT"
    python_version: str | None = None
    package_manager: str | None = None
    entry_points: tuple[str, ...] = ()
    dependencies: DependencyInfo = field(default_factory=DependencyInfo)
    has_tests: bool = False
    has_ci: bool = False
    has_docs: bool = False
    detected_files: tuple[str, ...] = ()

    @property
    def display_name(self) -> str:
        """Return a human-friendly project name."""

        source = self.package_name or self.name
        return source.replace("-", " ").replace("_", " ").strip().title()

    @property
    def repository_url(self) -> str:
        """Return the public GitHub URL for the project if it follows the n-vim namespace."""

        return f"https://github.com/n-vim/{self.name}"


@dataclass(frozen=True)
class GeneratedDocument:
    """A generated documentation artifact."""

    kind: DocumentKind
    relative_path: Path
    content: str


@dataclass(frozen=True)
class WriteResult:
    """Result from writing one generated artifact to disk."""

    relative_path: Path
    written: bool
    skipped: bool
    reason: str = ""


@dataclass(frozen=True)
class GeneratorOptions:
    """Options controlling documentation generation."""

    style: ReadmeStyle = ReadmeStyle.PROFESSIONAL
    author: str = "Nitish Vimal"
    license_name: str = "MIT"
    force: bool = False
    dry_run: bool = False
    include_code_of_conduct: bool = True
    include_issue_templates: bool = True
    include_pull_request_template: bool = True
    values: dict[str, Any] = field(default_factory=dict)
