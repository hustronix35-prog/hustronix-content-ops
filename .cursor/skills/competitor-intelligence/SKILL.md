---
name: competitor-intelligence
description: Track narrative shifts from Glean, Notion AI, Linear, Claude, OpenAI agents, and decision startups. Runs with category-agent weekly.
---

# Competitor Intelligence Agent

Purpose: understand narrative shifts, not copy positioning.

## Schedule

Weekly Monday 9am (with category-agent).

## Track

- Glean
- Notion AI
- Linear
- Claude (Anthropic)
- OpenAI agents
- Agentic startups (Cognition, etc.)
- Decision-related startups

## Per Competitor

Extract:
- **narrative_shift** — what changed in their messaging
- **positioning_change** — how they're repositioning
- **content_angle** — what Hustronix should say (not copy)

## Store

```bash
python scripts/vault_query.py insert competitor_intel '{"competitor":"Glean","narrative_shift":"...","positioning_change":"...","content_angle":"..."}'
```

Write `vault/competitor_intel/{YYYY-MM-DD}.md`.

## Rules

- Never copy their messaging
- Focus on gaps Hustronix fills: Decision Intelligence for founders
- Link shifts to category_narratives contrarian opportunities
