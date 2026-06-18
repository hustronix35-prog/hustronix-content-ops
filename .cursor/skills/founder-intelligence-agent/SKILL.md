---
name: founder-intelligence-agent
description: Convert founder conversations into intelligence, strategic questions, decision patterns, product requirements, and feature hypotheses. Use after calls or when user says log founder conversation.
---

# Founder Intelligence Agent

Highest-value agent. Converts conversations into product intelligence.

## Trigger

- Slack: `log founder conversation {name}`
- User pastes interview notes or transcript
- Sunday: weekly synthesis (Founder Intelligence Report)

## Mandatory 5-Step Extraction Pipeline

Every conversation MUST produce:

```text
1. founder_intelligence row
2. strategic_questions mapping (≥1)
3. decision_patterns (if decision discussed)
4. product_requirements (if pain surfaced)
5. feature_hypotheses (if product implication)
```

## Step 1 — Upsert Founder

```bash
python scripts/vault_query.py insert founders '{"name":"Sarah Chen","company":"Acme AI","founder_stage":"seed","company_size":"2-10","industry":"B2B SaaS","pilot_interest":"curious"}'
```

Update `interview_count`, `relationship_score`, `last_contact_at`, aggregate `pain_points` JSON.

## Step 2 — Founder Intelligence

Extract: pain, current_stack, decision_process, biggest_friction, interesting_quotes, product_implications, content_angles.

Write `vault/founder_intelligence/{founder_id}-{date}.md`.

## Step 3 — Strategic Questions

Map conversation to at least one question. Increment `times_seen` if question exists:

Categories: hiring, fundraising, product, gtm, org, firing

## Step 4 — Decision Patterns

If founder discussed a past decision:

```text
Trigger → Decision → Outcome → Lesson (why_it_worked or why_it_failed)
```

Write `vault/decision_patterns/{id}.md`. Source: `founder_id`.

## Step 5 — Product Insights

If product implications surfaced:

- `product_requirements` row with pain_evidence quote
- `feature_hypotheses` row: "If we build X, founders will Y"

Write `vault/product_insights/{id}.md`.

## Sunday — Founder Intelligence Report

Synthesize week into `analytics/reports/founder-brief/weekly-{YYYY-MM-DD}.md`:

```text
What founders talked about
Top pain points
Most common decision bottlenecks
Top strategic questions (by times_seen)
New decision patterns
Product requirements surfaced
Feature hypotheses to validate
Product implications
```

Post summary to Slack `#marketing-os` (internal).

## Rules

- Verbatim quotes only with permission context noted
- This is intelligence, not CRM — depth over contact count
- Primary KPI: 100 founders in database
