#!/usr/bin/env python3
"""Render PNG slides from an existing design-brief.yaml."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.carousel_renderer import load_brief, render_carousel  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", help="Path to design-brief.yaml or draft folder")
    parser.add_argument("--html-only", action="store_true")
    args = parser.parse_args()

    path = Path(args.brief)
    if path.is_dir():
        path = path / "design-brief.yaml"
    brief = load_brief(path)
    out_dir = path.parent
    result = render_carousel(brief, out_dir, render_png=not args.html_only)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
