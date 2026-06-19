"""Ensure premium carousel render environment is ready (local + cloud)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def ensure_render_ready(auto_setup: bool = True) -> dict:
    sys.path.insert(0, str(ROOT / "scripts"))
    from validate_carousel_setup import validate_all

    result = validate_all()
    if result["ok"]:
        return result

    if not auto_setup:
        raise RuntimeError(
            "Carousel render not ready: "
            + "; ".join(result.get("brand_errors", []) + [result.get("playwright_message", "")])
        )

    if result.get("brand_errors"):
        raise RuntimeError(
            "Brand assets missing from repo — commit assets/brand/ before cloud deploy. "
            + "; ".join(result["brand_errors"])
        )

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "setup_carousel_env.py")],
        check=True,
        cwd=ROOT,
    )
    result = validate_all()
    if not result["ok"]:
        raise RuntimeError(result.get("playwright_message", "setup failed"))
    return result
