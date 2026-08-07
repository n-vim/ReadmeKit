# Contributing to ReadmeKit

Thank you for your interest in contributing to ReadmeKit.

ReadmeKit is a Python CLI tool that generates professional GitHub documentation for repositories. The project should stay simple, practical, readable, and safe to use.

---

## Ways to Contribute

You can contribute by:

- Fixing bugs
- Improving project detection
- Improving generated Markdown quality
- Adding tests
- Improving CLI messages
- Improving documentation
- Adding safe and useful generator options
- Suggesting practical features

Small improvements are welcome.

---

## Development Setup

Clone the repository:

```bash
git clone https://github.com/n-vim/ReadmeKit.git
cd ReadmeKit
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the project with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Check the CLI:

```bash
readmekit --help
```

---

## Running Tests

Run the test suite:

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

Please make sure tests pass before opening a pull request.

---

## Pull Request Guidelines

Before opening a pull request:

- Keep the change focused
- Explain what changed and why
- Add or update tests when needed
- Update documentation when behavior changes
- Avoid unrelated formatting changes
- Do not commit cache files, build files, virtual environments, or secrets
- Keep the code readable and beginner-friendly

---

## Commit Messages

Use clear commit messages.

Good examples:

```text
Add pull request template generator
Fix README detection for Python projects
Improve config validation errors
Add tests for dry-run writes
```

Avoid unclear messages like:

```text
update
fix
changes
final
```

---

## Adding New Generators

When adding a new generated document:

1. Add a clear document kind.
2. Build the Markdown in a dedicated function.
3. Keep the generated text useful and editable.
4. Avoid placeholder-heavy output.
5. Add tests for the generated file.
6. Update the README if the new generator is user-facing.

---

## Documentation Style

Generated documentation should be:

- Clear
- Practical
- Professional
- Easy to edit
- GitHub-friendly
- Free from unnecessary filler

Avoid vague or over-designed documentation.

---

## License

By contributing to ReadmeKit, you agree that your contributions will be licensed under the MIT License.
