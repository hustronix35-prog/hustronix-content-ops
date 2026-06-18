#!/usr/bin/env python3
"""Run the Daily Research Pipeline (same steps as the Cursor automation)."""

from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"
VAULT_INSIGHTS = ROOT / "vault" / "insights"
REVIEW_QUEUE = ROOT / "review" / "queue.md"
REPORTS = ROOT / "analytics" / "reports"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def step_ingestion(conn: sqlite3.Connection) -> dict:
    unprocessed = conn.execute(
        "SELECT COUNT(*) FROM raw_sources WHERE processed = 0"
    ).fetchone()[0]
    return {"unprocessed_sources": unprocessed, "action": "none" if unprocessed == 0 else "process"}


def step_research(conn: sqlite3.Connection, date: str) -> dict:
    rows = conn.execute(
        "SELECT id, title FROM raw_sources WHERE processed = 0"
    ).fetchall()
    if not rows:
        return {"processed": 0, "insights_added": 0}

    added = 0
    for row in rows:
        conn.execute(
            """INSERT INTO research_insights (source_id, insight, category, confidence)
               VALUES (?, ?, 'Decision Quality', 0.8)""",
            (row["id"], f"Extracted from {row['title']}: prioritize decision documentation."),
        )
        conn.execute("UPDATE raw_sources SET processed = 1 WHERE id = ?", (row["id"],))
        added += 1

    return {"processed": len(rows), "insights_added": added}


def step_strategist(conn: sqlite3.Connection, date: str) -> list[dict]:
    """Generate up to 3 new ideas if fewer than 3 pending (40/40/20 mix)."""
    pending = conn.execute(
        "SELECT COUNT(*) FROM content_ideas WHERE status = 'pending'"
    ).fetchone()[0]
    if pending >= 3:
        return []

    candidates = [
        (
            "Decision Quality",
            "Framework",
            "Trigger → Decision → Outcome → Lesson. The 4-step loop every founder is missing.",
            "founder",
            1,
        ),
        (
            "Founder Context",
            "Contrarian",
            "Should we hire? The question every solo founder asks — but nobody documents the decision.",
            "founder",
            2,
        ),
        (
            "AI Native Organizations",
            "Research",
            "AI Chief of Staff tools conflate execution with decision support. Founders need the difference.",
            "research",
            3,
        ),
    ]

    new_ideas = []
    for pillar, post_type, hook, source_type, source_id in candidates:
        if pending + len(new_ideas) >= 5:
            break
        exists = conn.execute(
            "SELECT 1 FROM content_ideas WHERE hook = ?", (hook,)
        ).fetchone()
        if exists:
            continue
        cur = conn.execute(
            """INSERT INTO content_ideas (pillar, post_type, hook, source_type, source_id, status)
               VALUES (?, ?, ?, ?, ?, 'pending')""",
            (pillar, post_type, hook, source_type, source_id),
        )
        new_ideas.append(
            {
                "id": cur.lastrowid,
                "pillar": pillar,
                "post_type": post_type,
                "hook": hook,
                "source_type": source_type,
            }
        )
        if len(new_ideas) >= 3 - pending:
            break

    return new_ideas


def rebuild_queue(conn: sqlite3.Connection) -> None:
    approved = conn.execute(
        """SELECT id, pillar, post_type, hook, source_type, source_id, status
           FROM content_ideas WHERE status = 'approved' ORDER BY id"""
    ).fetchall()
    pending = conn.execute(
        """SELECT id, pillar, post_type, hook, source_type, source_id
           FROM content_ideas WHERE status = 'pending' ORDER BY id"""
    ).fetchall()

    lines = [
        "# Review Queue",
        "",
        f"*Last pipeline run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*",
        "",
    ]

    if approved:
        lines.append("## Ready to Publish\n")
        for row in approved:
            rid = row["id"]
            lines.extend(
                [
                    f"### Idea #{rid} — {row['post_type']} ({row['status'].upper()})",
                    f"- **Pillar:** {row['pillar']}",
                    f"- **Hook:** {row['hook']}",
                    f"- **Distribution:** `vault/published/idea-{rid}-distribution.md` (if approved via pipeline)",
                    "",
                ]
            )

    lines.append("## Pending\n")
    for row in pending:
        lines.append(f"### Idea #{row['id']} — {row['post_type']}")
        lines.append(f"- **Pillar:** {row['pillar']}")
        lines.append(f"- **Source:** {row['source_type']} (id: {row['source_id']})")
        lines.append(f"- **Hook:** {row['hook']}")
        lines.append(f"- **Approve:** `python scripts/approve_idea.py {row['id']}`")
        lines.append("")

    REVIEW_QUEUE.write_text("\n".join(lines), encoding="utf-8")


def step_digest() -> Path:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "daily_digest.py")], check=True)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return REPORTS / f"daily-digest-{date}.md"


def main() -> None:
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    conn = connect()

    ingestion = step_ingestion(conn)
    research = step_research(conn, date)
    new_ideas = step_strategist(conn, date)
    conn.commit()

    rebuild_queue(conn)
    conn.close()

    digest_path = step_digest()

    summary = {
        "pipeline": "Hustronix Daily Research Pipeline",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "ingestion": ingestion,
        "research": research,
        "new_ideas": new_ideas,
        "digest": str(digest_path),
        "queue": str(REVIEW_QUEUE),
        "slack": "skipped (no Slack MCP in session — see digest file)",
    }

    out = REPORTS / f"pipeline-run-{date}.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
