#!/usr/bin/env python3
"""Generate daily digest report (fallback when Slack MCP unavailable)."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"
REPORTS = ROOT / "analytics" / "reports"


def main() -> None:
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    stats = {
        "founders": conn.execute("SELECT COUNT(*) FROM founders").fetchone()[0],
        "pending_ideas": conn.execute(
            "SELECT COUNT(*) FROM content_ideas WHERE status = 'pending'"
        ).fetchone()[0],
        "unprocessed_sources": conn.execute(
            "SELECT COUNT(*) FROM raw_sources WHERE processed = 0"
        ).fetchone()[0],
    }

    ideas = conn.execute(
        "SELECT id, pillar, post_type, hook, source_type FROM content_ideas WHERE status = 'pending' LIMIT 5"
    ).fetchall()

    questions = conn.execute(
        "SELECT question, times_seen FROM strategic_questions ORDER BY times_seen DESC LIMIT 5"
    ).fetchall()

    lines = [
        f"# Daily Digest — {date}\n",
        "## Vault KPIs",
        f"- Founders: {stats['founders']} / 100 target",
        f"- Pending ideas: {stats['pending_ideas']}",
        f"- Unprocessed sources: {stats['unprocessed_sources']}\n",
        "## Pending Content Ideas\n",
    ]
    for idea in ideas:
        lines.append(
            f"- **#{idea['id']}** [{idea['post_type']}] {idea['hook'][:80]}... "
            f"({idea['source_type']})"
        )
        lines.append(f"  → Approve: `python scripts/approve_idea.py {idea['id']}`\n")

    lines.append("## Trending Strategic Questions\n")
    for q in questions:
        lines.append(f"- {q['question']} (seen {q['times_seen']}x)")

    lines.append("\n## Actions\n")
    lines.append("- Review ideas above (< 10 min)")
    lines.append("- Run `python scripts/approve_idea.py {id}` for top pick")
    lines.append("- Log founder conversations after calls\n")

    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / f"daily-digest-{date}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    conn.close()
    print(f"Digest written to {path}")


if __name__ == "__main__":
    main()
