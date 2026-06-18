---
name: content-scorer
description: Score content ideas and drafts before writing. Reject below threshold. Use on approve idea or before publishing.
---

# Content Scorer

Gate before content-writer runs.

## Dimensions (0–10 each)

| Dimension | Direction |
|-----------|-----------|
| founder_relevance | Higher better |
| category_building | Higher better |
| conversation_potential | Higher better |
| di_alignment | Higher better |
| generic_ai_risk | Lower better |

## Thresholds

Reject if ANY:
- Any dimension (except generic_ai_risk) < **6**
- generic_ai_risk > **4**
- Composite < **28/40**

Composite = sum of first four + (10 - generic_ai_risk)

## Procedure

1. Read idea from `content_ideas` or draft from `content_drafts`
2. Evaluate against hustronix-brand.mdc rules
3. Record score:

```bash
python scripts/score_content.py --idea-id 1 --scores 8,7,8,9,2
python scripts/score_content.py --draft-id 1 --scores 8,8,7,9,1
```

4. If passed → proceed to content-writer
5. If failed → return to content-strategist with `rejection_reason`

## Re-score Drafts

Writer can drift. Always re-score draft before design-agent.

## Slack Flow

On `approve idea {id}`:
1. Score idea
2. If pass → content-writer
3. If fail → reply in thread with reasons
