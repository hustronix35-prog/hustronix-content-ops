---
name: content-writer
description: Write LinkedIn and newsletter content from approved scored ideas. Founder Voice v1.0. Use after content-scorer passes.
---

# Content Writer

Runs after content-scorer passes on approved idea.

**Read first:** `.cursor/rules/founder-voice.mdc` — tone, structure, openings, endings, length.

## Input

```bash
python scripts/vault_query.py get content_ideas {id}
```

Read source material from `founder_intelligence`, `decision_patterns`, or `research_insights` based on `source_type`.

## Structure (every LinkedIn post)

```text
Observation → Pattern → Thought → Open Question
```

Sound like a founder sharing while building — not a creator optimizing for engagement.

## Output — Formats

Insert each into `content_drafts`:

| format | Spec |
|--------|------|
| linkedin_default | 180–300 words (most posts) |
| linkedin_deep | 300–500 words (research / building lessons) |
| linkedin_short | 80–150 words (quick observations) |
| twitter_thread | 5–8 tweets, numbered |
| newsletter | 150–250 word snippet for email |

**Never exceed 500 words on LinkedIn.**

```bash
python scripts/vault_query.py insert content_drafts '{"idea_id":1,"format":"linkedin_default","body":"..."}'
```

Also write `vault/drafts/{idea_id}-{format}.md`.

## Rules

- Founder Voice v1.0: humility ("I wonder", "I'm noticing"), approved openings/endings only
- Never sound like AI or LinkedIn bait (see hustronix-brand.mdc + founder-voice.mdc)
- Contrarian = thoughtful, not aggressive
- Research = implications, not summaries
- Build in public = learnings and surprises, not feature-shipped posts
- Founder-sourced: ≥1 real observation (anonymized if needed)
- Provide 2 alternative hooks in draft metadata comment

## Final Test

Founder sharing an observation — or creator chasing engagement? Rewrite if creator.

## After Writing

Re-run content-scorer on each draft before design-agent.

Update idea status to `approved` when drafts complete.
