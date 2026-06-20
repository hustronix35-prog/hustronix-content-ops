"""Capture README screenshot PNGs into docs/assets/."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_ASSETS = ROOT / "docs" / "assets"
sys.path.insert(0, str(ROOT / "scripts"))

from lib.carousel_renderer import _render_png  # noqa: E402


def capture(html: Path, png: Path, width: int = 1080, height: int = 1080) -> None:
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": width, "height": height, "deviceScaleFactor": 2})
            page.goto(html.resolve().as_uri())
            page.wait_for_timeout(1500)
            page.screenshot(path=str(png), full_page=False)
            browser.close()
    except Exception:
        ok = _render_png(html, png)
        if not ok:
            raise RuntimeError(f"Failed to capture {html} -> {png}")


def main() -> None:
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)

    carousel_slide = ROOT / "assets" / "generated" / "3" / "slides" / "01-hook.html"
    if not carousel_slide.exists():
        raise SystemExit(f"Missing carousel slide: {carousel_slide}. Run: python scripts/generate_carousel.py --idea-id 3")

    capture(carousel_slide, DOCS_ASSETS / "screenshot-carousel.png", 1080, 1080)
    capture(DOCS_ASSETS / "slack-mockup.html", DOCS_ASSETS / "screenshot-slack.png", 900, 720)

    print("OK:", DOCS_ASSETS / "screenshot-carousel.png")
    print("OK:", DOCS_ASSETS / "screenshot-slack.png")


if __name__ == "__main__":
    main()
