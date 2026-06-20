# Quickstart — 10-Minute Demo

For recruiters, contributors, or portfolio reviewers who want to see Content Ops running locally.

## Prerequisites

- Python 3.12+
- Git

## 1. Clone and install (3 min)

```bash
git clone https://github.com/hustronix35-prog/hustronix-content-ops.git
cd hustronix-content-ops
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python scripts/setup_carousel_env.py
python scripts/init_db.py
python scripts/seed_vault.py
```

## 2. Generate post options (2 min)

```bash
python scripts/generate_post_options.py
```

Output: 3 LinkedIn post options with Founder Voice v2.0 quality gates.

## 3. Generate carousel (3 min)

```bash
python scripts/generate_carousel.py --idea-id 1
```

Open `assets/generated/1/preview.html` in a browser — 7 intelligent slides.

## 4. Run tests (1 min)

```bash
python -m pytest tests/ -v
```

Validates voice rules: forbidden phrases, uncertainty caps.

## 5. Read portfolio docs (1 min)

| Doc | Purpose |
|-----|---------|
| [portfolio-case-study.md](portfolio-case-study.md) | 5-min recruiter overview |
| [architecture.md](architecture.md) | System design |
| [product.md](product.md) | Personas and metrics |

## Optional — Full Slack + LinkedIn

Copy `.env.example` → `.env`, add tokens. See [automations/SLACK_LINKEDIN_SETUP.md](../automations/SLACK_LINKEDIN_SETUP.md).

```bash
python scripts/slack_post_workflow.py "select 1"
python scripts/slack_post_workflow.py "carousel"
python scripts/slack_post_workflow.py "publish"
```

## What to show in an interview

1. **Problem:** AI-slop vs. decision-quality content
2. **Demo:** `generate_post_options.py` → show voice rules in `.cursor/rules/founder-voice.mdc`
3. **Architecture:** README Mermaid diagram
4. **Trade-off:** Human publish gate vs. full automation
