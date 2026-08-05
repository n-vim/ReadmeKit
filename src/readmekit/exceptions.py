"""Custom exceptions used by ReadmeKit."""

from __future__ import annotations


class ReadmeKitError(Exception):
    """Base error for all handled ReadmeKit failures."""


class ProjectNotFoundError(ReadmeKitError):
    """Raised when the requested project path does not exist."""


class UnsafeWriteError(ReadmeKitError):
    """Raised when a write operation would overwrite a file without permission."""


class ConfigError(ReadmeKitError):
    """Raised when configuration cannot be parsed or validated."""
