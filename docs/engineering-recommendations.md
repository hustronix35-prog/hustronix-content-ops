# Engineering Recommendations — Hustronix Content Ops

Recommendations before major refactors. Prioritized by impact vs. effort.

---

## P0 — Do Now (Completed or In Progress)

| Item | Status | Notes |
|------|--------|-------|
| MIT LICENSE | ✅ Done | `LICENSE` |
| OSS templates | ✅ Done | CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue/PR templates |
| Portfolio docs | ✅ Done | README, architecture, product, case study |
| Rename repo refs | 🔄 In progress | Update automation prefills to `hustronix-content-ops` |
| Slack upload fix | ✅ Done | Form-encoded API in `slack_upload.py` |
| Voice v2.0 | ✅ Done | `founder-voice.mdc` + `linkedin_posts.py` |

---

## P1 — High Impact, Low Effort

### 1. Voice validation tests

```python
# tests/test_linkedin_posts.py
def test_no_stacked_uncertainty():
    body = generate_post_body(...)
    assert count_uncertainty(body) <= 1
```

**Why:** Prevents regression on the core product differentiator.

### 2. Structured logging

Replace `print(json.dumps(...))` with optional `--json` flag + stderr logging for errors.

**Why:** Automation parsing stays stable; debugging improves.

### 3. Parameterized repo config

Single `config/repo.yaml`:

```yaml
github:
  org: hustronix35-prog
  repo: hustronix-content-ops
  branch: master
slack:
  channel: "#marketing-os"
```

**Why:** Forks and renames don't require grep-replace across 15 files.

### 4. `.env` validation on startup

Extend `env_config.py` to fail fast with actionable messages when publish/carousel secrets missing.

---

## P2 — Medium Effort

### 5. pytest CI job

Add `.github/workflows/test.yml`:

- `pytest tests/`
- `python scripts/validate_carousel_setup.py`

### 6. Deprecate legacy scripts

Mark as deprecated in docstrings:

- `slack_approve_and_post.py` → use `slack_post_workflow.py`
- `short_posts.py` → merged into `linkedin_posts.py`

Remove in v2.0 after one release cycle.

### 7. SQLite migrations

Replace ad-hoc `ALTER TABLE` with numbered migrations in `scripts/migrations/`.

### 8. LinkedIn token refresh

Document OAuth refresh flow; add `scripts/linkedin_token_check.py` that warns 7 days before expiry.

---

## P3 — Larger Refactors (Defer)

| Item | Rationale for deferral |
|------|------------------------|
| FastAPI gateway | CLI-first is correct for current stage |
| Postgres multi-tenant | No second customer yet |
| Docker Compose | Add when onboarding contributors |
| Web dashboard | Slack is the UI for now |
| Queue-based render | Playwright is fast enough for 7 slides |

---

## Security Hardening

1. Add pre-commit hook to block `.env` commits
2. Scan vault fixtures for accidental PII before publish
3. Document Slack bot scope minimum in SECURITY.md ✅
4. Add `scripts/check_secrets.py` — grep staged files for token patterns

---

## Documentation Gaps (Remaining)

- [ ] Replace screenshot placeholders with real `#marketing-os` captures
- [ ] Add `docs/QUICKSTART.md` — 10-minute local demo script
- [ ] Video walkthrough link (optional, high recruiter value)

---

## Refactoring Principles Applied

- **Minimal scope** — Voice rewrite targeted `linkedin_posts.py`, not full pipeline
- **Existing conventions** — JSON stdout, `scripts/lib/` modules, Cursor skills unchanged
- **Human gates preserved** — No auto-publish without explicit `publish` command
- **Portfolio first** — Docs and OSS files ship before infrastructure rewrites
