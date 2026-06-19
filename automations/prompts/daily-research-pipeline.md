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
   - Ensure at least 3 pending content ideas (40% research, 40% founder, 20% building)
   - Insert into content_ideas with status pending
   - Do not duplicate existing hooks

4. RUN PIPELINE
   - Execute: python scripts/run_daily_pipeline.py
   - Generates 3 LinkedIn options (Founder Voice v1.0):
     • Default 180–300 words (most days)
     • Short 80–150 words (quick observations)
     • Deep 300–500 words (research / building — rare)
     • Never exceed 500 words

5. SLACK — POST OPTIONS ONLY
   - Use Send to Slack to post to #marketing-os
   - Post the full slack_message from post_options (NOT the long daily digest)
   - Include at top: founders count + pending ideas count (one line KPIs)
   - End with: Reply *approve 1*, *approve 2*, or *approve 3* to publish to LinkedIn

Rules:
- Never sound like AI hype
- Do NOT publish without user replying `publish` in Slack
- Read `.cursor/rules/founder-voice.mdc` before writing or posting
- Morning options end with: `select 1|2|3` → `carousel` (optional) → `publish`
- Founder intelligence is primary KPI (target: 100 founders)

Primary action: run python scripts/run_daily_pipeline.py first, then post post_options.slack_message to Slack.
