---
name: distribution-agent
description: Prepare platform-specific copy for LinkedIn and X. Paste-and-schedule only. Ships after content and design scores pass.
---

# Distribution Agent

Prepare-only. No LinkedIn API dependency.

## Prerequisites

- content-scorer passed on draft
- design-scorer passed (if visual post)
- Human approved final copy in Slack

## Posting Schedule

| Day | Content Type |
|-----|--------------|
| Monday | Decision Insight (often founder-sourced) |
| Wednesday | Research Breakdown |
| Friday | Build In Public |
| Sunday | Deep Carousel |

## Output

Write `vault/published/{draft_id}-distribution.md`:

```markdown
# Distribution Package — Draft #{draft_id}

## Platform: LinkedIn Personal (Priority 1)

**Post copy:**
{linkedin_long or linkedin_short}

**Carousel:** assets/generated/{draft_id}/ (if applicable)

**Suggested time:** {day} 8:00 AM local

## Platform: LinkedIn Company (Priority 2)

**Adapted copy:**
{shorter company version}

## Platform: Twitter/X (Priority 3)

**Thread:**
{twitter_thread body}
```

Insert `published_posts` when founder confirms scheduled:

```bash
python scripts/vault_query.py insert published_posts '{"draft_id":1,"platform":"linkedin_personal","scheduled_at":"2026-06-23T08:00:00","published_at":null}'
```

## Founder Action

1. Copy from distribution package
2. Paste into LinkedIn native scheduler (2-click)
3. Confirm in Slack: `published draft {id}`

## Rules

- Never auto-post
- LinkedIn personal is priority 1
- Include design assets path for carousels
