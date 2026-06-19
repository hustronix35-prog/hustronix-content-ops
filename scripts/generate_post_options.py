#!/usr/bin/env python3
"""Generate 3 short LinkedIn post options for Slack approval."""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"
sys.path.insert(0, str(ROOT / "scripts"))
from lib.linkedin_posts import LENGTH_TIERS, pick_tiers_for_batch, post_from_idea  # noqa: E402


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def pick_ideas(conn: sqlite3.Connection, limit: int = 3) -> list[sqlite3.Row]:
    pending = conn.execute(
        """SELECT * FROM content_ideas WHERE status = 'pending'
           ORDER BY id DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    if len(pending) >= limit:
        return list(pending[:limit])

    extra = conn.execute(
        """SELECT * FROM content_ideas WHERE status IN ('pending', 'scored', 'approved')
           ORDER BY id DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    seen = {r["id"] for r in pending}
    merged = list(pending)
    for row in extra:
        if row["id"] not in seen and len(merged) < limit:
            merged.append(row)
            seen.add(row["id"])
    return merged[:limit]


def format_slack_message(batch_date: str, options: list[dict]) -> str:
    lines = [
        f"*Daily LinkedIn options — {batch_date}*",
        "",
        "Pick one, then follow the steps below:",
        "",
        "1. *select 1*  |  *select 2*  |  *select 3*  — choose your post",
        "2. *carousel* — generate brand slides (optional, sent to this channel)",
        "3. *publish* — post text (+ carousel if generated) to LinkedIn",
        "",
    ]
    for opt in options:
        lines.extend(
            [
                f"---",
                f"*OPTION {opt['option_num']}* — [{opt['post_type']}] {opt['pillar']} · {opt['tier_label']} ({opt['word_count']}w)",
                f"_{opt['hook']}_",
                "",
                opt["body"],
                "",
            ]
        )
    return "\n".join(lines)


def generate(batch_date: str | None = None) -> dict:
    batch_date = batch_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    import subprocess

    subprocess.run([sys.executable, str(ROOT / "scripts" / "init_db.py")], check=False)

    conn = connect()

    conn.execute(
        "DELETE FROM daily_post_options WHERE batch_date = ? AND status IN ('pending', 'expired')",
        (batch_date,),
    )

    ideas = pick_ideas(conn)
    if not ideas:
        conn.close()
        return {"batch_date": batch_date, "options": [], "slack_message": "No pending ideas in vault."}

    idea_dicts = [dict(i) for i in ideas[:3]]
    tiers = pick_tiers_for_batch(conn, idea_dicts)

    options = []
    for i, (idea, tier) in enumerate(zip(ideas[:3], tiers), start=1):
        generated = post_from_idea(dict(idea), tier)
        body = generated["body"]
        conn.execute(
            """INSERT INTO daily_post_options
               (batch_date, option_num, idea_id, pillar, post_type, hook, body, char_count, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')""",
            (
                batch_date,
                i,
                idea["id"],
                idea["pillar"],
                idea["post_type"],
                idea["hook"],
                body,
                generated["word_count"],
            ),
        )
        options.append(
            {
                "option_num": i,
                "idea_id": idea["id"],
                "pillar": idea["pillar"],
                "post_type": idea["post_type"],
                "hook": idea["hook"],
                "body": body,
                "word_count": generated["word_count"],
                "length_tier": tier,
                "tier_label": generated["tier_label"],
                "tier_hint": LENGTH_TIERS[tier]["slack_hint"],
            }
        )

    conn.commit()
    conn.close()

    slack_message = format_slack_message(batch_date, options)
    out_path = ROOT / "analytics" / "reports" / f"post-options-{batch_date}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(slack_message, encoding="utf-8")

    return {
        "batch_date": batch_date,
        "options": options,
        "slack_message": slack_message,
        "report_path": str(out_path),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="JSON only (for pipeline)")
    args = parser.parse_args()

    result = generate()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps({**result, "slack_message": result["slack_message"][:500] + "..."}, indent=2))
        print("\n--- SLACK MESSAGE ---\n")
        print(result["slack_message"])


if __name__ == "__main__":
    main()
