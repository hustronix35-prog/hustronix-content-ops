# Premium Carousel — Cloud Consistency

Yes — **premium carousels will render consistently online** if these are in place.

## What must be on GitHub (`marketing-os` / `master`)

| Path | Why |
|------|-----|
| `assets/brand/logo-lockup.png` | Exact logo (embedded in every slide) |
| `assets/brand/logo-horizontal.png` | Alternate lockup |
| `assets/brand/premium.css` | Premium v2 styles |
| `assets/brand/hex-grid.svg` | Background texture |
| `scripts/lib/carousel_*.py` | Builder + renderer + visuals |
| `scripts/setup_carousel_env.py` | Installs Playwright Chromium in cloud |
| `scripts/validate_carousel_setup.py` | Fails fast if setup broken |
| `requirements.txt` | `playwright`, `PyYAML` |

**Do not commit** `assets/generated/` — cloud regenerates on each `carousel` command.

## Cursor Automation setup

**Post Workflow** automation prompt must run setup before carousel:

```
1. python scripts/setup_carousel_env.py   (first run or if carousel fails)
2. python scripts/slack_post_workflow.py "{message}"
```

Or rely on auto-setup: `generate_carousel.py` calls `ensure_render_ready()` which installs Chromium if missing.

**Automation settings:**
- Repo: `hustronix35-prog/marketing-os`
- Branch: `master`
- `skipInstall: false` (allows pip install from requirements.txt)

**Secrets:**
- `SLACK_BOT_TOKEN` + `SLACK_CHANNEL_ID` — upload PNGs to Slack
- `LINKEDIN_ACCESS_TOKEN` + `LINKEDIN_AUTHOR_URN` — publish step

## CI guarantee

GitHub Action `.github/workflows/carousel.yml` runs on every push:
1. Installs Playwright Chromium
2. Validates brand assets
3. Generates idea #3 carousel
4. Asserts 6/6 premium PNGs

If CI passes, cloud automations use the same code path.

## Quality tier locked

Every manifest includes:
```json
"quality": "premium_v2",
"render_complete": true
```

If PNG render fails partially, the script **errors** instead of silently shipping basic HTML.

## One-time local check

```bash
pip install -r requirements.txt
python scripts/setup_carousel_env.py
python scripts/generate_carousel.py --idea-id 3
```

Open `assets/generated/3/preview.html`.

## Current blocker

Most carousel code is **not pushed yet** (local only). Push to `master` for online automations to use Premium v2.
