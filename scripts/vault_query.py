#!/usr/bin/env python3
"""CLI for querying and inserting into the Marketing OS vault."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"

TABLES = [
    "raw_sources",
    "research_insights",
    "founders",
    "founder_intelligence",
    "decision_patterns",
    "strategic_questions",
    "product_requirements",
    "feature_hypotheses",
    "category_narratives",
    "competitor_intel",
    "content_ideas",
    "content_drafts",
    "content_scores",
    "design_scores",
    "visual_patterns",
    "published_posts",
    "analytics_snapshots",
    "founder_outreach",
]


def connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        print("Database not found. Run: python scripts/init_db.py", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict]:
    return [dict(row) for row in rows]


def _print_row(row: sqlite3.Row) -> None:
    text = json.dumps(dict(row), default=str, ensure_ascii=True)
    print(text)


def cmd_list(args: argparse.Namespace) -> None:
    conn = connect()
    table = args.table
    if table not in TABLES:
        print(f"Unknown table: {table}", file=sys.stderr)
        sys.exit(1)

    query = f"SELECT * FROM {table}"
    params: list = []
    conditions = []

    if args.status and table in ("content_ideas", "founder_outreach", "product_requirements"):
        conditions.append("status = ?")
        params.append(args.status)
    if args.limit:
        pass
    else:
        args.limit = 20

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += f" ORDER BY id DESC LIMIT {int(args.limit)}"

    rows = conn.execute(query, params).fetchall()
    conn.close()

    if args.json:
        print(json.dumps(rows_to_dicts(rows), indent=2, default=str, ensure_ascii=True))
    else:
        for row in rows:
            _print_row(row)


def cmd_get(args: argparse.Namespace) -> None:
    conn = connect()
    row = conn.execute(
        f"SELECT * FROM {args.table} WHERE id = ?", (args.id,)
    ).fetchone()
    conn.close()
    if not row:
        print(f"No row id={args.id} in {args.table}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(dict(row), indent=2, default=str))


def cmd_stats(args: argparse.Namespace) -> None:
    conn = connect()
    stats = {
        "founders": conn.execute("SELECT COUNT(*) FROM founders").fetchone()[0],
        "founder_intelligence": conn.execute(
            "SELECT COUNT(*) FROM founder_intelligence"
        ).fetchone()[0],
        "decision_patterns": conn.execute(
            "SELECT COUNT(*) FROM decision_patterns"
        ).fetchone()[0],
        "strategic_questions": conn.execute(
            "SELECT COUNT(*) FROM strategic_questions"
        ).fetchone()[0],
        "content_ideas_pending": conn.execute(
            "SELECT COUNT(*) FROM content_ideas WHERE status = 'pending'"
        ).fetchone()[0],
        "raw_sources_unprocessed": conn.execute(
            "SELECT COUNT(*) FROM raw_sources WHERE processed = 0"
        ).fetchone()[0],
        "visual_patterns": conn.execute(
            "SELECT COUNT(*) FROM visual_patterns"
        ).fetchone()[0],
    }
    conn.close()
    print(json.dumps(stats, indent=2))


def cmd_insert(args: argparse.Namespace) -> None:
    conn = connect()
    data = json.loads(args.data)
    cols = ", ".join(data.keys())
    placeholders = ", ".join("?" for _ in data)
    cur = conn.execute(
        f"INSERT INTO {args.table} ({cols}) VALUES ({placeholders})",
        list(data.values()),
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    print(json.dumps({"id": row_id, "table": args.table}))


def main() -> None:
    parser = argparse.ArgumentParser(description="Hustronix Marketing OS vault CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List rows from a table")
    p_list.add_argument("table", choices=TABLES)
    p_list.add_argument("--status", help="Filter by status")
    p_list.add_argument("--limit", type=int, default=20)
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_get = sub.add_parser("get", help="Get row by id")
    p_get.add_argument("table", choices=TABLES)
    p_get.add_argument("id", type=int)
    p_get.set_defaults(func=cmd_get)

    p_stats = sub.add_parser("stats", help="Vault KPI summary")
    p_stats.set_defaults(func=cmd_stats)

    p_insert = sub.add_parser("insert", help="Insert JSON row")
    p_insert.add_argument("table", choices=TABLES)
    p_insert.add_argument("data", help="JSON object string")
    p_insert.set_defaults(func=cmd_insert)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
