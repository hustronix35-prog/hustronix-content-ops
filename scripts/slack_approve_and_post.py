#!/usr/bin/env python3
"""Legacy entry — use slack_post_workflow.py. 'approve N' now selects; use 'publish' to post."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from slack_post_workflow import parse_command, run_command  # noqa: E402


def main() -> None:
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    action, option = parse_command(text)
    if action == "select" and option:
        result = run_command(f"select {option}")
    elif action == "publish":
        result = run_command("publish")
    else:
        result = run_command(text)
    print(json.dumps(result, indent=2, default=str))
    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
