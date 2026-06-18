#!/usr/bin/env python3
"""V2 bridge: export Marketing OS insights to Hustronix OS-compatible JSON."""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"
EXPORT_DIR = ROOT / "exports" / "hustronix_bridge"


def export_signals(conn: sqlite3.Connection) -> dict:
    """Export insights as external_signals-compatible payloads."""
    signals = []

    for row in conn.execute(
        "SELECT id, insight, category, confidence, created_at FROM research_insights ORDER BY id DESC LIMIT 50"
    ):
        signals.append({
            "type": "research_insight",
            "source": "marketing_os",
            "id": row[0],
            "content": row[1],
            "category": row[2],
            "confidence": row[3],
            "timestamp": row[4],
        })

    for row in conn.execute(
        """SELECT fi.id, f.name, fi.pain, fi.product_implications, fi.created_at
           FROM founder_intelligence fi JOIN founders f ON f.id = fi.founder_id
           ORDER BY fi.id DESC LIMIT 50"""
    ):
        signals.append({
            "type": "founder_intelligence",
            "source": "marketing_os",
            "id": row[0],
            "founder": row[1],
            "pain": row[2],
            "product_implications": row[3],
            "timestamp": row[4],
        })

    for row in conn.execute(
        """SELECT id, category, trigger, decision_made, outcome, why_it_failed, created_at
           FROM decision_patterns ORDER BY id DESC LIMIT 50"""
    ):
        signals.append({
            "type": "decision_pattern",
            "source": "marketing_os",
            "id": row[0],
            "category": row[1],
            "trigger": row[2],
            "decision": row[3],
            "outcome": row[4],
            "lesson": row[5],
            "timestamp": row[6],
        })

    return {"exported_at": datetime.now(timezone.utc).isoformat(), "signals": signals}


def export_memory_records(conn: sqlite3.Connection) -> dict:
    """Export as memory_records-compatible facts for Hustronix OS."""
    records = []

    for row in conn.execute(
        "SELECT question, times_seen, category FROM strategic_questions WHERE times_seen > 0 ORDER BY times_seen DESC"
    ):
        records.append({
            "fact": f"Strategic question trending: '{row[0]}' (seen {row[1]}x, category: {row[2]})",
            "source": "marketing_os_strategic_questions",
        })

    for row in conn.execute(
        "SELECT requirement, priority, status FROM product_requirements ORDER BY id DESC LIMIT 20"
    ):
        records.append({
            "fact": f"Product requirement [{row[2]}]: {row[0]} (priority: {row[1]})",
            "source": "marketing_os_product_requirements",
        })

    return {"exported_at": datetime.now(timezone.utc).isoformat(), "memory_records": records}


def main() -> None:
    parser = argparse.ArgumentParser(description="Export vault to Hustronix OS bridge format")
    parser.add_argument("--output", default=str(EXPORT_DIR))
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    signals = export_signals(conn)
    memory = export_memory_records(conn)

    (out / "external_signals.json").write_text(json.dumps(signals, indent=2), encoding="utf-8")
    (out / "memory_records.json").write_text(json.dumps(memory, indent=2), encoding="utf-8")

    conn.close()
    print(f"Exported to {out}")
    print(f"  signals: {len(signals['signals'])}")
    print(f"  memory_records: {len(memory['memory_records'])}")


if __name__ == "__main__":
    main()
