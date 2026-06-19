#!/usr/bin/env python3
"""
Slack post workflow router:
  select 1|2|3  → pick post option
  carousel      → generate slides + upload to Slack (uses selected option)
  publish       → post text (+ carousel if ready) to LinkedIn
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"
sys.path.insert(0, str(ROOT / "scripts"))

from generate_carousel import generate  # noqa: E402
from lib.linkedin_media import post_to_linkedin  # noqa: E402
from lib.post_workflow import (  # noqa: E402
    get_selected,
    idea_dict_from_row,
    mark_carousel_ready,
    mark_published,
    migrate,
    select_option,
)
from lib.slack_upload import upload_carousel_optional  # noqa: E402


def parse_command(text: str) -> tuple[str, int | None]:
    t = text.strip().lower()
    if m := re.search(r"(?:select|pick|choose)\s*[#]?\s*([123])", t):
        return "select", int(m.group(1))
    if re.fullmatch(r"carousel", t) or t == "slides":
        return "carousel", None
    if m := re.search(r"carousel\s*[#]?\s*([123])", t):
        return "carousel", int(m.group(1))
    if re.fullmatch(r"publish|post|go", t):
        return "publish", None
    if m := re.search(r"approve\s*[#]?\s*([123])", t):
        return "select", int(m.group(1))
    return "unknown", None


def cmd_select(option_num: int) -> dict:
    result = select_option(option_num)
    if not result.get("success"):
        return result
    result["slack_message"] = (
        f"*Selected OPTION {option_num}*\n"
        f"_{result['hook']}_\n\n"
        f"{result['body_preview']}\n\n"
        f"Reply *carousel* to generate brand slides (sent here for review).\n"
        f"Reply *publish* to post on LinkedIn (text only, or text + carousel if generated)."
    )
    return result


def cmd_carousel(option_num: int | None = None) -> dict:
    migrate()
    if option_num:
        select_option(option_num)

    row = get_selected()
    if not row:
        return {
            "success": False,
            "error": "No post selected. Reply select 1, select 2, or select 3 first.",
        }

    idea = idea_dict_from_row(row)
    draft_id = idea["id"]
    manifest = generate(idea, draft_id=draft_id, visual_type="carousel", render_png=True)
    png_slides = manifest.get("png_slides", [])

    mark_carousel_ready(row["id"], manifest["output_dir"])

    slack_result = upload_carousel_optional(
        png_slides,
        option_num=row["option_num"],
        hook=row["hook"],
    )

    if slack_result.get("success"):
        slack_msg = (
            f"Carousel uploaded to Slack ({slack_result['uploaded_count']} slides).\n"
            f"Review the images above, then reply *publish* to post on LinkedIn."
        )
    elif slack_result.get("skipped"):
        slack_msg = (
            f"Carousel generated ({len(png_slides)} PNGs) but Slack upload needs secrets.\n"
            f"Add SLACK_BOT_TOKEN + SLACK_CHANNEL_ID to automation secrets.\n"
            f"Preview: {manifest['preview']}\n"
            f"Slides: {manifest['output_dir']}/slides/\n"
            f"Reply *publish* when ready."
        )
    else:
        slack_msg = (
            f"Carousel generated but Slack upload failed: {slack_result.get('error')}\n"
            f"Preview: {manifest['preview']}\n"
            f"Reply *publish* to post on LinkedIn anyway."
        )

    return {
        "success": True,
        "option_num": row["option_num"],
        "slide_count": manifest["slide_count"],
        "png_count": len(png_slides),
        "preview": manifest["preview"],
        "output_dir": manifest["output_dir"],
        "slack_upload": slack_result,
        "slack_message": slack_msg,
    }


def cmd_publish() -> dict:
    row = get_selected()
    if not row:
        return {
            "success": False,
            "error": "Nothing selected. Reply select 1|2|3 first.",
        }

    body = row["body"]
    image_paths: list[str] = []
    if row["carousel_dir"]:
        slides = sorted(Path(row["carousel_dir"]).glob("slides/*.png"))
        image_paths = [str(p) for p in slides]

    try:
        li_result = post_to_linkedin(body, image_paths=image_paths or None)
    except Exception as exc:
        return {"success": False, "error": str(exc), "option_num": row["option_num"]}

    mark_published(row["id"], li_result.get("post_id", "published"))

    if row["idea_id"]:
        conn = sqlite3.connect(DB_PATH)
        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "UPDATE content_ideas SET status = 'published' WHERE id = ?", (row["idea_id"],)
        )
        cur = conn.execute(
            "INSERT INTO content_drafts (idea_id, format, body) VALUES (?, 'linkedin_default', ?)",
            (row["idea_id"], body),
        )
        draft_id = cur.lastrowid
        conn.execute(
            "INSERT INTO published_posts (draft_id, platform, published_at) VALUES (?, 'linkedin_personal', ?)",
            (draft_id, now),
        )
        conn.commit()
        conn.close()

    mode = f"text + {len(image_paths)} images" if image_paths else "text only"
    return {
        "success": True,
        "option_num": row["option_num"],
        "hook": row["hook"],
        "word_count": len(body.split()),
        "linkedin": li_result,
        "publish_mode": mode,
        "slack_message": (
            f"Published OPTION {row['option_num']} to LinkedIn ({mode}).\n"
            f"Hook: {row['hook']}\n"
            f"Post ID: {li_result.get('post_id')}"
        ),
    }


def run_command(text: str) -> dict:
    action, option_num = parse_command(text)
    if action == "select":
        return cmd_select(option_num)  # type: ignore[arg-type]
    if action == "carousel":
        return cmd_carousel(option_num)
    if action == "publish":
        return cmd_publish()
    return {
        "success": False,
        "error": "Unknown command. Use: select 1|2|3 · carousel · publish",
    }


def main() -> None:
    if len(sys.argv) < 2:
        print(
            'Usage: slack_post_workflow.py "select 2" | "carousel" | "publish"',
            file=sys.stderr,
        )
        sys.exit(1)
    result = run_command(" ".join(sys.argv[1:]))
    print(json.dumps(result, indent=2, default=str))
    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
