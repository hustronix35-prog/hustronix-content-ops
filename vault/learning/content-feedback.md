# Content Quality Feedback — Strict Gate

*Last updated: 2026-06-19. Apply to all post generation until superseded.*

## Core failure mode (fix immediately)

The system was doing:

```text
Hook → Observation → Repeat uncertainty 4×
```

Required structure:

```text
Hook → Observation → Example → Insight → End
```

## Hard rules

| Rule | Value |
|------|-------|
| `max_uncertainty_statements` | **1** per post |
| Contrarian posts | Need evidence, story, or founder observation — not clever one-liners |
| Research posts | Must not sound like generic AI founder posts |
| Builder posts | Most authentic when tied to Hustronix; cut hedging by ~70% |

## Forbidden patterns (never use more than once; many are banned entirely)

- "Curious what others think"
- "Still exploring this idea"
- "I could be wrong"
- "Not sure if this is broadly true"
- "I'm still trying to understand whether this pattern holds at scale"
- "It might be specific to the founders I've spoken with so far"
- Multiple uncertainty / humility statements in the same post

## Approved closings (pick one max)

- "That's a pattern I'm paying close attention to right now."
- "I'm starting to think [specific insight]."
- One open question tied to the observation (not generic engagement bait)

## Scoring reference (2026-06-19 batch)

| Option | Score | Verdict |
|--------|-------|---------|
| Option 3 Contrarian | 8.8/10 | **Publish candidate** — rewrite ending only |
| Option 1 Builder | 8.2/10 | Authentic but over-hedged |
| Option 2 Research | 6.8/10 | Do not publish as-is — lacks evidence/story |

## Gold-standard rewrite (Option 3 target ~9.3/10)

Tone: founder → observation → insight. Not AI → thought leadership → engagement bait.

Use `.cursor/rules/founder-voice.mdc` and `scripts/lib/linkedin_posts.py` templates aligned to this bar.
