#!/usr/bin/env python3
"""Score content ideas and drafts against Hustronix thresholds."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"

MIN_DIMENSION = 6
MAX_GENERIC_AI_RISK = 4
MIN_TOTAL = 28


def evaluate(
    founder_relevance: int,
    category_building: int,
    conversation_potential: int,
    di_alignment: int,
    generic_ai_risk: int,
) -> tuple[bool, int, str | None]:
    scores = {
        "founder_relevance": founder_relevance,
        "category_building": category_building,
        "conversation_potential": conversation_potential,
        "di_alignment": di_alignment,
        "generic_ai_risk": generic_ai_risk,
    }
    total = (
        founder_relevance
        + category_building
        + conversation_potential
        + di_alignment
        + (10 - generic_ai_risk)
    )
    reasons = []
    for key in (
        "founder_relevance",
        "category_building",
        "conversation_potential",
        "di_alignment",
    ):
        if scores[key] < MIN_DIMENSION:
            reasons.append(f"{key}={scores[key]} < {MIN_DIMENSION}")
    if generic_ai_risk > MAX_GENERIC_AI_RISK:
        reasons.append(f"generic_ai_risk={generic_ai_risk} > {MAX_GENERIC_AI_RISK}")
    if total < MIN_TOTAL:
        reasons.append(f"total={total} < {MIN_TOTAL}")
    passed = len(reasons) == 0
    return passed, total, "; ".join(reasons) if reasons else None


def store_score(
    idea_id: int | None,
    draft_id: int | None,
    scores: tuple[int, int, int, int, int],
    conn: sqlite3.Connection | None = None,
) -> dict:
    passed, total, reason = evaluate(*scores)
    own_conn = conn is None
    if own_conn:
        conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        """INSERT INTO content_scores
           (idea_id, draft_id, founder_relevance, category_building,
            conversation_potential, di_alignment, generic_ai_risk,
            total_score, passed, rejection_reason)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            idea_id,
            draft_id,
            *scores,
            total,
            1 if passed else 0,
            reason,
        ),
    )
    if idea_id and passed:
        conn.execute(
            "UPDATE content_ideas SET status = 'scored' WHERE id = ?", (idea_id,)
        )
    elif idea_id and not passed:
        conn.execute(
            "UPDATE content_ideas SET status = 'rejected' WHERE id = ?", (idea_id,)
        )
    if own_conn:
        conn.commit()
        conn.close()
    row_id = cur.lastrowid
    return {
        "id": row_id,
        "passed": passed,
        "total_score": total,
        "rejection_reason": reason,
        "scores": {
            "founder_relevance": scores[0],
            "category_building": scores[1],
            "conversation_potential": scores[2],
            "di_alignment": scores[3],
            "generic_ai_risk": scores[4],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score content ideas/drafts")
    parser.add_argument("--idea-id", type=int)
    parser.add_argument("--draft-id", type=int)
    parser.add_argument(
        "--scores",
        required=True,
        help="Comma-separated: founder_relevance,category_building,conversation_potential,di_alignment,generic_ai_risk",
    )
    args = parser.parse_args()

    if not args.idea_id and not args.draft_id:
        print("Provide --idea-id and/or --draft-id", file=sys.stderr)
        sys.exit(1)

    parts = [int(x.strip()) for x in args.scores.split(",")]
    if len(parts) != 5:
        print("Expected 5 scores", file=sys.stderr)
        sys.exit(1)

    result = store_score(args.idea_id, args.draft_id, tuple(parts))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
