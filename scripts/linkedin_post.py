#!/usr/bin/env python3
"""Publish a text post to LinkedIn (personal profile via UGC API)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from lib.env_config import load_env, require_env  # noqa: E402
from lib.linkedin_media import post_to_linkedin as _post_with_media  # noqa: E402


def post_to_linkedin(text: str, image_paths: list | None = None) -> dict:
    return _post_with_media(text, image_paths=image_paths)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: linkedin_post.py \"post text\" OR --file path", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--file":
        text = open(sys.argv[2], encoding="utf-8").read()
    else:
        text = sys.argv[1]

    try:
        result = post_to_linkedin(text)
        print(json.dumps(result, indent=2))
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
