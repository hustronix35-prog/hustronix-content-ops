# Hustronix Marketing Chat (@mention only)

## Trigger

| Setting | Value |
|---------|--------|
| **Channel** | `#marketing-os` |
| **When** | User **@mentions** the bot only |
| **Ignore** | Messages without @mention |

Prefill: `automations/prefill/slack-marketing-chat.json`

## What it does

- Discuss post options, hooks, quality scores
- Accept strict feedback (like content-feedback.md)
- Regenerate when asked (`generate_post_options.py`, `select`, `carousel`)
- Save feedback to `vault/learning/content-feedback.md` when asked

## What it does NOT do

- Reply to every message in the channel (command automation handles `select` / `carousel` / `publish`)
- Auto-publish
- Stack "still exploring" / "curious what others think" phrases

## Setup in Cursor Automations UI

1. **New automation** → name: `Hustronix Marketing Chat`
2. **Slack trigger** → `#marketing-os` → **@mention only** (if available) or instruct in prompt
3. **Repo** → `hustronix35-prog/hustronix-content-ops` / `master`
4. Paste prompt from prefill JSON

## Three automations together

| Automation | Trigger | Role |
|------------|---------|------|
| Daily Research Pipeline | Cron 7 AM | 3 post options |
| Post Workflow | `select` / `carousel` / `publish` | Publish loop |
| **Marketing Chat** | **@mention** | Discuss, feedback, revise |

Commands still work without @mention. Chat only when you @mention.
