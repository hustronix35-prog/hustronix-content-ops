#!/usr/bin/env python3
"""Score design briefs against Hustronix visual thresholds."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"

THRESHOLDS = {
    "clarity": 8,
    "brand_consistency": 9,
    "founder_appeal": 8,
    "di_alignment": 9,
    "generic_ai_feel_max": 2,
}


def evaluate(
    clarity: int,
    brand_consistency: int,
    founder_appeal: int,
    di_alignment: int,
    generic_ai_feel: int,
) -> tuple[bool, int, str | None]:
    total = clarity + brand_consistency + founder_appeal + di_alignment + (
        10 - generic_ai_feel
    )
    reasons = []
    if clarity < THRESHOLDS["clarity"]:
        reasons.append(f"clarity={clarity} < {THRESHOLDS['clarity']}")
    if brand_consistency < THRESHOLDS["brand_consistency"]:
        reasons.append(
            f"brand_consistency={brand_consistency} < {THRESHOLDS['brand_consistency']}"
        )
    if founder_appeal < THRESHOLDS["founder_appeal"]:
        reasons.append(
            f"founder_appeal={founder_appeal} < {THRESHOLDS['founder_appeal']}"
        )
    if di_alignment < THRESHOLDS["di_alignment"]:
        reasons.append(
            f"di_alignment={di_alignment} < {THRESHOLDS['di_alignment']}"
        )
    if generic_ai_feel > THRESHOLDS["generic_ai_feel_max"]:
        reasons.append(
            f"generic_ai_feel={generic_ai_feel} > {THRESHOLDS['generic_ai_feel_max']}"
        )
    passed = len(reasons) == 0
    return passed, total, "; ".join(reasons) if reasons else None


def store_score(
    draft_id: int,
    visual_category: str | None,
    scores: tuple[int, int, int, int, int],
    conn: sqlite3.Connection | None = None,
) -> dict:
    passed, total, reason = evaluate(*scores)
    own_conn = conn is None
    if own_conn:
        conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        """INSERT INTO design_scores
           (draft_id, visual_category, clarity, brand_consistency, founder_appeal,
            di_alignment, generic_ai_feel, total_score, passed, rejection_reason)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (draft_id, visual_category, *scores, total, 1 if passed else 0, reason),
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
            "clarity": scores[0],
            "brand_consistency": scores[1],
            "founder_appeal": scores[2],
            "di_alignment": scores[3],
            "generic_ai_feel": scores[4],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score design briefs")
    parser.add_argument("--draft-id", type=int, required=True)
    parser.add_argument("--visual-category", default=None)
    parser.add_argument(
        "--scores",
        required=True,
        help="Comma-separated: clarity,brand_consistency,founder_appeal,di_alignment,generic_ai_feel",
    )
    args = parser.parse_args()

    parts = [int(x.strip()) for x in args.scores.split(",")]
    if len(parts) != 5:
        print("Expected 5 scores", file=sys.stderr)
        sys.exit(1)

    result = store_score(args.draft_id, args.visual_category, tuple(parts))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
