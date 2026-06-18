#!/usr/bin/env python3
"""Seed the vault with initial sources, founder interviews, and sample intelligence."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"

SOURCES = [
    {
        "source_type": "article",
        "source_url": "https://www.ycombinator.com/library/8F-how-to-start-a-startup",
        "title": "YC: How to Start a Startup — Decision Making Under Uncertainty",
        "content": """Paul Graham and YC partners emphasize that startup success depends less on ideas
and more on the quality of decisions founders make weekly. Key themes: talk to users before building,
prioritize learning speed over planning perfection, and recognize that most startup deaths come from
founders avoiding hard decisions (hiring too late, not firing fast enough, building without validation).
Decision quality compounds: small weekly choices about what to build, who to hire, and what to ignore
determine trajectory more than any single strategic plan.""",
        "tags": "yc,founder-context,decision-quality",
    },
    {
        "source_type": "article",
        "source_url": "https://openai.com/research",
        "title": "OpenAI: Agent Systems and Organizational Decision Infrastructure",
        "content": """OpenAI research direction increasingly points toward agent systems that can plan,
reason, and execute multi-step tasks. The gap in the market is not raw model capability but
organizational infrastructure: how decisions get made, recorded, and learned from when AI agents
participate in workflows. Enterprises struggle to move from AI demos to decision-grade systems
because they lack clarity on who decides, what context agents need, and how outcomes feed back.""",
        "tags": "openai,ai-native,organizational-learning",
    },
    {
        "source_type": "article",
        "source_url": "https://www.anthropic.com/research",
        "title": "Anthropic: Constitutional AI and Decision Safety in Agent Systems",
        "content": """Anthropic's research on safe AI systems highlights that agent reliability depends
on decision frameworks, not just model alignment. Organizations deploying AI agents need explicit
decision boundaries: what agents can decide autonomously vs what requires human judgment.
The emerging category of 'AI Chief of Staff' products often conflate task execution with
strategic decision support — a distinction founders must understand when evaluating tools.""",
        "tags": "anthropic,ai-native,decision-quality",
    },
    {
        "source_type": "article",
        "source_url": "https://www.lennysnewsletter.com",
        "title": "Lenny's Newsletter: How Top Founders Make Product Decisions",
        "content": """Top product leaders share a pattern: they separate signal from noise in customer
feedback, use lightweight decision frameworks (RICE, ICE, or custom), and document why decisions
were made so teams can learn when outcomes differ from expectations. The best founders treat
product prioritization as a decision quality problem, not a feature request queue. Vocal customers
often overweight the roadmap — a recurring failure mode.""",
        "tags": "podcast,product-strategy,decision-quality",
    },
    {
        "source_type": "article",
        "source_url": "https://www.latent.space",
        "title": "Latent Space: AI-Native Company Operating Models",
        "content": """AI-native companies operate differently: smaller teams, higher leverage per person,
agents handling operational loops, and founders spending more time on judgment calls than execution.
The bottleneck shifts from 'can we build it' to 'should we build it' and 'how do we know it worked.'
Decision intelligence — systematic capture of what was decided, why, and what happened — becomes
the competitive moat for AI-native organizations.""",
        "tags": "latent-space,ai-native,execution",
    },
    {
        "source_type": "article",
        "source_url": "https://hustronix.ai",
        "title": "Building Hustronix: Decision Intelligence as Category",
        "content": """Hustronix is building Decision Intelligence for founder-led startups.
The thesis: marketing, product, and operations all reduce to decision loops —
Inputs → Intelligence → Decision → Execution. Most tools optimize execution;
few help founders make better decisions and learn from outcomes. Building in public
means documenting our own decision patterns as we dogfood the framework.""",
        "tags": "building-hustronix,decision-intelligence",
    },
]

FOUNDER_INTERVIEWS = [
    {
        "name": "Alex Rivera",
        "company": "Stackline AI",
        "founder_stage": "seed",
        "company_size": "2-10",
        "industry": "B2B SaaS",
        "transcript": """Founder interview — Alex Rivera, Stackline AI (Seed, 8 people)

Pain: "We have 4 AI tools and zero clarity on what decisions they actually improved.
My team asks me the same strategic questions every week because nothing is documented."

Current stack: Notion, Linear, ChatGPT, Claude, Apollo

Decision process: "Mostly in my head. We have a weekly sync but decisions made in Slack
threads disappear. I can't tell if we're learning or just repeating mistakes."

Biggest friction: Prioritization. "Three enterprise customers asked for SSO last month.
We built it. Meanwhile our SMB onboarding is broken and that's where growth is."

Decision discussed: Prioritized enterprise SSO over SMB onboarding fix.
Outcome: Enterprise deal closed ($40k) but SMB activation dropped 18%.

Quote: "I don't need another AI wrapper. I need to know why we chose X over Y
and whether that was the right call six weeks later."

Product implications: Decision logging, outcome tracking, prioritization frameworks
that weight growth stage appropriately.""",
        "pain": "No decision documentation; AI tools without decision clarity",
        "strategic_question": "Should we prioritize feature X?",
        "decision_pattern": {
            "category": "Product Prioritization",
            "trigger": "3 enterprise customers requested SSO feature",
            "decision_made": "Prioritized enterprise SSO over SMB onboarding",
            "outcome": "Enterprise deal closed but SMB activation dropped 18%",
            "why_it_failed": "Overweighted vocal enterprise customers vs growth-stage SMB base",
        },
        "product_requirement": "Decision logging with outcome tracking tied to prioritization choices",
        "feature_hypothesis": "If we show founders decision→outcome history, they will reprioritize based on evidence not vocal customers",
    },
    {
        "name": "Morgan Lee",
        "company": "Clearpath Labs",
        "founder_stage": "pre-seed",
        "company_size": "solo",
        "industry": "Dev Tools",
        "transcript": """Founder interview — Morgan Lee, Clearpath Labs (Pre-seed, solo)

Pain: "I'm a solo founder making 20+ decisions a day with no one to pressure-test them.
By Friday I can't remember why I chose one approach over another on Monday."

Current stack: Cursor, GitHub, Linear, personal Notion

Decision process: "Gut feel + Twitter advice. I know that's bad but I don't have a system
lightweight enough for a solo founder."

Biggest friction: Hiring decision. "I need a founding engineer but can't tell if I should
hire now or stay solo until we hit $10k MRR."

Quote: "Every founder blog says 'hire slow' but nobody helps you decide WHEN.
That's the actual decision I'm stuck on."

Product implications: Solo-founder decision frameworks, lightweight decision journal,
strategic question templates for common founder forks.""",
        "pain": "Solo founder decision overload with no lightweight system",
        "strategic_question": "Should we hire?",
        "decision_pattern": None,
        "product_requirement": "Lightweight decision journal for solo founders with strategic question templates",
        "feature_hypothesis": "If we provide hire/no-hire decision frameworks with stage-appropriate criteria, solo founders will make faster confident hiring decisions",
    },
]

INSIGHTS = [
    (1, "Vocal customers overweight roadmaps — founders need decision frameworks that weight growth stage", "Decision Quality", 0.9),
    (2, "Agent capability exceeds organizational decision infrastructure in most startups", "AI Native Organizations", 0.85),
    (3, "AI Chief of Staff products conflate execution with strategic decision support", "Product Strategy", 0.8),
    (4, "Top founders document why decisions were made, not just what was decided", "Organizational Learning", 0.9),
    (5, "AI-native companies bottleneck on judgment calls, not build capacity", "Execution", 0.85),
    (6, "Decision Intelligence is the missing layer between AI tools and business outcomes", "Decision Quality", 0.9),
]


def write_raw_source_md(row_id: int, src: dict) -> None:
    path = ROOT / "vault" / "raw_sources" / f"{row_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# {src['title']}\n\n"
        f"- **URL:** {src.get('source_url', 'N/A')}\n"
        f"- **Tags:** {src.get('tags', '')}\n\n"
        f"## Content\n\n{src['content']}\n",
        encoding="utf-8",
    )


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for src in SOURCES:
        cur = conn.execute(
            """INSERT INTO raw_sources (source_type, source_url, title, content, date, tags, processed)
               VALUES (?, ?, ?, ?, ?, ?, 1)""",
            (src["source_type"], src["source_url"], src["title"], src["content"], date, src["tags"]),
        )
        write_raw_source_md(cur.lastrowid, src)

    for insight in INSIGHTS:
        conn.execute(
            """INSERT INTO research_insights (source_id, insight, category, confidence)
               VALUES (?, ?, ?, ?)""",
            insight,
        )

    insights_path = ROOT / "vault" / "insights" / f"{date}.md"
    insights_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# Research Insights — {date}\n"]
    for _, text, cat, conf in INSIGHTS:
        lines.append(f"## {cat} (confidence: {conf})\n\n{text}\n")
    insights_path.write_text("\n".join(lines), encoding="utf-8")

    for interview in FOUNDER_INTERVIEWS:
        cur = conn.execute(
            """INSERT INTO founders (name, company, founder_stage, company_size, industry,
               pain_points, interview_count, relationship_score, pilot_interest, first_contact_at, last_contact_at)
               VALUES (?, ?, ?, ?, ?, ?, 1, 60, 'curious', ?, ?)""",
            (
                interview["name"],
                interview["company"],
                interview["founder_stage"],
                interview["company_size"],
                interview["industry"],
                f'["{interview["pain"]}"]',
                date,
                date,
            ),
        )
        founder_id = cur.lastrowid

        interview_path = ROOT / "vault" / "founder_interviews" / f"{founder_id}-{interview['name'].replace(' ', '_')}.md"
        interview_path.write_text(interview["transcript"], encoding="utf-8")

        fi_cur = conn.execute(
            """INSERT INTO founder_intelligence
               (founder_id, conversation_date, pain, current_stack, decision_process,
                biggest_friction, interesting_quotes, product_implications, content_angles)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                founder_id,
                date,
                interview["pain"],
                interview.get("current_stack", "See transcript"),
                "See transcript",
                interview["pain"],
                interview["transcript"].split("Quote:")[-1].strip() if "Quote:" in interview["transcript"] else "",
                interview.get("product_requirement", ""),
                f"Founder decision bottleneck: {interview['strategic_question']}",
            ),
        )
        fi_id = fi_cur.lastrowid

        fi_md = ROOT / "vault" / "founder_intelligence" / f"{founder_id}-{date}.md"
        fi_md.write_text(
            f"# Founder Intelligence — {interview['name']}\n\n"
            f"**Pain:** {interview['pain']}\n\n"
            f"**Product implications:** {interview.get('product_requirement', '')}\n",
            encoding="utf-8",
        )

        sq = conn.execute(
            "SELECT id, times_seen FROM strategic_questions WHERE question = ? AND founder_id IS NULL",
            (interview["strategic_question"],),
        ).fetchone()
        if sq:
            conn.execute(
                """INSERT INTO strategic_questions
                   (question, category, founder_id, founder_intelligence_id, context, status, times_seen)
                   VALUES (?, (SELECT category FROM strategic_questions WHERE id = ?), ?, ?, ?, 'open', 1)""",
                (interview["strategic_question"], sq[0], founder_id, fi_id, interview["pain"][:200]),
            )
            conn.execute(
                "UPDATE strategic_questions SET times_seen = times_seen + 1, updated_at = datetime('now') WHERE id = ?",
                (sq[0],),
            )

        if interview.get("decision_pattern"):
            dp = interview["decision_pattern"]
            dp_cur = conn.execute(
                """INSERT INTO decision_patterns
                   (category, trigger, decision_made, outcome, why_it_failed, source, source_id, confidence)
                   VALUES (?, ?, ?, ?, ?, 'founder_id', ?, 0.85)""",
                (
                    dp["category"],
                    dp["trigger"],
                    dp["decision_made"],
                    dp["outcome"],
                    dp.get("why_it_failed"),
                    founder_id,
                ),
            )
            dp_id = dp_cur.lastrowid
            dp_md = ROOT / "vault" / "decision_patterns" / f"{dp_id}.md"
            dp_md.write_text(
                f"# Decision Pattern #{dp_id}\n\n"
                f"**Category:** {dp['category']}\n"
                f"**Trigger:** {dp['trigger']}\n"
                f"**Decision:** {dp['decision_made']}\n"
                f"**Outcome:** {dp['outcome']}\n"
                f"**Lesson:** {dp.get('why_it_failed', '')}\n",
                encoding="utf-8",
            )

        pr_cur = conn.execute(
            """INSERT INTO product_requirements
               (founder_intelligence_id, founder_id, requirement, pain_evidence, priority, status)
               VALUES (?, ?, ?, ?, 'high', 'hypothesis')""",
            (fi_id, founder_id, interview["product_requirement"], interview["pain"]),
        )
        pr_id = pr_cur.lastrowid
        conn.execute(
            """INSERT INTO feature_hypotheses
               (product_requirement_id, hypothesis, validation_method, status)
               VALUES (?, ?, 'Founder interview validation', 'untested')""",
            (pr_id, interview["feature_hypothesis"]),
        )
        pi_md = ROOT / "vault" / "product_insights" / f"{pr_id}.md"
        pi_md.write_text(
            f"# Product Insight #{pr_id}\n\n"
            f"**Requirement:** {interview['product_requirement']}\n\n"
            f"**Hypothesis:** {interview['feature_hypothesis']}\n",
            encoding="utf-8",
        )

    ideas = [
        ("Decision Quality", "Framework", "Vocal customers hijack your roadmap. Here's the decision framework top founders use.", "founder", 1),
        ("Founder Context", "Interview", "A Series A founder told me: 'I don't need another AI wrapper. I need to know why we chose X over Y.'", "founder", 1),
        ("Decision Quality", "Contrarian", "Your AI stack is not your problem. Your decision infrastructure is.", "research", 2),
        ("AI Native Organizations", "Research", "AI-native companies don't fail on build speed. They fail on judgment calls.", "research", 5),
        ("Building Hustronix", "Builder", "We're building Decision Intelligence by dogfooding our own decision loops.", "building", 6),
    ]
    queue_lines = ["# Review Queue\n\nPending content ideas.\n"]
    for pillar, post_type, hook, source_type, source_id in ideas:
        cur = conn.execute(
            """INSERT INTO content_ideas (pillar, post_type, hook, source_type, source_id, status)
               VALUES (?, ?, ?, ?, ?, 'pending')""",
            (pillar, post_type, hook, source_type, source_id),
        )
        idea_id = cur.lastrowid
        queue_lines.append(
            f"### Idea #{idea_id} — {post_type}\n"
            f"- **Pillar:** {pillar}\n"
            f"- **Source:** {source_type} (id: {source_id})\n"
            f"- **Hook:** {hook}\n"
            f"- **Status:** pending\n"
        )

    (ROOT / "review" / "queue.md").write_text("\n".join(queue_lines), encoding="utf-8")

    for name, category, layout in [
        ("decision_pattern_vertical_v1", "decision_pattern", "Trigger → Decision → Outcome → Lesson"),
        ("strategic_question_minimal_v1", "strategic_question", "Large Inter Bold question centered"),
        ("founder_insight_quote_v1", "founder_insight", "Large quote + small framework"),
    ]:
        yaml_path = ROOT / "vault" / "visual_patterns" / f"{name}.yaml"
        yaml_path.write_text(
            f"pattern:\n  name: {name}\n  category: {category}\n  performance: 0.0\n  times_used: 0\n  layout_spec: \"{layout}\"\n  examples: []\n",
            encoding="utf-8",
        )

    conn.commit()
    conn.close()
    print("Seed complete: 6 sources, 6 insights, 2 founders, 5 content ideas")


if __name__ == "__main__":
    main()
