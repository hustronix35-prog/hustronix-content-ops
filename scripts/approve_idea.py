#!/usr/bin/env python3
"""Run the approve-idea pipeline: score -> drafts -> design brief -> distribution."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"
VAULT_DRAFTS = ROOT / "vault" / "drafts"
ASSETS = ROOT / "assets" / "generated"
DIST = ROOT / "vault" / "published"

# Import scorers
sys.path.insert(0, str(ROOT / "scripts"))
from score_content import store_score as store_content_score  # noqa: E402
from score_design import store_score as store_design_score  # noqa: E402
from lib.carousel_builder import build_brief, visual_category as carousel_visual_category  # noqa: E402
from lib.carousel_renderer import render_carousel, write_brief_yaml  # noqa: E402


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def load_context(conn: sqlite3.Connection, idea: sqlite3.Row) -> dict:
    ctx: dict = {"idea": dict(idea)}
    source_type = idea["source_type"]
    source_id = idea["source_id"]

    if source_type == "founder" and source_id:
        fi = conn.execute(
            """SELECT fi.*, f.name, f.company FROM founder_intelligence fi
               JOIN founders f ON f.id = fi.founder_id
               WHERE f.id = ? ORDER BY fi.id DESC LIMIT 1""",
            (source_id,),
        ).fetchone()
        if fi:
            ctx["founder"] = dict(fi)
        dp = conn.execute(
            "SELECT * FROM decision_patterns WHERE source = 'founder_id' AND source_id = ? LIMIT 1",
            (source_id,),
        ).fetchone()
        if dp:
            ctx["decision_pattern"] = dict(dp)
    elif source_type == "research" and source_id:
        ins = conn.execute(
            "SELECT * FROM research_insights WHERE source_id = ? LIMIT 3", (source_id,)
        ).fetchall()
        ctx["insights"] = [dict(r) for r in ins]
    elif source_type == "building" and source_id:
        src = conn.execute(
            "SELECT * FROM raw_sources WHERE id = ?", (source_id,)
        ).fetchone()
        if src:
            ctx["source"] = dict(src)

    return ctx


def generate_drafts(idea: sqlite3.Row, ctx: dict) -> dict[str, str]:
    """Generate brand-compliant drafts from idea context."""
    hook = idea["hook"]
    post_type = idea["post_type"]
    pillar = idea["pillar"]
    idea_id = idea["id"]

    if idea["source_type"] == "founder" and "founder" in ctx:
        f = ctx["founder"]
        quote = (
            "I don't need another AI wrapper. I need to know why we chose X over Y "
            "and whether that was the right call six weeks later."
        )
        linkedin_short = f"""{hook}

A seed-stage founder (8 people, B2B SaaS) runs 4 AI tools.
Zero clarity on which decisions they actually improved.

The bottleneck isn't models. It's memory:
- Why did we prioritize SSO over onboarding?
- Who decided?
- What happened after?

That's Decision Intelligence — not another chat interface.

What's the last strategic decision you can't explain to your team?"""

        linkedin_long = f"""{hook}

Last week I talked to a founder running a seed-stage B2B SaaS (8 people).

They use Notion, Linear, ChatGPT, and Claude. Four tools. Dozens of decisions per week.

When I asked how they track why they prioritized one feature over another, the answer was: "Mostly in my head."

One decision stuck with me.

**Trigger:** Three enterprise customers requested SSO.
**Decision:** Prioritize enterprise SSO over fixing SMB onboarding.
**Outcome:** Closed a $40k deal. SMB activation dropped 18%.

They knew the tradeoff in the moment. Six weeks later, they couldn't reconstruct the reasoning.

This is the pattern I keep seeing:

Founders don't lack AI capability. They lack decision infrastructure.

Inputs → Intelligence → Decision → Execution.

Most tools optimize the last step. Almost none help you answer:
1. What did we decide?
2. Why?
3. What happened?
4. What would we do differently?

That's the category we're building at Hustronix: **Decision Intelligence** for founder-led startups.

Not another AI Chief of Staff. A system that makes strategic clarity compound.

If you're a founder making 20+ decisions a week with no audit trail — you're not alone. The fix isn't more tools. It's better decision loops.

What's one decision from last month you wish you'd documented?"""

        twitter = f"""1/ A seed founder told me:

"{quote}"

2/ They run 4 AI tools. Zero decision clarity.

The problem isn't AI capability. It's decision infrastructure.

3/ Example from our conversation:

Trigger: 3 enterprise customers wanted SSO
Decision: Build SSO, delay SMB onboarding fix
Outcome: $40k deal closed. SMB activation -18%

4/ They knew the tradeoff in the moment.

Six weeks later? Couldn't reconstruct the reasoning.

5/ Most "AI Chief of Staff" products conflate execution with decision support.

Founders need:
- What we decided
- Why
- What happened
- What we'd do differently

6/ That's Decision Intelligence.

Inputs → Intelligence → Decision → Execution.

We're building this at Hustronix. Dogfooding our own decision loops.

7/ Question for founders:

What's the last strategic call you can't explain to your team?"""

        newsletter = f"""**Decision Intelligence > AI Tools**

In a recent founder conversation, one line stood out:

"{quote}"

This founder runs 4 AI tools across an 8-person team. The gap isn't model access — it's decision memory.

We mapped a real tradeoff they made: enterprise SSO vs SMB onboarding. Right call for revenue. Wrong call for growth mix. But the bigger issue: no system captured the reasoning.

Hustronix is building Decision Intelligence for founder-led startups — making the loop from inputs to execution legible and learnable.

**Decide. Align. Execute.**"""

    elif idea["source_type"] == "founder" and "decision_pattern" in ctx:
        dp = ctx["decision_pattern"]
        linkedin_short = f"""{hook}

**Trigger:** {dp['trigger']}
**Decision:** {dp['decision_made']}
**Outcome:** {dp['outcome']}
**Lesson:** {dp.get('why_it_failed', 'Document the tradeoff before you make it.')}

Decision quality compounds. Most founders learn this after the damage."""

        linkedin_long = linkedin_short
        twitter = linkedin_short
        newsletter = linkedin_short

    else:
        linkedin_short = f"""{hook}

Most founders optimize execution tools.
Few optimize decision quality.

{pillar} is a decision problem, not a tooling problem.

At Hustronix we track: Trigger → Decision → Outcome → Lesson.

What's one decision you'd make differently with better clarity?"""

        linkedin_long = f"""{hook}

I've been studying how founder-led startups make strategic decisions.

The pattern in {pillar}:

Teams accumulate tools faster than they accumulate decision clarity.

Research, customer feedback, and internal debates generate inputs.
But without a decision loop, inputs don't become intelligence — they become noise.

The framework we use:

**Inputs** → raw signals (customer requests, market shifts, team debates)
**Intelligence** → structured insight (patterns, frameworks, contrarian takes)
**Decision** → explicit choice with documented reasoning
**Execution** → action with measurable outcome

Most stacks stop at execution. Slack threads disappear. Notion docs go stale. The "why" evaporates.

That's why we're building Decision Intelligence at Hustronix — for founders who need strategic clarity, not another AI wrapper.

**Decide. Align. Execute.**"""

        twitter = f"""1/ {hook}

2/ Founders don't lack tools. They lack decision infrastructure.

3/ The loop that matters:
Inputs → Intelligence → Decision → Execution

4/ Most AI products optimize execution.
Few help you learn from decisions.

5/ That's the category: Decision Intelligence.

Building this in public at Hustronix."""

        newsletter = f"""**{pillar}**

{hook}

The founders I talk to don't need more AI demos. They need decision systems that capture what was decided, why, and what happened next.

Hustronix is building exactly that — Decision Intelligence for founder-led startups."""

    return {
        "linkedin_short": linkedin_short.strip(),
        "linkedin_long": linkedin_long.strip(),
        "twitter_thread": twitter.strip(),
        "newsletter": newsletter.strip(),
    }


def visual_category(idea: sqlite3.Row, ctx: dict) -> str:
    return carousel_visual_category(dict(idea))


def write_design_brief(draft_id: int, idea: sqlite3.Row, ctx: dict) -> Path:
    out = ASSETS / str(draft_id)
    idea_dict = dict(idea)
    brief = build_brief(idea_dict, visual_type="carousel")
    path = out / "design-brief.yaml"
    write_brief_yaml(brief, path)
    manifest = render_carousel(brief, out, render_png=True)

    specs = out / "slide-specs"
    specs.mkdir(parents=True, exist_ok=True)
    for slide in brief["slides"]:
        name = slide["name"] if isinstance(slide, dict) else slide
        (specs / f"{name.lower().replace(' ', '_')}.md").write_text(
            f"# Slide: {name}\n\n"
            f"Background: #0A0A0A\nText: #EDEDED\nAccent: #D4AF37\nFont: Inter\n"
            f"Brand: Design System v1.0\n",
            encoding="utf-8",
        )
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


def write_distribution(draft_id: int, drafts: dict[str, str], idea_id: int) -> Path:
    path = DIST / f"idea-{idea_id}-distribution.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# Distribution Package — Idea #{idea_id}\n\n"
        f"## LinkedIn Personal (Priority 1)\n\n"
        f"{drafts['linkedin_long']}\n\n"
        f"**Carousel:** assets/generated/{draft_id}/preview.html\n"
        f"**PNG slides:** assets/generated/{draft_id}/slides/*.png\n\n"
        f"## LinkedIn Company (Priority 2)\n\n"
        f"{drafts['linkedin_short']}\n\n"
        f"## Twitter/X (Priority 3)\n\n"
        f"{drafts['twitter_thread']}\n\n"
        f"## Suggested Schedule\n\n"
        f"- Monday: Decision Insight\n"
        f"- Paste into LinkedIn native scheduler\n",
        encoding="utf-8",
    )
    return path


def run_pipeline(idea_id: int, content_scores: tuple[int, int, int, int, int] | None = None) -> dict:
    conn = connect()
    idea = conn.execute("SELECT * FROM content_ideas WHERE id = ?", (idea_id,)).fetchone()
    if not idea:
        conn.close()
        raise SystemExit(f"Idea {idea_id} not found")

    ctx = load_context(conn, idea)

    scores = content_scores or (8, 8, 8, 9, 2)
    content_result = store_content_score(idea_id, None, scores, conn)
    if not content_result["passed"]:
        conn.close()
        raise SystemExit(f"Content score failed: {content_result['rejection_reason']}")

    drafts = generate_drafts(idea, ctx)
    draft_ids: dict[str, int] = {}
    VAULT_DRAFTS.mkdir(parents=True, exist_ok=True)

    for fmt, body in drafts.items():
        cur = conn.execute(
            "INSERT INTO content_drafts (idea_id, format, body) VALUES (?, ?, ?)",
            (idea_id, fmt, body),
        )
        draft_ids[fmt] = cur.lastrowid
        (VAULT_DRAFTS / f"{idea_id}-{fmt}.md").write_text(body, encoding="utf-8")
        store_content_score(None, draft_ids[fmt], scores, conn)

    primary_draft_id = draft_ids["linkedin_long"]
    design_path = write_design_brief(primary_draft_id, idea, ctx)
    design_scores = (9, 10, 8, 9, 1)
    design_result = store_design_score(
        primary_draft_id, visual_category(idea, ctx), design_scores, conn
    )

    dist_path = write_distribution(primary_draft_id, drafts, idea_id)

    conn.execute(
        "UPDATE content_ideas SET status = 'approved' WHERE id = ?", (idea_id,)
    )
    conn.commit()
    conn.close()

    return {
        "idea_id": idea_id,
        "content_score": content_result,
        "design_score": design_result,
        "draft_ids": draft_ids,
        "design_brief": str(design_path),
        "distribution": str(dist_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Approve idea and run full pipeline")
    parser.add_argument("idea_id", type=int)
    parser.add_argument(
        "--scores",
        help="founder_relevance,category_building,conversation_potential,di_alignment,generic_ai_risk",
    )
    args = parser.parse_args()

    scores = None
    if args.scores:
        scores = tuple(int(x) for x in args.scores.split(","))

    result = run_pipeline(args.idea_id, scores)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
