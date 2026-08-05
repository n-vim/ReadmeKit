"""Repository detection logic."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

from .exceptions import ProjectNotFoundError
from .models import DependencyInfo, ProjectMetadata, ProjectType
from .utils import normalize_license, package_slug, relative_file_list, safe_read_text, slugify, titleize


def detect_project(path: Path, author: str = "Nitish Vimal", license_name: str = "MIT") -> ProjectMetadata:
    """Detect project metadata from a repository folder."""

    root = path.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ProjectNotFoundError(f"Project path does not exist or is not a directory: {path}")

    files = relative_file_list(root)
    file_set = set(files)
    name = root.name
    slug = slugify(name)
    project_type = _detect_type(root, file_set)

    pyproject = _read_pyproject(root)
    package_json = _read_package_json_like(root)

    description = _description_from_sources(root, pyproject, package_json) or _default_description(name, project_type)
    detected_author = _author_from_sources(pyproject, package_json) or author
    detected_license = _license_from_sources(pyproject, package_json, root) or license_name
    detected_package = _package_name_from_sources(name, pyproject, package_json, project_type)
    python_version = _python_version_from_pyproject(pyproject) if pyproject else None
    package_manager = _detect_package_manager(file_set, project_type)
    dependencies = _detect_dependencies(root, pyproject, package_json, project_type)
    entry_points = _detect_entry_points(pyproject, package_json, project_type)

    return ProjectMetadata(
        root=root,
        name=name,
        slug=slug,
        description=description,
        project_type=project_type,
        package_name=detected_package,
        author=detected_author,
        license_name=normalize_license(detected_license),
        python_version=python_version,
        package_manager=package_manager,
        entry_points=entry_points,
        dependencies=dependencies,
        has_tests=_has_tests(root, file_set),
        has_ci=any(file.startswith(".github/workflows/") for file in files),
        has_docs=any(file.startswith("docs/") for file in files),
        detected_files=files,
    )


def _detect_type(root: Path, files: set[str]) -> ProjectType:
    if "pyproject.toml" in files or "requirements.txt" in files or any(
        path.endswith(".py") for path in files
    ):
        return ProjectType.PYTHON
    if "package.json" in files or "pnpm-lock.yaml" in files or "package-lock.json" in files:
        return ProjectType.NODE
    if "Cargo.toml" in files:
        return ProjectType.RUST
    if "go.mod" in files:
        return ProjectType.GO
    if (root / "src").exists():
        return ProjectType.GENERAL
    return ProjectType.GENERAL


def _read_pyproject(root: Path) -> dict[str, Any] | None:
    path = root / "pyproject.toml"
    if not path.exists():
        return None
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return None


def _read_package_json_like(root: Path) -> dict[str, Any] | None:
    path = root / "package.json"
    if not path.exists():
        return None
    text = safe_read_text(path)
    if text is None:
        return None
    # Small, dependency-free extraction. This is enough for docs metadata without importing json errors everywhere.
    import json

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if isinstance(data, dict):
        return data
    return None


def _description_from_sources(
    root: Path, pyproject: dict[str, Any] | None, package_json: dict[str, Any] | None
) -> str | None:
    if pyproject:
        project = pyproject.get("project", {})
        if isinstance(project, dict) and isinstance(project.get("description"), str):
            return project["description"].strip()
    if package_json and isinstance(package_json.get("description"), str):
        return package_json["description"].strip()
    readme = safe_read_text(root / "README.md") or safe_read_text(root / "readme.md")
    if readme:
        for line in readme.splitlines():
            clean = line.strip().strip("# ")
            if clean and not clean.startswith("!") and len(clean) > 8:
                return clean[:160]
    return None


def _default_description(name: str, project_type: ProjectType) -> str:
    readable = titleize(name)
    if project_type == ProjectType.PYTHON:
        return f"{readable} is a Python project with a clean, maintainable structure."
    if project_type == ProjectType.NODE:
        return f"{readable} is a JavaScript project designed for practical development workflows."
    if project_type == ProjectType.RUST:
        return f"{readable} is a Rust project focused on reliable and maintainable software."
    if project_type == ProjectType.GO:
        return f"{readable} is a Go project focused on simple and efficient development."
    return f"{readable} is a software project with clean documentation and practical structure."


def _author_from_sources(
    pyproject: dict[str, Any] | None, package_json: dict[str, Any] | None
) -> str | None:
    if pyproject:
        project = pyproject.get("project", {})
        if isinstance(project, dict):
            authors = project.get("authors")
            if isinstance(authors, list) and authors:
                first = authors[0]
                if isinstance(first, dict) and isinstance(first.get("name"), str):
                    return first["name"].strip()
                if isinstance(first, str):
                    return first.strip()
    if package_json:
        author = package_json.get("author")
        if isinstance(author, str):
            return author.strip()
        if isinstance(author, dict) and isinstance(author.get("name"), str):
            return author["name"].strip()
    return None


def _license_from_sources(
    pyproject: dict[str, Any] | None, package_json: dict[str, Any] | None, root: Path
) -> str | None:
    if pyproject:
        project = pyproject.get("project", {})
        if isinstance(project, dict):
            license_value = project.get("license")
            if isinstance(license_value, str):
                return license_value
            if isinstance(license_value, dict):
                text = license_value.get("text")
                if isinstance(text, str):
                    return text
    if package_json and isinstance(package_json.get("license"), str):
        return package_json["license"]
    license_file = safe_read_text(root / "LICENSE") or safe_read_text(root / "LICENSE.md")
    if license_file:
        first_line = license_file.splitlines()[0] if license_file.splitlines() else ""
        if "MIT" in first_line.upper() or "MIT" in license_file[:120].upper():
            return "MIT"
        return first_line.strip() or None
    return None


def _package_name_from_sources(
    name: str,
    pyproject: dict[str, Any] | None,
    package_json: dict[str, Any] | None,
    project_type: ProjectType,
) -> str | None:
    if pyproject:
        project = pyproject.get("project", {})
        if isinstance(project, dict) and isinstance(project.get("name"), str):
            return project["name"].strip()
    if package_json and isinstance(package_json.get("name"), str):
        return package_json["name"].strip()
    if project_type == ProjectType.PYTHON:
        return package_slug(name)
    return slugify(name)


def _python_version_from_pyproject(pyproject: dict[str, Any] | None) -> str | None:
    if not pyproject:
        return None
    project = pyproject.get("project", {})
    if isinstance(project, dict) and isinstance(project.get("requires-python"), str):
        return project["requires-python"].strip()
    return None


def _detect_package_manager(files: set[str], project_type: ProjectType) -> str | None:
    if project_type == ProjectType.PYTHON:
        if "uv.lock" in files:
            return "uv"
        if "poetry.lock" in files:
            return "Poetry"
        if "pyproject.toml" in files:
            return "pip"
        if "requirements.txt" in files:
            return "pip"
    if project_type == ProjectType.NODE:
        if "pnpm-lock.yaml" in files:
            return "pnpm"
        if "yarn.lock" in files:
            return "Yarn"
        if "package-lock.json" in files:
            return "npm"
        return "npm"
    if project_type == ProjectType.RUST:
        return "Cargo"
    if project_type == ProjectType.GO:
        return "Go modules"
    return None


def _detect_dependencies(
    root: Path,
    pyproject: dict[str, Any] | None,
    package_json: dict[str, Any] | None,
    project_type: ProjectType,
) -> DependencyInfo:
    runtime: list[str] = []
    development: list[str] = []
    if project_type == ProjectType.PYTHON:
        if pyproject:
            project = pyproject.get("project", {})
            if isinstance(project, dict):
                deps = project.get("dependencies", [])
                if isinstance(deps, list):
                    runtime.extend(str(item) for item in deps if isinstance(item, str))
                optional = project.get("optional-dependencies", {})
                if isinstance(optional, dict):
                    for group_name in ("dev", "test", "docs"):
                        group = optional.get(group_name, [])
                        if isinstance(group, list):
                            development.extend(str(item) for item in group if isinstance(item, str))
        req = safe_read_text(root / "requirements.txt")
        if req:
            runtime.extend(_parse_requirements(req))
        dev_req = safe_read_text(root / "requirements-dev.txt")
        if dev_req:
            development.extend(_parse_requirements(dev_req))
    if project_type == ProjectType.NODE and package_json:
        deps = package_json.get("dependencies", {})
        dev_deps = package_json.get("devDependencies", {})
        if isinstance(deps, dict):
            runtime.extend(str(item) for item in deps.keys())
        if isinstance(dev_deps, dict):
            development.extend(str(item) for item in dev_deps.keys())
    return DependencyInfo(runtime=tuple(_unique(runtime)), development=tuple(_unique(development)))


def _parse_requirements(text: str) -> list[str]:
    deps: list[str] = []
    for line in text.splitlines():
        clean = line.strip()
        if not clean or clean.startswith("#") or clean.startswith("-"):
            continue
        deps.append(re.split(r"[<>=~!;\s]", clean, maxsplit=1)[0])
    return deps


def _detect_entry_points(
    pyproject: dict[str, Any] | None,
    package_json: dict[str, Any] | None,
    project_type: ProjectType,
) -> tuple[str, ...]:
    entries: list[str] = []
    if project_type == ProjectType.PYTHON and pyproject:
        project = pyproject.get("project", {})
        if isinstance(project, dict):
            scripts = project.get("scripts", {})
            if isinstance(scripts, dict):
                entries.extend(str(key) for key in scripts.keys())
    if project_type == ProjectType.NODE and package_json:
        bin_value = package_json.get("bin")
        if isinstance(bin_value, str):
            name = package_json.get("name")
            entries.append(str(name or "cli"))
        if isinstance(bin_value, dict):
            entries.extend(str(key) for key in bin_value.keys())
    return tuple(_unique(entries))


def _has_tests(root: Path, files: set[str]) -> bool:
    if any(file.startswith("tests/") for file in files):
        return True
    patterns = ("test_*.py", "*_test.py", "*.test.ts", "*.test.js", "*.spec.ts", "*.spec.js")
    return any(root.glob(pattern) for pattern in patterns)


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean = value.strip()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        result.append(clean)
    return result
