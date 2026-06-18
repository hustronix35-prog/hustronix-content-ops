#!/usr/bin/env python3
"""Manual pipeline runner for daily research → strategist cycle."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run(cmd: list[str]) -> None:
    print(f">>> {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    steps = [
        [sys.executable, str(SCRIPTS / "vault_query.py"), "stats"],
        [sys.executable, str(SCRIPTS / "vault_query.py"), "list", "raw_sources", "--limit", "5"],
        [sys.executable, str(SCRIPTS / "vault_query.py"), "list", "content_ideas", "--status", "pending"],
    ]
    print("Marketing OS pipeline check")
    print("=" * 40)
    print("Next: run research-agent -> content-strategist skills in Cursor")
    print("Or ingest: python scripts/ingest_url.py <url>")
    print()
    for step in steps:
        run(step)


if __name__ == "__main__":
    main()
