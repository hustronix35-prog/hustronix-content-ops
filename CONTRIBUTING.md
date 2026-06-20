# Contributing to Hustronix Content Ops

Thank you for your interest in contributing. This project is designed as portfolio-grade open source — we welcome improvements that increase clarity, reliability, and voice quality.

## How to Contribute

1. **Fork** the repository
2. **Create a branch** from `master`: `git checkout -b feat/your-feature`
3. **Make changes** following existing conventions
4. **Test locally** (see below)
5. **Open a pull request** using the PR template

## Development Setup

```bash
git clone https://github.com/hustronix35-prog/hustronix-content-ops.git
cd hustronix-content-ops
python -m venv .venv
pip install -r requirements.txt
python scripts/setup_carousel_env.py
python scripts/init_db.py
```

Copy `.env.example` to `.env` for LinkedIn/Slack integration tests.

## What We Welcome

- Voice rule improvements (`.cursor/rules/founder-voice.mdc`)
- Carousel layout and brand system enhancements
- Pipeline reliability and error handling
- Documentation and architecture diagrams
- Tests for post generation and workflow state
- Integration adapters (other channels, CMS exports)

## What to Avoid

- Committing secrets (`.env`, tokens, real founder PII)
- Auto-publish without human approval gates
- Generic AI content patterns (see `vault/learning/content-feedback.md`)
- Large unrelated refactors in a single PR

## Code Style

- Python 3.12+, type hints where helpful
- Match existing script structure in `scripts/` and `scripts/lib/`
- CLI scripts print JSON to stdout for automation parsing
- Keep changes focused — one concern per PR

## Testing

```bash
# Carousel smoke test
python scripts/validate_carousel_setup.py
python scripts/generate_carousel.py --idea-id 1

# Voice validation (when pytest added)
pytest tests/ -v
```

## Commit Messages

Use clear, imperative messages:

- `fix: form-encode Slack file upload API`
- `docs: add architecture data flow diagram`
- `feat: enforce max 1 uncertainty statement per post`

## Questions

Open a [Discussion](https://github.com/hustronix35-prog/hustronix-content-ops/discussions) or issue with the `question` label.
