"""Configuration loading for ReadmeKit."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .exceptions import ConfigError
from .models import GeneratorOptions, ReadmeStyle
from .utils import normalize_license

CONFIG_FILENAMES = (".readmekit.yaml", ".readmekit.yml", "readmekit.yaml", "readmekit.yml")


def load_config(root: Path) -> dict[str, Any]:
    """Load a ReadmeKit config dictionary from a repository root."""

    for filename in CONFIG_FILENAMES:
        path = root / filename
        if not path.exists():
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise ConfigError(f"Could not read config file {path}: {exc}") from exc
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise ConfigError(f"Config file {path} must contain a YAML object.")
        return dict(data)
    return {}


def options_from_config(config: dict[str, Any], base: GeneratorOptions | None = None) -> GeneratorOptions:
    """Create generation options from a config dictionary."""

    current = base or GeneratorOptions()
    style_value = str(config.get("style", current.style.value)).strip().lower()
    try:
        style = ReadmeStyle(style_value)
    except ValueError as exc:
        valid = ", ".join(item.value for item in ReadmeStyle)
        raise ConfigError(f"Invalid README style '{style_value}'. Valid styles: {valid}") from exc

    return GeneratorOptions(
        style=style,
        author=str(config.get("author", current.author)).strip() or current.author,
        license_name=normalize_license(str(config.get("license", current.license_name))),
        force=bool(config.get("force", current.force)),
        dry_run=bool(config.get("dry_run", current.dry_run)),
        include_code_of_conduct=bool(
            config.get("include_code_of_conduct", current.include_code_of_conduct)
        ),
        include_issue_templates=bool(
            config.get("include_issue_templates", current.include_issue_templates)
        ),
        include_pull_request_template=bool(
            config.get("include_pull_request_template", current.include_pull_request_template)
        ),
        values=dict(config.get("values", current.values) or {}),
    )


def default_config_text() -> str:
    """Return a complete default configuration file."""

    return """# ReadmeKit configuration
# This file controls how documentation is generated for this repository.

author: Nitish Vimal
license: MIT
style: professional

include_code_of_conduct: true
include_issue_templates: true
include_pull_request_template: true

# Keep false unless you intentionally want existing files replaced.
force: false

# Custom values can be used by future generators and integrations.
values: {}
"""
