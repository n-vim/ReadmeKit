"""Generation and file writing services."""

from __future__ import annotations

from pathlib import Path

from .exceptions import UnsafeWriteError
from .models import DocumentKind, GeneratedDocument, GeneratorOptions, ProjectMetadata, WriteResult
from .templates import (
    build_bug_report,
    build_code_of_conduct,
    build_contributing,
    build_documents,
    build_feature_request,
    build_pull_request_template,
    build_readme,
    build_security,
)
from .utils import ensure_trailing_newline


def generate_document(
    kind: DocumentKind, meta: ProjectMetadata, options: GeneratorOptions
) -> GeneratedDocument:
    """Generate a single documentation file."""

    builders = {
        DocumentKind.README: build_readme,
        DocumentKind.CONTRIBUTING: build_contributing,
        DocumentKind.SECURITY: build_security,
        DocumentKind.CODE_OF_CONDUCT: build_code_of_conduct,
        DocumentKind.BUG_REPORT: build_bug_report,
        DocumentKind.FEATURE_REQUEST: build_feature_request,
        DocumentKind.PULL_REQUEST: build_pull_request_template,
    }
    return builders[kind](meta, options)


def generate_all(meta: ProjectMetadata, options: GeneratorOptions) -> list[GeneratedDocument]:
    """Generate the default project documentation set."""

    return build_documents(meta, options)


def write_document(root: Path, document: GeneratedDocument, force: bool = False, dry_run: bool = False) -> WriteResult:
    """Write one document to disk, safely skipping existing files unless forced."""

    target = (root / document.relative_path).resolve()
    root_resolved = root.resolve()
    if root_resolved not in target.parents and target != root_resolved:
        raise UnsafeWriteError(f"Refusing to write outside repository root: {document.relative_path}")

    if target.exists() and not force:
        return WriteResult(
            relative_path=document.relative_path,
            written=False,
            skipped=True,
            reason="already exists",
        )

    if dry_run:
        return WriteResult(
            relative_path=document.relative_path,
            written=False,
            skipped=False,
            reason="dry run",
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(ensure_trailing_newline(document.content), encoding="utf-8")
    return WriteResult(relative_path=document.relative_path, written=True, skipped=False)


def write_documents(
    root: Path, documents: list[GeneratedDocument], force: bool = False, dry_run: bool = False
) -> list[WriteResult]:
    """Write multiple documents and return per-file results."""

    return [write_document(root, document, force=force, dry_run=dry_run) for document in documents]
