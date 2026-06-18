---
name: founder-outreach
description: Generate 5 ICP-matched founder profiles and personalized DM drafts for human review. Never auto-send. Use for daily outreach weekdays.
---

# Founder Outreach Agent

Semi-automated. Ends at DM generation — conversations go to founder-intelligence-agent.

## Schedule

Weekdays 8am via Cursor Automation.

## ICP (from hustronix-brand.mdc)

- Founder-led startups, pre-seed to Series A
- 2–50 employees, B2B SaaS / dev tools / AI-native
- Making decisions under uncertainty, using AI tools without decision infrastructure

## Daily Output

Find 5 founders matching ICP. For each:

1. Check if already in `founders` table
2. If new, create founder stub
3. Generate personalized connection request + follow-up message
4. Insert `founder_outreach` with `status: pending_review`

```bash
python scripts/vault_query.py insert founder_outreach '{"founder_id":1,"name":"...","company":"...","linkedin_url":"...","message_draft":"...","status":"pending_review"}'
```

## Message Rules

- Reference specific content they posted or company context
- No generic "I'd love to connect" spam
- Frame around Decision Intelligence / founder decision-making
- Ask one genuine question, not a pitch
- Max 300 characters for connection note

## Human Gate

**NEVER auto-send.** All messages stay `pending_review` until founder approves in Slack.

Post daily batch to `#marketing-os`:

```text
## Founder Outreach — {date}
### 1. {name} @ {company}
**LinkedIn:** {url}
**Draft:** {message}
→ Reply "approve outreach {id}" to mark ready
```

## KPI

Month 1: 20 founder DMs drafted. Quality over volume.
