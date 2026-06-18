# Cursor Automations Setup

## Quick commands (no Slack required)

```bash
# Daily digest (replaces morning Slack post until Slack MCP connected)
python scripts/daily_digest.py

# Approve an idea → full pipeline (score, drafts, design brief, distribution)
python scripts/approve_idea.py 3

# Vault stats
python scripts/vault_query.py stats
```

## Open automations in Cursor

Prefill JSON files are in `automations/prefill/`. Ask Cursor: **"open automation from automations/prefill/daily-research-pipeline.json"**

Or use the Automations UI with these specs:

### 1. Daily Research Pipeline

| Field | Value |
|-------|-------|
| **Trigger** | Cron `0 7 * * *` (7:00 daily) |
| **Prompt** | Run skills in order: `source-ingestion` (check for new URLs) → `research-agent` (process unprocessed raw_sources) → `content-strategist` (generate 3-5 ideas, update review/queue.md). Post summary to Slack #marketing-os. |
| **Tools** | Slack MCP, file read/write |

### 2. Daily Founder Outreach

| Field | Value |
|-------|-------|
| **Trigger** | Cron `0 8 * * 1-5` (weekdays 8:00) |
| **Prompt** | Run `founder-outreach` skill. Generate 5 ICP-matched founder DM drafts. Post to #marketing-os for review. Never auto-send. |

### 3. Weekly Category Radar

| Field | Value |
|-------|-------|
| **Trigger** | Cron `0 9 * * 1` (Monday 9:00) |
| **Prompt** | Run `category-agent` then `competitor-intelligence`. Write to vault/category_radar/ and vault/competitor_intel/. Post summary to Slack. |

### 4. Weekly Analytics + Learning

| Field | Value |
|-------|-------|
| **Trigger** | Cron `0 10 * * 1` (Monday 10:00) |
| **Prompt** | Run `analytics-agent` (read analytics/metrics.csv) then `learning-agent` then `visual-intelligence-agent`. Write reports to analytics/reports/ and vault/learning/. Post to Slack. |

### 5. Sunday Founder Brief

| Field | Value |
|-------|-------|
| **Trigger** | Cron `0 9 * * 0` (Sunday 9:00) |
| **Prompt** | Run `founder-intelligence-agent` weekly synthesis. Write analytics/reports/founder-brief/weekly-{date}.md. Post internal summary to Slack. |

## Slack Command Automations

### Ingest URL

| Field | Value |
|-------|-------|
| **Trigger** | Slack message matching `ingest ` |
| **Prompt** | Extract URL from message. Run `source-ingestion` skill / `python scripts/ingest_url.py {url}`. Confirm in thread. |

### Log Founder Conversation

| Field | Value |
|-------|-------|
| **Trigger** | Slack message matching `log founder conversation` |
| **Prompt** | Run `founder-intelligence-agent` with conversation notes from thread. Full 5-step extraction pipeline. |

### Approve Idea

| Field | Value |
|-------|-------|
| **Trigger** | Slack message matching `approve idea ` |
| **Prompt** | Extract idea ID. Run `content-scorer` → if pass `content-writer` → `design-agent` → `design-scorer`. Reply in thread with drafts, design brief, and scores. |

## Manual Setup Note

Cursor Automations must be finalized in the Automations UI. This file is the specification — use "create a Cursor automation" in Agents Window to draft each one.

## Daily Review (< 30 min)

1. Morning digest in #marketing-os (10 min)
2. `approve idea {id}` + light edit drafts (10 min)
3. Log founder conversation OR send 2-3 approved DMs (10 min)
