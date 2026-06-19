"""Post selection workflow state in SQLite."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "marketing.db"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def migrate(conn: sqlite3.Connection | None = None) -> None:
    own = conn is None
    conn = conn or connect()
    cols = {r[1] for r in conn.execute("PRAGMA table_info(daily_post_options)")}
    if "carousel_dir" not in cols:
        conn.execute("ALTER TABLE daily_post_options ADD COLUMN carousel_dir TEXT")
    if "selected_at" not in cols:
        conn.execute("ALTER TABLE daily_post_options ADD COLUMN selected_at TEXT")
    if own:
        conn.commit()
        conn.close()


def get_option(option_num: int, batch_date: str | None = None) -> sqlite3.Row | None:
    migrate()
    conn = connect()
    if batch_date:
        row = conn.execute(
            """SELECT * FROM daily_post_options
               WHERE batch_date = ? AND option_num = ?""",
            (batch_date, option_num),
        ).fetchone()
    else:
        row = conn.execute(
            """SELECT * FROM daily_post_options
               WHERE option_num = ? AND status IN ('pending', 'selected', 'carousel_ready')
               ORDER BY batch_date DESC LIMIT 1""",
            (option_num,),
        ).fetchone()
    conn.close()
    return row


def get_selected() -> sqlite3.Row | None:
    migrate()
    conn = connect()
    row = conn.execute(
        """SELECT * FROM daily_post_options
           WHERE status IN ('selected', 'carousel_ready')
           ORDER BY selected_at DESC LIMIT 1"""
    ).fetchone()
    conn.close()
    return row


def select_option(option_num: int) -> dict:
    migrate()
    conn = connect()
    row = conn.execute(
        """SELECT * FROM daily_post_options
           WHERE option_num = ? AND status IN ('pending', 'selected', 'carousel_ready')
           ORDER BY batch_date DESC LIMIT 1""",
        (option_num,),
    ).fetchone()
    if not row:
        conn.close()
        return {"success": False, "error": f"No active option {option_num}"}

    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """UPDATE daily_post_options SET status = 'skipped'
           WHERE batch_date = ? AND id != ? AND status IN ('selected', 'carousel_ready')""",
        (row["batch_date"], row["id"]),
    )
    conn.execute(
        """UPDATE daily_post_options SET status = 'selected', selected_at = ?
           WHERE id = ?""",
        (now, row["id"]),
    )
    conn.commit()
    conn.close()
    return {
        "success": True,
        "option_num": option_num,
        "hook": row["hook"],
        "batch_date": row["batch_date"],
        "body_preview": row["body"][:280] + ("..." if len(row["body"]) > 280 else ""),
        "next_steps": "Reply *carousel* to generate slides, then *publish* to post on LinkedIn.",
    }


def mark_carousel_ready(option_id: int, carousel_dir: str) -> None:
    migrate()
    conn = connect()
    conn.execute(
        """UPDATE daily_post_options SET status = 'carousel_ready', carousel_dir = ?
           WHERE id = ?""",
        (carousel_dir, option_id),
    )
    conn.commit()
    conn.close()


def mark_published(option_id: int, linkedin_post_id: str) -> None:
    migrate()
    conn = connect()
    now = datetime.now(timezone.utc).isoformat()
    row = conn.execute("SELECT batch_date FROM daily_post_options WHERE id = ?", (option_id,)).fetchone()
    conn.execute(
        """UPDATE daily_post_options SET status = 'published', linkedin_post_id = ?,
           slack_approved_at = ?, published_at = ? WHERE id = ?""",
        (linkedin_post_id, now, now, option_id),
    )
    if row:
        conn.execute(
            """UPDATE daily_post_options SET status = 'skipped'
               WHERE batch_date = ? AND id != ? AND status IN ('pending', 'selected', 'carousel_ready')""",
            (row["batch_date"], option_id),
        )
    conn.commit()
    conn.close()


def idea_dict_from_row(row: sqlite3.Row) -> dict:
    conn = connect()
    idea = None
    if row["idea_id"]:
        idea = conn.execute("SELECT * FROM content_ideas WHERE id = ?", (row["idea_id"],)).fetchone()
    conn.close()
    return {
        "id": row["idea_id"] or row["option_num"],
        "pillar": row["pillar"],
        "post_type": row["post_type"],
        "hook": row["hook"],
        "source_type": (dict(idea)["source_type"] if idea else "research"),
        "body": row["body"],
        "option_id": row["id"],
        "option_num": row["option_num"],
    }
