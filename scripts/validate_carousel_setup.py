#!/usr/bin/env python3
"""Validate brand assets and render dependencies for premium carousels."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "assets" / "brand"

REQUIRED_BRAND_FILES = [
    "logo-lockup.png",
    "logo-horizontal.png",
    "hex-grid.svg",
    "premium.css",
    "tokens.css",
]


def validate_brand_assets() -> list[str]:
    errors = []
    for name in REQUIRED_BRAND_FILES:
        if not (BRAND / name).exists():
            errors.append(f"Missing brand asset: assets/brand/{name}")
    return errors


def validate_playwright() -> tuple[bool, str]:
    try:
        import playwright  # noqa: F401
    except ImportError:
        return False, "playwright not installed (pip install -r requirements.txt)"
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
        return True, "playwright chromium ok"
    except Exception as exc:
        return False, f"playwright chromium not ready: {exc}. Run: python scripts/setup_carousel_env.py"


def validate_all() -> dict:
    brand_errors = validate_brand_assets()
    pw_ok, pw_msg = validate_playwright()
    ok = not brand_errors and pw_ok
    return {
        "ok": ok,
        "brand_errors": brand_errors,
        "playwright_ok": pw_ok,
        "playwright_message": pw_msg,
        "quality_tier": "premium_v2",
    }


def main() -> None:
    result = validate_all()
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
