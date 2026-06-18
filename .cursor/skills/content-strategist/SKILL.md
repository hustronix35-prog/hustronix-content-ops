---
name: content-strategist
description: Daily content ideation from founder intelligence, decision patterns, research, and category radar. Enforces 40/40/20 source mix. Use when generating content ideas or populating review queue.
---

# Content Strategist

Runs daily after research-agent. Produces 3–5 content ideas.

## Input Priority (strict mix)

| Share | Source | Query |
|-------|--------|-------|
| 40% | Founder | `founder_intelligence` + `decision_patterns` last 7 days |
| 40% | Research | `research_insights` + `category_narratives` + top `strategic_questions` by times_seen |
| 20% | Building | Hustronix building-in-public + `feature_hypotheses` validation stories |

```bash
python scripts/vault_query.py stats
python scripts/vault_query.py list founder_intelligence --limit 10
python scripts/vault_query.py list decision_patterns --limit 10
python scripts/vault_query.py list research_insights --limit 10
python scripts/vault_query.py list strategic_questions --limit 10
```

## Post Types

Research, Builder, Contrarian, Interview, Framework, Prediction

## Output Per Idea

Insert into `content_ideas`:

```json
{
  "pillar": "Decision Quality",
  "post_type": "Framework",
  "hook": "One-line hook for LinkedIn",
  "source_type": "founder|research|building",
  "source_id": 1,
  "status": "pending"
}
```

## Update Review Queue

Append to `review/queue.md`:

```markdown
### Idea #{id} — {post_type}
- **Pillar:** {pillar}
- **Source:** {source_type} (id: {source_id})
- **Hook:** {hook}
- **Status:** pending
```

## Rules

- Founder-sourced ideas MUST cite `founder_id` in hook context and include quote angle
- Decision pattern ideas → post_type Framework or Contrarian
- Strategic question ideas → post_type Research or Contrarian
- Never propose generic startup advice
- Enforce 40/40/20 mix across the 3–5 ideas (e.g., 2 founder, 2 research, 1 building)

## Posting Schedule Hints

Tag ideas with day preference in hook or notes:
- Monday: Decision Insight
- Wednesday: Research Breakdown
- Friday: Build In Public
- Sunday: Deep Carousel
