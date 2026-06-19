"""Derive carousel slides intelligently from selected post content."""

from __future__ import annotations

import re

GENERIC_OPENINGS = (
    "one thing i've noticed",
    "something interesting came up",
    "i've been thinking about",
    "while working on hustronix",
    "after talking to a few founders",
    "a pattern i'm starting to see",
    "this surprised me",
    "we've been experimenting",
    "i used to think",
)

PILLAR_SERIES = {
    "Decision Quality": "DECISION QUALITY",
    "Founder Context": "FOUNDER CONTEXT",
    "AI Native Organizations": "AI NATIVE ORGS",
    "Building Hustronix": "BUILDING HUSTRONIX",
    "Founder Research": "FOUNDER RESEARCH",
    "Organizational Learning": "ORG LEARNING",
}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u2014", "-").replace("\u2013", "-")).strip()


def _paragraphs(body: str, hook: str) -> list[str]:
    raw = body.replace("\r\n", "\n")
    parts = [p.strip() for p in re.split(r"\n\s*\n", raw) if p.strip()]
    out: list[str] = []
    hook_norm = _clean(hook).lower()
    for p in parts:
        c = _clean(p)
        if not c:
            continue
        if c.lower() == hook_norm:
            continue
        if any(c.lower().startswith(o) for o in GENERIC_OPENINGS):
            continue
        out.append(c)
    return out


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 8]


def _split_hook(hook: str) -> tuple[str, str]:
    hook = _clean(hook)
    if ". " in hook:
        a, b = hook.split(". ", 1)
        return a + ".", b.rstrip(".") + ("." if not b.endswith(".") else "")
    return hook, ""


def _short(s: str, max_len: int = 72) -> str:
    s = _clean(s)
    if len(s) <= max_len:
        return s
    cut = s[: max_len - 3].rsplit(" ", 1)[0]
    return cut + "..."


def _bullets_from_post(paragraphs: list[str], hook: str, n: int = 4) -> list[str]:
    bullets: list[str] = []
    for p in paragraphs:
        for line in p.split("\n"):
            line = line.strip().lstrip("-•").strip()
            if line and len(line) < 80:
                bullets.append(_short(line, 60))
        for s in _sentences(p):
            if s.endswith("?"):
                continue
            if len(s) < 90 and s.lower() not in hook.lower():
                bullets.append(_short(s, 65))
        if len(bullets) >= n:
            break
    return bullets[:n] if bullets else [
        "why the decision was made",
        "what tradeoff was accepted",
        "what context shaped the call",
        "what the team still doesn't share",
    ]


def _find_question(paragraphs: list[str], hook: str) -> str:
    for p in paragraphs:
        if "?" in p:
            return _short(p, 140)
    for s in _sentences(hook):
        if "?" in s:
            return s
    return "What decision does your team keep reopening?"


def _find_contrast(paragraphs: list[str]) -> tuple[str, str]:
    for p in paragraphs:
        low = p.lower()
        if " isn't " in low or " is not " in low:
            parts = re.split(r"\.\s+", p, maxsplit=2)
            if len(parts) >= 2:
                return _short(parts[0]), _short(parts[1])
        if "i wonder" in low:
            return "We measure what's visible.", _short(p)
    for p in paragraphs:
        if "not because" in p.lower() and "because" in p.lower():
            return _short(p.split(".")[0] + "."), _short(p.split(".")[1] + "." if "." in p else p)
    return "The challenge isn't collecting more information.", "The challenge is knowing what matters."


def _fragment_lines(paragraphs: list[str]) -> list[tuple[str, str]]:
    teams = []
    for p in paragraphs:
        for m in re.finditer(r"(Sales|Product|Engineering|Marketing|GTM|Founders?)\s+sees?\s+(.+?)\.", p, re.I):
            teams.append((m.group(1).title(), m.group(2).strip().rstrip(".") + "."))
    if teams:
        return teams[:3]
    for p in paragraphs:
        if "fragment" in p.lower() or "scattered" in p.lower() or "slice" in p.lower():
            return [
                ("Product", "sees one piece."),
                ("Sales", "sees another."),
                ("Engineering", "sees another."),
            ]
    return [
        ("Teams", "see different slices."),
        ("Founders", "hold the full picture."),
        ("Context", "doesn't travel."),
    ]


def _data_items(post_type: str, paragraphs: list[str]) -> list[str]:
    text = " ".join(paragraphs).lower()
    items = []
    for word in ("Dashboards", "Metrics", "Reports", "Feedback", "Analytics", "Meetings"):
        if word.lower() in text:
            items.append(word)
    if not items:
        items = ["Dashboards", "Metrics", "Reports"] if post_type != "Builder" else [
            "Hypotheses", "Signals", "Outcomes"
        ]
    return items[:3]


def _flow_items(post_type: str, pillar: str) -> list[str]:
    if post_type in ("Framework", "Contrarian") or "decision" in pillar.lower():
        return ["Understanding", "Decision", "Action"]
    if post_type == "Builder":
        return ["Research", "Decision", "Execution"]
    return ["Inputs", "Intelligence", "Decision", "Action"][:3]


def _series_title(idea: dict) -> str:
    pillar = idea.get("pillar", "Decision Quality")
    if pillar in PILLAR_SERIES:
        return PILLAR_SERIES[pillar]
    return pillar.upper()[:28]


def _slide1(idea: dict, paragraphs: list[str]) -> dict:
    hook = idea.get("hook", "")
    line1, line2 = _split_hook(hook)
    if not line2 and paragraphs:
        sents = _sentences(paragraphs[0])
        if len(sents) >= 2:
            line2 = sents[1]
        elif len(sents) == 1:
            line2 = sents[0]
    note = "A pattern we're noticing while building Hustronix."
    for p in paragraphs[:2]:
        if "hustronix" in p.lower() or "founder" in p.lower():
            note = _short(p, 70)
            break
    return {
        "name": "Hook",
        "layout": "fcp_hook",
        "line1": line1,
        "line2": line2 or "The real issue is decision clarity.",
        "footer_note": note,
    }


def _slide2(idea: dict, paragraphs: list[str]) -> dict:
    post_type = idea.get("post_type", "Research")
    if post_type == "Builder":
        title = "What we're learning:"
    elif idea.get("source_type") == "founder":
        title = "Founders are telling us:"
    else:
        title = "The pattern:"
    bullets = _bullets_from_post(paragraphs, idea.get("hook", ""))
    callout = "Most of this is never written down."
    for p in paragraphs:
        if "never" in p.lower() or "not written" in p.lower() or "reopen" in p.lower():
            callout = _short(p, 80)
            break
        if "i wonder" in p.lower():
            callout = _short(p, 80)
            break
    return {
        "name": "Insight",
        "layout": "fcp_founder",
        "title": title,
        "bullets": bullets,
        "callout": callout,
    }


def _slide3(idea: dict, paragraphs: list[str]) -> dict:
    frags = _fragment_lines(paragraphs)
    line1 = "As teams grow:"
    line2 = "Context gets fragmented."
    for p in paragraphs:
        low = p.lower()
        if "grow" in low or "scale" in low:
            line1 = _short(_sentences(p)[0] if _sentences(p) else p, 50)
        if "fragment" in low or "scattered" in low or "harder" in low:
            line2 = _short(p.split(".")[0] + "." if "." in p else p, 55)
    return {
        "name": "Fragment",
        "layout": "fcp_fragment",
        "line1": line1,
        "line2": line2,
        "fragments": frags,
    }


def _slide4(idea: dict, paragraphs: list[str]) -> dict:
    line1 = "Everyone has data."
    line2 = "Few people have understanding."
    for i, p in enumerate(paragraphs):
        low = p.lower()
        if "tools" in low and "isn't" in low:
            line1 = _short(p.split(".")[0] + ".")
            if i + 1 < len(paragraphs):
                line2 = _short(paragraphs[i + 1].split(".")[0] + ".")
            break
        if "not the tools" in low or "interesting part" in low:
            line1 = _short(p)
            if i + 1 < len(paragraphs):
                line2 = _short(paragraphs[i + 1])
            break
        if "output" in low and "learn" in " ".join(paragraphs).lower():
            line1 = "Everyone optimizes for output."
            line2 = "Few optimize for decision quality."
            break
    return {
        "name": "Contrast",
        "layout": "fcp_data",
        "line1": line1,
        "line2": line2,
        "data_items": _data_items(idea.get("post_type", ""), paragraphs),
        "flow_items": _flow_items(idea.get("post_type", ""), idea.get("pillar", "")),
    }


def _slide5(idea: dict, paragraphs: list[str]) -> dict:
    c1, c2 = _find_contrast(paragraphs)
    c1b = ""
    c2b = c2
    if " isn't " in c1.lower() or " is not " in c1.lower():
        challenge1 = "The challenge isn't:"
        challenge1b = c1
        challenge2 = "The challenge is:"
        challenge2b = c2
    else:
        challenge1 = c1
        challenge1b = ""
        challenge2 = "The real question:"
        challenge2b = c2
    return {
        "name": "Challenge",
        "layout": "fcp_challenge",
        "challenge1": challenge1,
        "challenge1b": challenge1b,
        "challenge2": challenge2,
        "challenge2b": challenge2b,
    }


def _slide6(idea: dict, paragraphs: list[str]) -> dict:
    q = _find_question(paragraphs, idea.get("hook", ""))
    return {
        "name": "Question",
        "layout": "fcp_question",
        "intro": "This creates a question:",
        "question": q,
    }


def _slide7(idea: dict, paragraphs: list[str]) -> dict:
    pillar = idea.get("pillar", "Decision Quality")
    post_type = idea.get("post_type", "Research")
    headline = f"We're exploring this at Hustronix."
    for p in paragraphs:
        if "hustronix" in p.lower():
            headline = _short(p, 90)
            break
    if post_type == "Builder":
        headline = "We're building Decision Intelligence in public."

    points = []
    humility = ("still exploring", "still learning", "still figuring", "curious", "not sure", "keeps showing up")
    for p in paragraphs[-4:]:
        low = p.lower()
        if any(h in low for h in humility):
            words = p.split()
            if len(words) > 3:
                mid = " ".join(words[:2]).rstrip(".")
                rest = " ".join(words[2:])
                points.append((mid.capitalize(), rest))
    if not points:
        points = [
            ("Still", "exploring this idea."),
            ("Still", "learning from founders."),
            ("It keeps showing up in", "conversations."),
        ]
    return {
        "name": "CTA",
        "layout": "fcp_cta",
        "headline": headline,
        "points": points[:3],
        "cta": "Building in public.",
    }


def slides_from_post(idea: dict) -> list[dict]:
    """Build 7 intelligent slides from hook + body + metadata."""
    body = idea.get("body", "") or idea.get("hook", "")
    hook = idea.get("hook", "")
    paragraphs = _paragraphs(body, hook)
    if not paragraphs:
        paragraphs = [_clean(hook)]

    return [
        _slide1(idea, paragraphs),
        _slide2(idea, paragraphs),
        _slide3(idea, paragraphs),
        _slide4(idea, paragraphs),
        _slide5(idea, paragraphs),
        _slide6(idea, paragraphs),
        _slide7(idea, paragraphs),
    ]


def brief_metadata(idea: dict) -> dict:
    return {
        "series_title": _series_title(idea),
        "story": "post_intelligent",
    }
