---
name: analytics-agent
description: Weekly analytics report from metrics.csv and published posts. Use Monday 10am or when user says run weekly report.
---

# Analytics Agent

Runs weekly after founder pastes LinkedIn metrics (~5 min manual).

## Input

1. `analytics/metrics.csv` — update with weekly LinkedIn numbers
2. `published_posts` table
3. `analytics_snapshots` (insert new rows from CSV)

## Metrics to Track

- Impressions, likes, comments, reposts
- Followers delta, profile visits, website clicks
- Founder interactions (note in CSV notes column)

## Procedure

1. Read metrics.csv
2. Insert/update `analytics_snapshots` per post
3. Calculate week-over-week deltas
4. Identify top/bottom performing posts by engagement rate

## Output

`analytics/reports/weekly-{YYYY-MM-DD}.md`:

```markdown
# Weekly Analytics — {date}

## Summary
- Posts published: N
- Total impressions: N
- Follower delta: +N

## Top Performers
1. {post} — {impressions} impressions, {comments} comments

## Bottom Performers
...

## By Content Type
- Founder-sourced vs research vs building

## Founder Interactions
- Notable founder comments/DMs
```

Post summary to Slack `#marketing-os`.

## Rules

- Secondary KPI: followers (primary is founder intelligence DB)
- Correlate performance with source_type and post_type
