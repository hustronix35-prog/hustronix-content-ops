# Hustronix Marketing OS

> This is not a content automation system.
>
> This is a **Decision Intelligence system for marketing**.
>
> Every component is designed to become a reusable Hustronix subsystem.
> The marketing operation is the first dogfood environment for Hustronix.

## Triple Moat

```text
Decision Pattern Library + Visual Pattern Library + Founder Intelligence Database
```

## Primary KPIs

| Metric | Target |
|--------|--------|
| Founders in intelligence DB | **100** |
| Decision patterns | 200+ by month 12 |

Secondary: 10k followers (meaningless without founder depth).

## Quick Start

```bash
# Initialize database
python scripts/init_db.py

# Query vault
python scripts/vault_query.py list founders
python scripts/vault_query.py list content_ideas --status pending

# Ingest a URL
python scripts/ingest_url.py "https://example.com/article" --type article

# Score content / design
python scripts/score_content.py --idea-id 1 --scores 8,7,8,9,2
python scripts/score_design.py --draft-id 1 --scores 9,10,8,9,1
```

## Daily Workflow (< 30 min)

1. Review morning digest in Slack `#marketing-os`
2. Approve ideas: `approve idea {id}` in Slack
3. Light-edit drafts, paste to LinkedIn scheduler
4. After founder calls: `log founder conversation {name}` in Slack

## Content Source Mix

| Source | Share |
|--------|-------|
| Research | 40% |
| Founder Interviews | 40% |
| Building Hustronix | 20% |

## Agent Skills

Skills live in `.cursor/skills/`. Invoke by name in Cursor chat or via Cursor Automations (see `automations/README.md`).

| Skill | Schedule |
|-------|----------|
| source-ingestion | On demand / daily |
| research-agent | Daily 7am |
| content-strategist | Daily 7am |
| founder-intelligence-agent | After conversations / Sunday |
| founder-outreach | Weekdays 8am |
| content-scorer / content-writer | On approval |
| design-agent | After writer |
| category-agent / competitor-intelligence | Monday 9am |
| analytics-agent / learning-agent | Monday 10am |
| visual-intelligence-agent | Weekly with learning |

## Project Layout

```text
.cursor/rules/     Brand + design hard constraints
.cursor/skills/    Agent skill definitions
data/              SQLite vault (marketing.db)
vault/             Markdown artifacts
review/queue.md    Human approval queue
analytics/         Metrics CSV + reports
assets/generated/  Design briefs + visuals
scripts/           CLI utilities
automations/       Cursor Automation setup guides
```

## Signal → Decision → Execution → Outcome

```text
Research            → Signal
Founder Interviews  → Signal
Category Radar      → Signal
Content Strategy    → Decision
Publishing          → Execution
Analytics           → Outcome
Learning            → Signal
```
