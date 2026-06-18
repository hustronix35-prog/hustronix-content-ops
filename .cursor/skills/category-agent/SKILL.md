---
name: category-agent
description: Weekly category radar tracking market narratives for Decision Intelligence and related terms. Use Monday 9am or on demand.
---

# Category Agent

**Question:** What is the market currently believing?

## Schedule

Weekly Monday 9am.

## Track These Terms

- Decision Intelligence
- AI Chief of Staff
- Company Brain
- Organizational Intelligence
- Agentic Workflows
- Startup Operating Systems

## Per Term, Output

```text
Current Narrative
Emerging Narrative
Contrarian Opportunity
Content Gap
```

## Store

### Database

```bash
python scripts/vault_query.py insert category_narratives '{"week_of":"2026-06-16","category_term":"Decision Intelligence","current_narrative":"...","emerging_narrative":"...","contrarian_opportunity":"...","content_gap":"..."}'
```

### Markdown

`vault/category_radar/weekly-{YYYY-MM-DD}.md` — all terms in one report.

## Inputs

- Recent `research_insights`
- `competitor_intel` from prior week
- `decision_patterns` themes
- Web search for each category term

## Feeds

- content-strategist (40% research ideas)
- competitor-intelligence agent
- category-owned content angles

## Rules

- Not copying competitors — understanding narrative shifts
- Contrarian opportunity must be Hustronix-specific, not generic
