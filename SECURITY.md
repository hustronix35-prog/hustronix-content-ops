# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| master  | :white_check_mark: |

## Reporting a Vulnerability

**Do not open public issues for security vulnerabilities.**

Report privately by opening a GitHub Security Advisory (if enabled) or contacting the repository maintainers with:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We aim to acknowledge reports within 48 hours.

## Secrets Handling

| Secret | Storage | Never |
|--------|---------|-------|
| `LINKEDIN_ACCESS_TOKEN` | `.env` / Cursor Dashboard Secrets | Commit to git |
| `LINKEDIN_AUTHOR_URN` | `.env` / Cursor Dashboard Secrets | Commit to git |
| `SLACK_BOT_TOKEN` | `.env` / Cursor Dashboard Secrets | Commit to git |
| `SLACK_CHANNEL_ID` | `.env` / Cursor Dashboard Secrets | Commit to git |

- `.env` is gitignored — verify before every commit
- Cursor Cloud Agents inject secrets at runtime; they appear in run logs only when misconfigured
- Rotate tokens immediately if exposed

## Scope Notes

- **LinkedIn tokens** expire (~60 days for standard OAuth). Regenerate at [LinkedIn Developer Portal](https://www.linkedin.com/developers/).
- **Slack bot tokens** should use minimum scopes: `files:write`, `chat:write`, `channels:read`
- **Private Slack channels** — automation run history may contain post content; treat as internal data
- **Vault data** — founder interview fixtures are synthetic/demo; do not load real PII without consent

## Known Limitations

- No automated OAuth refresh flow
- SQLite file is unencrypted at rest
- No rate limiting on local CLI scripts
- Cloud automation depends on third-party Cursor platform security model
