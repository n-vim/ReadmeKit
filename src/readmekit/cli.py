"""Command-line interface for ReadmeKit."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __app_name__, __version__
from .config import default_config_text, load_config, options_from_config
from .detector import detect_project
from .exceptions import ConfigError, ProjectNotFoundError, ReadmeKitError, UnsafeWriteError
from .generator import generate_all, generate_document, write_document, write_documents
from .models import DocumentKind, GeneratorOptions, ReadmeStyle
from .utils import ensure_trailing_newline

app = typer.Typer(
    name="readmekit",
    help="Generate professional README and GitHub documentation for repositories.",
    no_args_is_help=True,
)
console = Console()

PathArg = Annotated[Path, typer.Argument(help="Repository path to inspect or write documentation into.")]
StyleOpt = Annotated[
    ReadmeStyle,
    typer.Option("--style", "-s", help="README style to generate."),
]
AuthorOpt = Annotated[str, typer.Option("--author", help="Author name used in generated docs.")]
LicenseOpt = Annotated[str, typer.Option("--license", help="License name used in generated docs.")]
ForceOpt = Annotated[bool, typer.Option("--force", "-f", help="Overwrite existing files.")]
DryRunOpt = Annotated[bool, typer.Option("--dry-run", help="Preview writes without creating files.")]
PrintOpt = Annotated[bool, typer.Option("--print", "-p", help="Print generated document instead of writing it.")]


@app.callback()
def main(
    version: Annotated[bool, typer.Option("--version", help="Show the installed ReadmeKit version.")] = False,
) -> None:
    """ReadmeKit command entry point."""

    if version:
        console.print(f"{__app_name__} {__version__}")
        raise typer.Exit()


@app.command()
def inspect(path: PathArg = Path(".")) -> None:
    """Inspect a repository and show detected metadata."""

    try:
        meta = detect_project(path)
    except ReadmeKitError as exc:
        _fail(str(exc))

    table = Table(title=f"{meta.display_name} metadata")
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("Name", meta.name)
    table.add_row("Type", meta.project_type.value)
    table.add_row("Description", meta.description)
    table.add_row("Author", meta.author)
    table.add_row("License", meta.license_name)
    table.add_row("Package", meta.package_name or "-")
    table.add_row("Package manager", meta.package_manager or "-")
    table.add_row("Entry points", ", ".join(meta.entry_points) or "-")
    table.add_row("Tests detected", "yes" if meta.has_tests else "no")
    table.add_row("CI detected", "yes" if meta.has_ci else "no")
    console.print(table)


@app.command()
def init(
    path: PathArg = Path("."),
    force: ForceOpt = False,
) -> None:
    """Create a default .readmekit.yaml config file."""

    root = path.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        _fail(f"Project path does not exist or is not a directory: {path}")
    target = root / ".readmekit.yaml"
    if target.exists() and not force:
        _fail(".readmekit.yaml already exists. Use --force to replace it.")
    target.write_text(default_config_text(), encoding="utf-8")
    console.print(f"[green]Created[/green] {target.relative_to(root)}")


@app.command("readme")
def readme_command(
    path: PathArg = Path("."),
    style: StyleOpt = ReadmeStyle.PROFESSIONAL,
    author: AuthorOpt = "Nitish Vimal",
    license_name: LicenseOpt = "MIT",
    force: ForceOpt = False,
    dry_run: DryRunOpt = False,
    print_output: PrintOpt = False,
) -> None:
    """Generate README.md."""

    _generate_one(
        DocumentKind.README,
        path,
        style=style,
        author=author,
        license_name=license_name,
        force=force,
        dry_run=dry_run,
        print_output=print_output,
    )


@app.command("contributing")
def contributing_command(
    path: PathArg = Path("."),
    author: AuthorOpt = "Nitish Vimal",
    license_name: LicenseOpt = "MIT",
    force: ForceOpt = False,
    dry_run: DryRunOpt = False,
    print_output: PrintOpt = False,
) -> None:
    """Generate CONTRIBUTING.md."""

    _generate_one(
        DocumentKind.CONTRIBUTING,
        path,
        author=author,
        license_name=license_name,
        force=force,
        dry_run=dry_run,
        print_output=print_output,
    )


@app.command("security")
def security_command(
    path: PathArg = Path("."),
    author: AuthorOpt = "Nitish Vimal",
    license_name: LicenseOpt = "MIT",
    force: ForceOpt = False,
    dry_run: DryRunOpt = False,
    print_output: PrintOpt = False,
) -> None:
    """Generate SECURITY.md."""

    _generate_one(
        DocumentKind.SECURITY,
        path,
        author=author,
        license_name=license_name,
        force=force,
        dry_run=dry_run,
        print_output=print_output,
    )


@app.command("github")
def github_command(
    path: PathArg = Path("."),
    author: AuthorOpt = "Nitish Vimal",
    license_name: LicenseOpt = "MIT",
    force: ForceOpt = False,
    dry_run: DryRunOpt = False,
) -> None:
    """Generate GitHub community files such as issue templates and PR template."""

    try:
        root = path.expanduser().resolve()
        options = _make_options(root, ReadmeStyle.PROFESSIONAL, author, license_name, force, dry_run)
        meta = detect_project(root, author=options.author, license_name=options.license_name)
        docs = [
            generate_document(DocumentKind.CODE_OF_CONDUCT, meta, options),
            generate_document(DocumentKind.BUG_REPORT, meta, options),
            generate_document(DocumentKind.FEATURE_REQUEST, meta, options),
            generate_document(DocumentKind.PULL_REQUEST, meta, options),
        ]
        results = write_documents(root, docs, force=options.force, dry_run=options.dry_run)
    except ReadmeKitError as exc:
        _fail(str(exc))
    _show_results(results)


@app.command("all")
def all_command(
    path: PathArg = Path("."),
    style: StyleOpt = ReadmeStyle.PROFESSIONAL,
    author: AuthorOpt = "Nitish Vimal",
    license_name: LicenseOpt = "MIT",
    force: ForceOpt = False,
    dry_run: DryRunOpt = False,
) -> None:
    """Generate README, community docs, and GitHub templates."""

    try:
        root = path.expanduser().resolve()
        options = _make_options(root, style, author, license_name, force, dry_run)
        meta = detect_project(root, author=options.author, license_name=options.license_name)
        documents = generate_all(meta, options)
        results = write_documents(root, documents, force=options.force, dry_run=options.dry_run)
    except ReadmeKitError as exc:
        _fail(str(exc))
    _show_results(results)


@app.command("preview")
def preview_command(
    path: PathArg = Path("."),
    kind: Annotated[DocumentKind, typer.Option("--kind", "-k", help="Document type to preview.")] = DocumentKind.README,
    style: StyleOpt = ReadmeStyle.PROFESSIONAL,
    author: AuthorOpt = "Nitish Vimal",
    license_name: LicenseOpt = "MIT",
) -> None:
    """Print a generated document without writing it."""

    try:
        root = path.expanduser().resolve()
        options = _make_options(root, style, author, license_name, force=False, dry_run=True)
        meta = detect_project(root, author=options.author, license_name=options.license_name)
        document = generate_document(kind, meta, options)
    except ReadmeKitError as exc:
        _fail(str(exc))
    console.print(document.content)


def _generate_one(
    kind: DocumentKind,
    path: Path,
    *,
    style: ReadmeStyle = ReadmeStyle.PROFESSIONAL,
    author: str,
    license_name: str,
    force: bool,
    dry_run: bool,
    print_output: bool,
) -> None:
    try:
        root = path.expanduser().resolve()
        options = _make_options(root, style, author, license_name, force, dry_run)
        meta = detect_project(root, author=options.author, license_name=options.license_name)
        document = generate_document(kind, meta, options)
        if print_output:
            console.print(document.content)
            return
        result = write_document(root, document, force=options.force, dry_run=options.dry_run)
    except ReadmeKitError as exc:
        _fail(str(exc))
    _show_results([result])


def _make_options(
    root: Path,
    style: ReadmeStyle,
    author: str,
    license_name: str,
    force: bool,
    dry_run: bool,
) -> GeneratorOptions:
    try:
        config = load_config(root)
        options = options_from_config(
            config,
            GeneratorOptions(
                style=style,
                author=author,
                license_name=license_name,
                force=force,
                dry_run=dry_run,
            ),
        )
    except ConfigError as exc:
        raise ConfigError(str(exc)) from exc

    # CLI flags should override config for operational safety switches and common metadata.
    return GeneratorOptions(
        style=style,
        author=author or options.author,
        license_name=license_name or options.license_name,
        force=force or options.force,
        dry_run=dry_run or options.dry_run,
        include_code_of_conduct=options.include_code_of_conduct,
        include_issue_templates=options.include_issue_templates,
        include_pull_request_template=options.include_pull_request_template,
        values=options.values,
    )


def _show_results(results: list[object]) -> None:
    table = Table(title="ReadmeKit results")
    table.add_column("File", style="bold")
    table.add_column("Status")
    table.add_column("Reason")
    for result in results:
        relative_path = getattr(result, "relative_path")
        written = getattr(result, "written")
        skipped = getattr(result, "skipped")
        reason = getattr(result, "reason")
        if written:
            status = "[green]written[/green]"
        elif skipped:
            status = "[yellow]skipped[/yellow]"
        else:
            status = "[blue]planned[/blue]"
        table.add_row(str(relative_path), status, str(reason or "-"))
    console.print(table)


def _fail(message: str) -> None:
    console.print(Panel(message, title="ReadmeKit error", border_style="red"))
    raise typer.Exit(1)


if __name__ == "__main__":
    app()
