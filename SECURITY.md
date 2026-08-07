# Security Policy

ReadmeKit is a local documentation generator. It scans repository files to understand a project and writes Markdown documentation when requested.

Security matters because the tool works with local project folders and may run inside repositories that contain private files or sensitive configuration.

---

## Supported Versions

Security fixes are handled for the latest release and the current `main` branch.

| Version | Supported |
| --- | --- |
| Latest release | Yes |
| `main` branch | Yes |
| Older releases | No |

---

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues.

Use GitHub private vulnerability reporting if it is available. If it is not available, open a public issue asking for a private contact method, but do not include technical details, exploit steps, secrets, or sensitive files in the public issue.

When reporting a vulnerability, include safe details such as:

- A short summary of the issue
- The affected command or module
- The version or commit tested
- Steps to reproduce the issue
- The possible impact
- Any suggested fix

Do not include real tokens, passwords, private keys, or private repository contents.

---

## Security Expectations

ReadmeKit should:

- Not execute code from scanned repositories
- Not upload repository contents anywhere
- Not expose secrets in generated documentation
- Not write files outside the target repository
- Skip overwriting files unless the user passes `--force`
- Handle unusual file names safely
- Keep dependencies minimal and maintained

---

## Sensitive Files

Repositories may include sensitive files such as:

- `.env`
- `.env.local`
- Private keys
- API tokens
- Cloud credentials
- Deployment secrets
- Local database files

ReadmeKit should never print or copy secret values into generated documentation.

---

## Responsible Disclosure

Please give maintainers reasonable time to investigate and fix security issues before sharing details publicly.

A good process is:

1. Report the issue privately.
2. Allow time for review and fixes.
3. Help verify the fix if possible.
4. Avoid publishing exploit details before the fix is available.

---

## Thank You

Thank you for helping keep ReadmeKit safe and trustworthy.
