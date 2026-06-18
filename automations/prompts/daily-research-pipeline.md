You are running the Hustronix Marketing OS daily pipeline in repo hustronix35-prog/marketing-os on branch master.

Read these project rules first:
- .cursor/rules/hustronix-brand.mdc
- Skills in .cursor/skills/

Run in order:

1. SOURCE INGESTION
   - Check raw_sources for processed=0 rows
   - If new URLs were added, ingest them via scripts/ingest_url.py

2. RESEARCH AGENT
   - Process unprocessed raw_sources
   - Extract insights into research_insights table
   - Write vault/insights/{date}.md
   - Extract decision_patterns where applicable

3. CONTENT STRATEGIST
   - Generate 3-5 content ideas
   - Enforce source mix: 40% research, 40% founder, 20% building Hustronix
   - Insert into content_ideas with status pending
   - Update review/queue.md

4. RUN PIPELINE SCRIPT
   - Execute: python scripts/run_daily_pipeline.py
   - Or: python scripts/daily_digest.py

5. SLACK SUMMARY
   - Use Send to Slack to post to #marketing-os with:
     • Vault KPIs (founders count, pending ideas, decision patterns)
     • List of pending ideas (id + hook)
     • Top strategic question by times_seen
     • Reminder: approve with "python scripts/approve_idea.py {id}"

Rules:
- Never sound like AI hype
- Never auto-publish content
- Founder intelligence is primary KPI (target: 100 founders)
- Do not duplicate existing hooks in content_ideas

Primary action: run python scripts/run_daily_pipeline.py first.
Post the contents of analytics/reports/daily-digest-{date}.md to Slack.
Do not manually rewrite ideas unless pending ideas < 3.
