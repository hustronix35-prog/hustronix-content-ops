#!/usr/bin/env python3
"""One-time / CI setup: pip deps + Playwright Chromium for premium PNG export."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    req = ROOT / "requirements.txt"
    if req.exists():
        run([sys.executable, "-m", "pip", "install", "-r", str(req)])

    run([sys.executable, "-m", "playwright", "install", "chromium"])

    run([sys.executable, str(ROOT / "scripts" / "init_db.py")])

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_carousel_setup.py")],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    print(json.dumps({"setup": "complete", "ready_for": "premium carousel cloud render"}, indent=2))


if __name__ == "__main__":
    main()
