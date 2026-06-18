---
name: design-agent
description: Brand-first YAML design brief generator for Hustronix visuals. NOT generic image generation. Read design.mdc hard constraints first.
---

# Design Agent v2 — Brand-First Generation

**Read `.cursor/rules/design.mdc` before every run. Hard constraint, not reference.**

## Never

- Generate random startup graphics
- Call image tool without scored YAML brief
- Use colors or fonts outside brand spec

## Step 1 — Classify Visual Category

| Source | Category |
|--------|----------|
| decision_patterns row | decision_pattern |
| strategic_questions row | strategic_question |
| founder_intelligence row | founder_insight |
| framework / research insight | execution_model |
| category radar / vision | future_of_organizations |

## Step 2 — Check Visual Pattern Library

```bash
python scripts/vault_query.py list visual_patterns --limit 10
```

Prefer top-performing patterns from `vault/visual_patterns/`.

## Step 3 — Generate YAML Brief

Write `assets/generated/{draft_id}/design-brief.yaml`:

```yaml
topic: Decision Intelligence
audience: Seed-Series B Founders
visual_type: Executive Carousel
visual_category: decision_pattern
brand_rules:
  background: "#0A0A0A"
  typography: "#EDEDED"
  accent: "#D4AF37"
  font: Inter
layout: Minimal, Linear-inspired
slides:
  - name: Hook
    content: "..."
  - name: Problem
    content: "..."
  - name: Framework
    content: "..."
  - name: Example
    content: "..."
  - name: Insight
    content: "..."
  - name: CTA
    content: "..."
```

Write per-slide specs to `assets/generated/{draft_id}/slide-specs/`.

## Step 4 — Design Score

Run design-scorer skill / `python scripts/score_design.py` before any image generation.

## Step 5 — Generate Images (only if score passes)

Use Cursor image generation with brief as input. One image per slide.

## Principle

Every visual = one strategic insight. Clarity > Creativity.
