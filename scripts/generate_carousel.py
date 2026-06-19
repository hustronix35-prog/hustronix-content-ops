#!/usr/bin/env python3
"""Generate Hustronix carousel or single image from a content idea."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"
ASSETS = ROOT / "assets" / "generated"
sys.path.insert(0, str(ROOT / "scripts"))

from lib.carousel_builder import build_brief  # noqa: E402
from lib.carousel_env import ensure_render_ready  # noqa: E402
from lib.carousel_renderer import render_carousel, write_brief_yaml  # noqa: E402


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def idea_from_id(idea_id: int) -> dict:
    conn = connect()
    row = conn.execute("SELECT * FROM content_ideas WHERE id = ?", (idea_id,)).fetchone()
    conn.close()
    if not row:
        raise SystemExit(f"Idea {idea_id} not found")
    return dict(row)


def idea_from_post_option(option_num: int) -> dict:
    conn = connect()
    row = conn.execute(
        """SELECT o.*, i.source_type, i.source_id
           FROM daily_post_options o
           LEFT JOIN content_ideas i ON i.id = o.idea_id
           WHERE o.option_num = ? AND o.status = 'pending'
           ORDER BY o.batch_date DESC LIMIT 1""",
        (option_num,),
    ).fetchone()
    conn.close()
    if not row:
        raise SystemExit(f"No pending post option {option_num}")
    return {
        "id": row["idea_id"] or option_num,
        "pillar": row["pillar"],
        "post_type": row["post_type"],
        "hook": row["hook"],
        "source_type": row["source_type"] or "research",
        "body": row["body"],
    }


def generate(
    idea: dict,
    draft_id: int | None = None,
    visual_type: str = "carousel",
    render_png: bool = True,
) -> dict:
    draft_id = draft_id or idea.get("id") or 0
    out_dir = ASSETS / str(draft_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    if render_png:
        ensure_render_ready(auto_setup=True)
    brief = build_brief(idea, visual_type=visual_type)
    write_brief_yaml(brief, out_dir / "design-brief.yaml")
    manifest = render_carousel(brief, out_dir, render_png=render_png)
    if render_png and manifest.get("slide_count", 0) != len(manifest.get("png_slides", [])):
        raise RuntimeError(
            f"Premium PNG render incomplete ({len(manifest.get('png_slides', []))}/"
            f"{manifest.get('slide_count')} slides). Run: python scripts/setup_carousel_env.py"
        )
    manifest["visual_type"] = brief["visual_type"]
    manifest["visual_category"] = brief["visual_category"]
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Hustronix carousel/images")
    parser.add_argument("--idea-id", type=int, help="Content idea ID")
    parser.add_argument("--option", type=int, help="Daily post option 1-3")
    parser.add_argument("--single", action="store_true", help="Single insight image (1080x1080)")
    parser.add_argument("--html-only", action="store_true", help="Skip PNG render")
    parser.add_argument("--draft-id", type=int, help="Output folder under assets/generated/")
    args = parser.parse_args()

    if args.option:
        idea = idea_from_post_option(args.option)
    elif args.idea_id:
        idea = idea_from_id(args.idea_id)
    else:
        parser.error("Provide --idea-id or --option")

    visual_type = "single_image" if args.single else "carousel"
    result = generate(
        idea,
        draft_id=args.draft_id,
        visual_type=visual_type,
        render_png=not args.html_only,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
