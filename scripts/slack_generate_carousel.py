#!/usr/bin/env python3
"""Legacy — use slack_post_workflow.py carousel."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from slack_post_workflow import main  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.argv = [sys.argv[0], sys.argv[1] if "carousel" in sys.argv[1].lower() else f"carousel {sys.argv[1]}"]
    else:
        sys.argv = [sys.argv[0], "carousel"]
    main()
