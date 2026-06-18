---
name: content-writer
description: Write LinkedIn and newsletter content from approved scored ideas. Four formats. Never sound like AI. Use after content-scorer passes.
---

# Content Writer

Runs after content-scorer passes on approved idea.

## Input

```bash
python scripts/vault_query.py get content_ideas {id}
```

Read source material from `founder_intelligence`, `decision_patterns`, or `research_insights` based on `source_type`.

## Output — 4 Formats

Insert each into `content_drafts`:

| format | Spec |
|--------|------|
| linkedin_short | < 150 words, punchy hook |
| linkedin_long | 200–400 words, framework or story |
| twitter_thread | 5–8 tweets, numbered |
| newsletter | 150–250 word snippet for email |

```bash
python scripts/vault_query.py insert content_drafts '{"idea_id":1,"format":"linkedin_short","body":"..."}'
```

Also write `vault/drafts/{idea_id}-{format}.md`.

## Rules

- Never sound like AI (see hustronix-brand.mdc bans)
- Never hype, never generic startup advice
- Always Decision Intelligence angle
- Founder-sourced: include ≥1 real observation (anonymized if needed)
- Decision pattern posts: use Trigger → Decision → Outcome → Lesson structure
- Provide 2 alternative hooks in draft metadata comment

## After Writing

Re-run content-scorer on each draft before design-agent.

Update idea status to `approved` when drafts complete.
