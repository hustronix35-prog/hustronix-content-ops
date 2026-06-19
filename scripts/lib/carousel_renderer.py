"""Render premium Hustronix carousel slides to HTML and PNG."""

from __future__ import annotations

import base64
import html
import json
import subprocess
from pathlib import Path

from lib.carousel_visuals import (
    execution_arrow,
    founder_silhouette,
    fragmented_nodes,
    hook_signal_glow,
    network_splitting,
    question_mark_nodes,
    signal_network,
    signal_noise_highlight,
    unified_network,
)

ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "assets" / "brand"

LOGO_LOCKUP_URI: str | None = None


def _png_data_uri(filename: str) -> str:
    path = BRAND / filename
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _logo_uri() -> str:
    global LOGO_LOCKUP_URI
    if LOGO_LOCKUP_URI is None:
        LOGO_LOCKUP_URI = _png_data_uri("logo-lockup.png")
    return LOGO_LOCKUP_URI


def _esc(text: str) -> str:
    return html.escape(text or "")


def _load_css(story: str | None = None) -> str:
    premium = (BRAND / "premium.css").read_text(encoding="utf-8")
    hex_grid = (BRAND / "hex-grid.svg").read_text(encoding="utf-8")
    hex_uri = "data:image/svg+xml," + hex_grid.replace("\n", "").replace("#", "%23")
    css = premium.replace('url("../brand/hex-grid.svg")', f'url("{hex_uri}")')
    if story in ("founder_context_problem", "post_intelligent"):
        story_css = (BRAND / "story-founder-context.css").read_text(encoding="utf-8")
        css += "\n" + story_css
    return css


def _headline_html(slide: dict) -> str:
    hl = slide.get("headline", "")
    highlight = slide.get("headline_highlight")
    if highlight:
        return f"{_esc(hl)} <span class='gold'>{_esc(highlight)}</span>"
    return _esc(hl)


def _footer_dots(index: int, total: int) -> str:
    parts = []
    for i in range(1, total + 1):
        cls = " slide__footer-dot--active" if i == index else ""
        parts.append(f'<span class="slide__footer-dot{cls}"></span>')
    return f'<div class="slide__footer-dots">{"".join(parts)}</div>'


def _shell(
    slide: dict,
    index: int,
    total: int,
    category: str,
    body_html: str,
    *,
    cta: bool = False,
    cover: bool = False,
    story: str | None = None,
    series_title: str = "",
) -> str:
    progress = int((index / total) * 100)
    logo = _logo_uri()
    story_class = " story-fcp" if story in ("founder_context_problem", "post_intelligent") else ""
    cta_class = " slide--cta" if cta else ""
    cover_class = " slide--cover" if cover else ""
    if story in ("founder_context_problem", "post_intelligent") and slide.get("layout") == "fcp_hook":
        cover_class += " slide--fcp-hook"
    label = series_title or slide.get("label", category.replace("_", " ").title())

    if story in ("founder_context_problem", "post_intelligent") and slide.get("layout") == "fcp_cta":
        footer_html = f'<img class="slide__logo-img slide__logo-img--large" src="{logo}" alt="Hustronix"/>'
        footer_class = "slide__footer slide__footer--fcp-cta"
    elif story in ("founder_context_problem", "post_intelligent") and slide.get("layout") == "fcp_hook":
        footer_html = _footer_dots(index, total)
        footer_class = "slide__footer"
    elif story in ("founder_context_problem", "post_intelligent"):
        footer_html = f'<img class="slide__logo-img" src="{logo}" alt="Hustronix"/>{_footer_dots(index, total)}'
        footer_class = "slide__footer"
    elif cta:
        footer_html = f'<img class="slide__cta-logo" src="{logo}" alt="Hustronix"/>'
        footer_class = "slide__footer"
    else:
        footer_html = f'<img class="slide__logo-img" src="{logo}" alt="Hustronix"/>{_footer_dots(index, total)}'
        footer_class = "slide__footer"

    cta_rings = ""
    if cta and story not in ("founder_context_problem", "post_intelligent"):
        cta_rings = '<div class="slide__cta-ring"></div><div class="slide__cta-ring slide__cta-ring--inner"></div>'

    index_html = (
        f'<span class="fcp-num">{index:02d}</span>'
        if story in ("founder_context_problem", "post_intelligent")
        else f'<span class="slide__index">{index:02d} / {total:02d}</span>'
    )
    series_html = (
        f'<span class="fcp-series">{_esc(label)}</span>'
        if story in ("founder_context_problem", "post_intelligent")
        else f'<span class="slide__series">{_esc(label)}</span>'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{_esc(slide.get('name', 'Slide'))}</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
  <style>{_load_css(story)}</style>
</head>
<body>
  <div class="slide{story_class}{cta_class}{cover_class}">
    <div class="slide__glow slide__glow--gold"></div>
    <div class="slide__glow slide__glow--soft"></div>
    <div class="slide__hex"></div>
    <div class="slide__vignette"></div>
    {cta_rings}
    <div class="slide__progress"><div class="slide__progress-fill" style="width:{progress}%"></div></div>
    <div class="slide__frame">
      <div class="slide__top">
        {index_html}
        {series_html}
      </div>
      {body_html}
    </div>
    <footer class="{footer_class}">
      {footer_html}
    </footer>
  </div>
</body>
</html>"""


def _layout_cover(slide: dict) -> str:
    sub = f'<p class="slide__sub">{_esc(slide["sub"])}</p>' if slide.get("sub") else ""
    visual = f'<div class="visual-panel" style="margin-top:40px;height:240px;">{signal_network(active=True)}</div>'
    return f"""
      <div class="slide__pill"><span class="slide__pill-dot"></span>{_esc(slide.get('label', ''))}</div>
      <h1 class="slide__headline slide__headline--hero">{_headline_html(slide)}</h1>
      {sub}
      {visual}
    """


def _layout_split(slide: dict) -> str:
    bullets = slide.get("bullets", [])
    bl = ""
    if bullets:
        items = "".join(f"<li>{_esc(b)}</li>" for b in bullets)
        bl = f'<ul class="slide__bullets">{items}</ul>'

    vis_key = slide.get("visual", "fragments")
    vis = fragmented_nodes() if vis_key == "fragments" else signal_network(active=True)

    sub = f'<p class="slide__sub">{_esc(slide["sub"])}</p>' if slide.get("sub") else ""
    return f"""
      <div class="slide__pill"><span class="slide__pill-dot"></span>{_esc(slide.get('label', ''))}</div>
      <div class="slide__split">
        <div>
          <h1 class="slide__headline">{_esc(slide.get('headline', ''))}</h1>
          {sub}
          {bl}
        </div>
        <div class="visual-panel">{vis}</div>
      </div>
    """


def _layout_pipeline(slide: dict) -> str:
    steps = slide.get("pipeline", [])
    parts = ['<div class="pipeline">']
    for i, (title, desc) in enumerate(steps, 1):
        parts.append(f"""
          <div class="pipeline__step">
            <div class="pipeline__badge">{i:02d}</div>
            <div>
              <div class="pipeline__title">{_esc(title)}</div>
              <div class="pipeline__desc">{_esc(desc)}</div>
            </div>
          </div>
        """)
    parts.append("</div>")
    sub = f'<p class="slide__sub">{_esc(slide["sub"])}</p>' if slide.get("sub") else ""
    return f"""
      <div class="slide__pill"><span class="slide__pill-dot"></span>{_esc(slide.get('label', 'Framework'))}</div>
      <h1 class="slide__headline">{_esc(slide.get('headline', ''))}</h1>
      {sub}
      {"".join(parts)}
    """


def _layout_flow(slide: dict) -> str:
    steps = slide.get("flow", [])
    active = slide.get("active_step")
    nodes = []
    for i, step in enumerate(steps):
        if i:
            nodes.append('<span class="flow-bar__arrow">→</span>')
        cls = " flow-bar__node--active" if step == active else ""
        nodes.append(f'<div class="flow-bar__node{cls}">{_esc(step)}</div>')

    sub = f'<p class="slide__sub">{_esc(slide["sub"])}</p>' if slide.get("sub") else ""
    return f"""
      <div class="slide__pill"><span class="slide__pill-dot"></span>{_esc(slide.get('label', 'Model'))}</div>
      <h1 class="slide__headline">{_esc(slide.get('headline', ''))}</h1>
      {sub}
      <div class="flow-bar">
        <div class="flow-bar__track">{"".join(nodes)}</div>
        <div style="margin-top:24px">{execution_arrow()}</div>
      </div>
    """


def _layout_stats(slide: dict) -> str:
    stats = slide.get("stats", [])
    cards = []
    for label, text in stats:
        cards.append(f"""
          <div class="stat-card">
            <div class="stat-card__label">{_esc(label)}</div>
            <div class="stat-card__text">{_esc(text)}</div>
          </div>
        """)
    return f"""
      <div class="slide__pill"><span class="slide__pill-dot"></span>{_esc(slide.get('label', ''))}</div>
      <h1 class="slide__headline">{_esc(slide.get('headline', ''))}</h1>
      <div class="stat-row">{"".join(cards)}</div>
    """


def _layout_quote(slide: dict) -> str:
    sub = f'<p class="slide__sub">{_esc(slide["sub"])}</p>' if slide.get("sub") else ""
    quote = slide.get("quote", slide.get("sub", ""))
    return f"""
      <div class="slide__pill"><span class="slide__pill-dot"></span>{_esc(slide.get('label', ''))}</div>
      <h1 class="slide__headline slide__headline--quote">{_esc(slide.get('headline', ''))}</h1>
      {sub}
      <div class="quote-block"><p class="slide__sub" style="margin:0;color:var(--hx-white);font-size:22px;">{_esc(quote)}</p></div>
      <div class="visual-panel" style="margin-top:32px;height:180px;">{unified_network()}</div>
    """


def _layout_cta(slide: dict) -> str:
    sub = f'<p class="slide__sub">{_esc(slide["sub"])}</p>' if slide.get("sub") else ""
    return f"""
      <div class="slide__pill"><span class="slide__pill-dot"></span>Hustronix</div>
      <h1 class="slide__headline">{_esc(slide.get('headline', ''))}</h1>
      {sub}
    """


def _layout_fcp_hook(slide: dict) -> str:
    line2 = f'<p class="fcp-line2">{_esc(slide["line2"])}</p>' if slide.get("line2") else ""
    note = f'<div class="fcp-footer-note">{_esc(slide.get("footer_note", ""))}</div>' if slide.get("footer_note") else ""
    visual = f'<div class="fcp-hook-visual">{hook_signal_glow()}</div>'
    return f"""
      <div style="position:relative;flex:1;display:flex;flex-direction:column;">
        <p class="fcp-line1">{_esc(slide.get("line1", ""))}</p>
        {line2}
        {note}
        {visual}
      </div>
    """


def _layout_fcp_founder(slide: dict) -> str:
    bullets = "".join(f"<li>{_esc(b)}</li>" for b in slide.get("bullets", []))
    return f"""
      <div class="fcp-split">
        <div>
          <h2 class="fcp-section-title">{_esc(slide.get("title", ""))}</h2>
          <ul class="fcp-bullets">{bullets}</ul>
          <div class="fcp-callout">{_esc(slide.get("callout", ""))}</div>
        </div>
        <div class="fcp-visual">{founder_silhouette()}</div>
      </div>
    """


def _layout_fcp_fragment(slide: dict) -> str:
    frags = "".join(
        f'<p><strong>{_esc(name)}</strong> {_esc(desc)}</p>'
        for name, desc in slide.get("fragments", [])
    )
    return f"""
      <div>
        <p class="fcp-line1" style="font-size:32px;">{_esc(slide.get("line1", ""))}</p>
        <p class="fcp-line2 fcp-line2--lg">{_esc(slide.get("line2", ""))}</p>
        <div class="fcp-split" style="margin-top:32px;">
          <div class="fcp-fragment-lines">{frags}</div>
          <div class="fcp-visual">{network_splitting()}</div>
        </div>
      </div>
    """


def _layout_fcp_data(slide: dict) -> str:
    data_boxes = "".join(
        f'<div class="fcp-data-box"><span class="fcp-data-icon">◆</span>{_esc(item)}</div>'
        for item in slide.get("data_items", [])
    )
    flow = slide.get("flow_items", [])
    flow_html = []
    for i, step in enumerate(flow):
        if i:
            flow_html.append('<div class="fcp-flow-arrow">↓</div>')
        cls = " fcp-flow-step--gold" if step == "Decision" else ""
        flow_html.append(f'<div class="fcp-flow-step{cls}">{_esc(step)}</div>')
    return f"""
      <div>
        <p class="fcp-line1" style="font-size:36px;">{_esc(slide.get("line1", ""))}</p>
        <p class="fcp-line2 fcp-line2--lg" style="margin-bottom:40px;">{_esc(slide.get("line2", ""))}</p>
        <div class="fcp-split">
          <div class="fcp-data-col">
            <h3>Data</h3>
            {data_boxes}
          </div>
          <div class="fcp-flow-col">{"".join(flow_html)}</div>
        </div>
      </div>
    """


def _layout_fcp_challenge(slide: dict) -> str:
    return f"""
      <div class="fcp-split">
        <div class="fcp-challenge-block">
          <p>{_esc(slide.get("challenge1", ""))}</p>
          <p>{_esc(slide.get("challenge1b", ""))}</p>
          <p style="margin-top:28px;">{_esc(slide.get("challenge2", ""))}</p>
          <p class="gold">{_esc(slide.get("challenge2b", ""))}</p>
        </div>
        <div class="fcp-visual">{signal_noise_highlight()}</div>
      </div>
    """


def _layout_fcp_question(slide: dict) -> str:
    return f"""
      <div class="fcp-split">
        <div>
          <p class="fcp-line1" style="font-size:28px;color:var(--hx-grey-soft);font-weight:500;">{_esc(slide.get("intro", ""))}</p>
          <p class="fcp-question-text" style="margin-top:24px;">{_esc(slide.get("question", ""))}</p>
        </div>
        <div class="fcp-visual">{question_mark_nodes()}</div>
      </div>
    """


def _layout_fcp_cta(slide: dict) -> str:
    points = "".join(
        f'<li><strong>{_esc(a)}</strong> {_esc(b)}</li>'
        for a, b in slide.get("points", [])
    )
    cta = f'<div class="fcp-building">{_esc(slide.get("cta", ""))}</div>' if slide.get("cta") else ""
    return f"""
      <div class="fcp-cta-layout">
        <div>
          <h2 class="fcp-section-title">{_esc(slide.get("headline", ""))}</h2>
          <ul class="fcp-cta-bullets">{points}</ul>
          {cta}
        </div>
      </div>
    """


def _layout_default(slide: dict) -> str:
    sub = f'<p class="slide__sub">{_esc(slide["sub"])}</p>' if slide.get("sub") else ""
    return f"""
      <h1 class="slide__headline">{_esc(slide.get('headline', ''))}</h1>
      {sub}
    """


LAYOUTS = {
    "cover": _layout_cover,
    "split": _layout_split,
    "pipeline": _layout_pipeline,
    "flow": _layout_flow,
    "stats": _layout_stats,
    "quote": _layout_quote,
    "cta": _layout_cta,
    "fcp_hook": _layout_fcp_hook,
    "fcp_founder": _layout_fcp_founder,
    "fcp_fragment": _layout_fcp_fragment,
    "fcp_data": _layout_fcp_data,
    "fcp_challenge": _layout_fcp_challenge,
    "fcp_question": _layout_fcp_question,
    "fcp_cta": _layout_fcp_cta,
}


def render_slide_html(
    slide: dict,
    index: int,
    total: int,
    category: str,
    *,
    story: str | None = None,
    series_title: str = "",
) -> str:
    layout = slide.get("layout", "cover")
    builder = LAYOUTS.get(layout, _layout_default)
    body = builder(slide)
    return _shell(
        slide,
        index,
        total,
        category,
        body,
        cta=(layout in ("cta", "fcp_cta")),
        cover=(layout in ("cover", "fcp_hook")),
        story=story,
        series_title=series_title,
    )


def write_brief_yaml(brief: dict, path: Path) -> None:
    lines = [
        f"topic: {brief['topic']}",
        f"visual_type: {brief['visual_type']}",
        f"visual_category: {brief['visual_category']}",
        f"layout: {brief['layout']}",
        "slides:",
    ]
    for slide in brief["slides"]:
        if isinstance(slide, dict):
            lines.append(f"  - name: {slide['name']}")
            lines.append(f"    layout: {slide.get('layout', 'cover')}")
            lines.append(f"    headline: \"{slide.get('headline', '').replace(chr(34), '')[:120]}\"")
        else:
            lines.append(f"  - name: {slide}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_brief(path: Path) -> dict:
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not data.get("slides"):
        raise ValueError(f"No slides in {path}")
    return data


def render_carousel(brief: dict, out_dir: Path, render_png: bool = True) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    slides_dir = out_dir / "slides"
    slides_dir.mkdir(exist_ok=True)

    category = brief.get("visual_category", "decision_pattern")
    story = brief.get("story")
    series_title = brief.get("series_title", "")
    slides = brief["slides"]
    total = len(slides)
    html_paths: list[str] = []
    png_paths: list[str] = []

    for i, slide in enumerate(slides, 1):
        slide_data = slide if isinstance(slide, dict) else {"name": str(slide), "headline": str(slide), "layout": "cover"}
        name = slide_data.get("name", f"slide-{i}").lower().replace(" ", "-")
        html_path = slides_dir / f"{i:02d}-{name}.html"
        html_path.write_text(
            render_slide_html(slide_data, i, total, category, story=story, series_title=series_title),
            encoding="utf-8",
        )
        html_paths.append(str(html_path))

        if render_png:
            png_path = slides_dir / f"{i:02d}-{name}.png"
            if _render_png(html_path, png_path):
                png_paths.append(str(png_path))

    preview_path = out_dir / "preview.html"
    frames = "\n".join(
        f'<iframe src="slides/{Path(p).name}" width="1080" height="1080" style="border:none;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,0.5);"></iframe>'
        for p in html_paths
    )
    preview_path.write_text(
        f"<!DOCTYPE html><html><head><meta charset='utf-8'/><title>Premium Carousel</title>"
        f"<style>body{{background:#050505;margin:0;padding:32px;display:flex;flex-direction:column;align-items:center;gap:32px;font-family:Inter,sans-serif;}}"
        f"h1{{color:#ededed;font-size:14px;letter-spacing:0.2em;text-transform:uppercase;font-weight:600;}}</style></head>"
        f"<body><h1>{_esc(series_title or 'Hustronix Premium Carousel')}</h1>{frames}</body></html>",
        encoding="utf-8",
    )

    manifest = {
        "output_dir": str(out_dir),
        "slide_count": total,
        "html_slides": html_paths,
        "png_slides": png_paths,
        "preview": str(preview_path),
        "design_brief": str(out_dir / "design-brief.yaml"),
        "quality": "post_intelligent_v1" if story == "post_intelligent" else (
            "founder_context_v1" if story == "founder_context_problem" else "premium_v2"
        ),
        "render_complete": len(png_paths) == total if render_png else None,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def _render_png(html_path: Path, png_path: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1080, "height": 1080, "deviceScaleFactor": 2})
            page.goto(html_path.resolve().as_uri())
            page.wait_for_timeout(1200)
            page.screenshot(path=str(png_path), full_page=True)
            browser.close()
        return True
    except ImportError:
        return _render_png_edge(html_path, png_path)
    except Exception:
        return _render_png_edge(html_path, png_path)


def _render_png_edge(html_path: Path, png_path: Path) -> bool:
    for browser in [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]:
        exe = Path(browser)
        if not exe.exists():
            continue
        try:
            subprocess.run(
                [str(exe), "--headless=new", "--disable-gpu", "--window-size=1080,1080",
                 f"--screenshot={png_path}", html_path.resolve().as_uri()],
                check=True, capture_output=True, timeout=45,
            )
            return png_path.exists()
        except Exception:
            continue
    return False
