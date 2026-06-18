---
name: learning-agent
description: Weekly learning from analytics and vault patterns. Produces recommendations for strategist, category-agent, and visual-intelligence-agent.
---

# Learning Agent

Runs weekly after analytics-agent.

## Inputs

- `analytics/reports/weekly-{date}.md`
- `content_scores` and `design_scores` history
- `founder_intelligence` patterns (pain frequency)
- `strategic_questions` by times_seen
- `decision_patterns` usage in content

## Questions to Answer

1. Which topics perform best?
2. Which hooks perform best?
3. Which content formats perform best?
4. Which founders engage?
5. Which pain points recur in conversations?
6. Founder-sourced vs research content performance?

## Output

Append to `vault/learning/recommendations.md`:

```markdown
## Week of {date}

### Performance Insights
- "Decision Quality content outperformed AI content by 230%"
- "Founder interview content generated 4x more conversations"

### Content Recommendations
- Increase {topic} by {percent}
- Reduce {topic}

### Founder Intelligence Patterns
- Pain point X appeared in 6/10 conversations

### Strategic Questions Trending
- "Should we hire?" times_seen: 12
```

## Feeds

- content-strategist (next week's ideas)
- category-agent (content gaps)
- visual-intelligence-agent (visual performance)

## Rules

- Recommendations must be specific and actionable
- Cite data from analytics_snapshots, not assumptions
