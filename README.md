<div align="center">

# ReadmeKit

**A Python CLI that generates clean README, CONTRIBUTING, SECURITY, and GitHub documentation for repositories.**

ReadmeKit helps developers turn empty or unfinished repositories into professional GitHub projects with polished Markdown documentation and community files.

<br>

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python&logoColor=white)
![CLI](https://img.shields.io/badge/CLI-Typer-0E7C86?style=flat)
![Terminal](https://img.shields.io/badge/Terminal-Rich-4B8BBE?style=flat)
![Config](https://img.shields.io/badge/Config-YAML-yellow?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

</div>

---

## Overview

ReadmeKit is a documentation generator for GitHub repositories. It scans a project folder, detects basic project details, and creates useful Markdown files such as `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue templates, and pull request templates.

The goal is simple: help developers create clean repository documentation without starting from a blank file every time.

ReadmeKit works locally, does not require an API key, and does not upload your project files anywhere.

---

## Why ReadmeKit?

A good repository needs more than code. It should explain what the project does, how to install it, how to use it, how to contribute, and how to report security problems.

ReadmeKit helps with that by generating documentation that is:

- Clean and readable
- GitHub-friendly
- Project-aware
- Easy to edit after generation
- Useful for open-source repositories
- Practical for personal and professional projects

---

## Features

- Generate a professional `README.md`
- Generate `CONTRIBUTING.md`
- Generate `SECURITY.md`
- Generate `CODE_OF_CONDUCT.md`
- Generate GitHub issue templates
- Generate a pull request template
- Inspect project metadata before writing docs
- Detect Python, Node, Rust, Go, and general projects
- Read metadata from files like `pyproject.toml` and `package.json`
- Support multiple README styles
- Support local `.readmekit.yaml` configuration
- Skip existing files by default for safety
- Use `--force` when you intentionally want to overwrite files
- Use `--dry-run` to preview write operations
- Use `--print` or `preview` to inspect generated output

---

## Installation

Clone the repository:

```bash
git clone https://github.com/n-vim/ReadmeKit.git
cd ReadmeKit
```

Install locally:

```bash
python -m pip install -e .
```

Install with development tools:

```bash
python -m pip install -e ".[dev]"
```

Check the CLI:

```bash
readmekit --help
```

You can also use:

```bash
readme-kit --help
```

---

## Quick Start

Inspect the current repository:

```bash
readmekit inspect .
```

Generate a README:

```bash
readmekit readme .
```

Generate all supported documentation files:

```bash
readmekit all .
```

Preview a README without writing it:

```bash
readmekit preview . --kind readme
```

Print a generated README to the terminal:

```bash
readmekit readme . --print
```

Overwrite an existing file intentionally:

```bash
readmekit readme . --force
```

---

## Commands

| Command | Description |
| --- | --- |
| `readmekit inspect .` | Show detected project metadata |
| `readmekit init .` | Create a `.readmekit.yaml` config file |
| `readmekit readme .` | Generate `README.md` |
| `readmekit contributing .` | Generate `CONTRIBUTING.md` |
| `readmekit security .` | Generate `SECURITY.md` |
| `readmekit github .` | Generate GitHub issue and PR templates |
| `readmekit all .` | Generate the full documentation set |
| `readmekit preview . --kind readme` | Preview a document without writing files |

---

## Generated Files

When you run `readmekit all .`, ReadmeKit can create:

```text
README.md
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
.github/ISSUE_TEMPLATE/bug_report.md
.github/ISSUE_TEMPLATE/feature_request.md
.github/pull_request_template.md
```

Existing files are skipped unless you pass `--force`.

---

## README Styles

ReadmeKit supports three README styles:

| Style | Best For |
| --- | --- |
| `minimal` | Small projects that need a short README |
| `professional` | Most GitHub repositories |
| `detailed` | Projects that need extra explanation and quality notes |

Example:

```bash
readmekit readme . --style detailed
```

---

## Configuration

Create a config file:

```bash
readmekit init .
```

This creates `.readmekit.yaml`:

```yaml
author: Nitish Vimal
license: MIT
style: professional

include_code_of_conduct: true
include_issue_templates: true
include_pull_request_template: true
force: false
values: {}
```

Config files help keep documentation generation consistent across projects.

---

## Safety Behavior

ReadmeKit is designed to be safe by default.

- It does not overwrite files unless `--force` is used
- It does not execute code from the scanned project
- It does not upload repository contents anywhere
- It only writes files inside the target repository
- It supports `--dry-run` for safe previews

Example dry run:

```bash
readmekit all . --dry-run
```

---

## Project Structure

```text
ReadmeKit/
├── src/
│   └── readmekit/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── detector.py
│       ├── exceptions.py
│       ├── generator.py
│       ├── markdown.py
│       ├── models.py
│       ├── templates.py
│       └── utils.py
├── tests/
├── .github/
│   └── workflows/
│       └── ci.yml
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── README.md
└── SECURITY.md
```

---

## Built With

| Tool | Purpose |
| --- | --- |
| Python | Main programming language |
| Typer | Command-line interface |
| Rich | Terminal output |
| PyYAML | Config file support |
| Pytest | Testing |
| Ruff | Linting |
| Mypy | Type checking |
| Hatchling | Build backend |

---

## Development

Install development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

Run type checking:

```bash
mypy src
```

---

## Example Workflow

A common workflow looks like this:

```bash
git clone https://github.com/n-vim/ReadmeKit.git
cd ReadmeKit
python -m pip install -e ".[dev]"
pytest
readmekit inspect .
readmekit all . --dry-run
```

---

## Good Use Cases

ReadmeKit is useful for:

- New repositories with no documentation
- Python CLI projects
- Open-source projects
- Student GitHub projects
- Developer tool repositories
- Projects that need GitHub community files
- Quickly improving repository presentation
- Creating consistent documentation across many repos

---

## Roadmap

Planned improvements:

- More project type detectors
- More README layouts
- Better command and dependency detection
- Documentation quality scoring
- Markdown cleanup mode
- Optional badge generation profiles
- Better support for monorepos
- More GitHub template options

---

## Contributing

Contributions are welcome. You can help by improving generators, adding tests, refining detection logic, or improving documentation.

Please read `CONTRIBUTING.md` before opening a pull request.

---

## Author

Created by **Nitish Vimal**.

GitHub: [n-vim](https://github.com/n-vim)

---

## License

This project is licensed under the MIT License.

---

<div align="center">

**ReadmeKit helps you create better GitHub documentation faster.**

</div>
