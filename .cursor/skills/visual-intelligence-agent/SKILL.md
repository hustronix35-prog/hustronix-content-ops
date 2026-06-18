---
name: visual-intelligence-agent
description: Learn which visual structures perform best. Updates visual pattern library. Runs weekly with learning-agent.
---

# Visual Intelligence Agent

Parallel to decision pattern library — for visuals.

## Schedule

Weekly with learning-agent (Monday after analytics).

## Track Performance By

- Decision Pattern visuals
- Strategic Question visuals
- Framework / flowchart visuals
- Quote cards
- Carousels (by slide count and structure)

## Inputs

- `analytics_snapshots` joined with `design_scores` and `published_posts`
- `visual_patterns` table
- `assets/generated/` example paths

## Procedure

1. Rank visual categories by engagement rate
2. Update `visual_patterns.performance_score` for each pattern
3. Increment `times_used` for patterns used in published posts
4. Write/update `vault/visual_patterns/{name}.yaml`:

```yaml
pattern:
  name: decision_pattern_vertical_v1
  category: decision_pattern
  performance: 0.82
  times_used: 5
  examples:
    - assets/generated/42/
  notes: "Outperformed quote cards 2.3x on comments"
```

## Output

Section in `vault/learning/recommendations.md`:

```markdown
### Visual Intelligence
- decision_pattern carousels: 2.3x comments vs quote cards
- Recommend: use decision_pattern_vertical_v1 for Monday posts
```

## Feeds

- design-agent (prefer top-performing patterns)
- content-strategist (suggest visual-friendly idea types for Sunday carousels)

## Triple Moat

Decision Pattern Library + **Visual Pattern Library** + Founder Intelligence Database
