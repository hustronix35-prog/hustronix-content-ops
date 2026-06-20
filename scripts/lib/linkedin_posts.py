"""Generate LinkedIn posts in Founder Voice v2.0 — strict anti-mediocrity gate."""

from __future__ import annotations

import re

LENGTH_TIERS = {
    "default": {
        "label": "Default",
        "min_words": 180,
        "max_words": 300,
        "target_share": 0.70,
        "slack_hint": "180–300 words · most posts",
    },
    "short": {
        "label": "Short",
        "min_words": 80,
        "max_words": 150,
        "target_share": 0.20,
        "slack_hint": "80–150 words · quick observation",
    },
    "deep": {
        "label": "Deep",
        "min_words": 300,
        "max_words": 500,
        "target_share": 0.10,
        "slack_hint": "300–500 words · research / building lesson",
    },
}

ABSOLUTE_MAX_WORDS = 500
MAX_UNCERTAINTY_STATEMENTS = 1

OPENINGS = [
    "I've been talking to founders over the last few weeks while building Hustronix.",
    "One thing I've noticed while talking to founders.",
    "While working on Hustronix, something keeps showing up in conversations.",
    "After a few founder conversations this month, a pattern keeps showing up.",
    "A pattern I'm starting to see while building Hustronix.",
]

CLOSINGS = [
    "That's a pattern I'm paying close attention to right now.",
    "I'm starting to think many execution problems begin as decision problems.",
    "That feels like the right question to sit with for a while.",
]

FORBIDDEN_PHRASES = [
    r"hot take",
    r"unpopular opinion",
    r"nobody talks about",
    r"here's what i learned",
    r"let that sink in",
    r"game changer",
    r"ai will replace",
    r"this changes everything",
    r"follow for more",
    r"^thoughts\?$",
    r"^agree\?$",
    r"like and share",
    r"comment below",
    r"what's your take",
    r"in today's fast-paced world",
    r"let's dive in",
    r"revolutionary",
    r"game-changing",
    r"10x your growth",
    r"curious what others think",
    r"still exploring this idea",
    r"i could be wrong",
    r"not sure if this is broadly true",
    r"i'm still trying to understand whether this pattern holds at scale",
    r"it might be specific to the founders i've spoken with so far",
]

UNCERTAINTY_PATTERNS = [
    r"curious what others think",
    r"still exploring this idea",
    r"i could be wrong",
    r"not sure if this is broadly true",
    r"i'm still trying to understand whether",
    r"it might be specific to the founders",
    r"still trying to understand the pattern",
    r"still figuring out how to",
    r"i don't think we have the full answer yet",
    r"would love to hear how others",
    r"this feels important, but i'm still",
]


def word_count(text: str) -> int:
    return len(text.split())


def classify_tier(wc: int) -> str:
    if wc <= 150:
        return "short"
    if wc <= 300:
        return "default"
    return "deep"


def pick_opening(idea: dict) -> str:
    idx = (idea.get("id") or 0) % len(OPENINGS)
    return OPENINGS[idx]


def pick_closing(idea: dict) -> str:
    idx = ((idea.get("id") or 0) + 2) % len(CLOSINGS)
    return CLOSINGS[idx]


def validate_voice(text: str) -> list[str]:
    lower = text.lower()
    hits = []
    for pattern in FORBIDDEN_PHRASES:
        if re.search(pattern, lower, re.MULTILINE):
            hits.append(pattern)
    if count_uncertainty(text) > MAX_UNCERTAINTY_STATEMENTS:
        hits.append(f"too_many_uncertainty_statements>{MAX_UNCERTAINTY_STATEMENTS}")
    return hits


def count_uncertainty(text: str) -> int:
    lower = text.lower()
    count = 0
    for pattern in UNCERTAINTY_PATTERNS:
        count += len(re.findall(pattern, lower))
    return count


def _split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def _join_paragraphs(paragraphs: list[str]) -> str:
    return "\n\n".join(paragraphs)


def _normalize_para(para: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", para.strip().lower()))


def _paragraph_in_text(para: str, text: str) -> bool:
    a = _normalize_para(para)
    b = _normalize_para(text)
    if not a or len(a) < 12:
        return False
    return a in b or any(a in _normalize_para(p) for p in _split_paragraphs(text))


def _dedupe_paragraphs(paragraphs: list[str]) -> list[str]:
    seen: list[str] = []
    for para in paragraphs:
        if any(_paragraph_in_text(para, s) for s in seen):
            continue
        seen.append(para)
    return seen


def enforce_voice_quality(text: str, idea: dict) -> str:
    """Remove banned phrases and cap uncertainty at one statement."""
    paragraphs = _dedupe_paragraphs(_split_paragraphs(text))
    cleaned: list[str] = []
    uncertainty_used = 0

    for para in paragraphs:
        lower = para.lower()
        skip = False
        for pattern in FORBIDDEN_PHRASES:
            if re.search(pattern, lower):
                skip = True
                break
        if skip:
            continue

        is_uncertain = any(re.search(p, lower) for p in UNCERTAINTY_PATTERNS)
        if is_uncertain:
            if uncertainty_used >= MAX_UNCERTAINTY_STATEMENTS:
                continue
            uncertainty_used += 1
        cleaned.append(para)

    if not cleaned:
        cleaned = _dedupe_paragraphs(_split_paragraphs(text))[:1] or [text]

    joined = _join_paragraphs(cleaned)
    last = cleaned[-1].lower()
    has_closing = any(
        phrase in joined.lower()
        for phrase in (
            "paying close attention",
            "begin as decision problems",
            "right question to sit with",
            "right call",
            "decisions matter more than the output",
        )
    )
    if not has_closing and count_uncertainty(joined) == 0:
        cleaned.append(pick_closing(idea))

    return _join_paragraphs(_dedupe_paragraphs(cleaned))


def trim_to_word_range(text: str, min_words: int, max_words: int, idea: dict) -> str:
    text = enforce_voice_quality(text, idea)
    max_words = min(max_words, ABSOLUTE_MAX_WORDS)
    wc = word_count(text)
    if wc > max_words:
        words = text.split()
        text = " ".join(words[:max_words])
        text = enforce_voice_quality(text, idea)
    elif wc < min_words:
        text = _extend_with_substance(text, idea, min_words - wc)
    return enforce_voice_quality(text, idea)


def _extend_with_substance(text: str, idea: dict, gap: int) -> str:
    """Add concrete example lines — never pad with repeated humility."""
    pillar = idea.get("pillar", "Decision Quality")
    post_type = idea.get("post_type", "Research")
    extras = {
        "Contrarian": [
            "When we talk to founders about where slowdown actually starts, the answer is rarely we need more tools.",
            "It's usually that teams are re-deciding the same thing because context didn't travel.",
            "That shows up before anyone calls it a hiring problem or a process problem.",
        ],
        "Builder": [
            "The loop only works if we're honest about what we're trying to learn — not what will perform.",
            "Dogfooding means killing angles that score well but don't feel true.",
            "That's the bar we're holding ourselves to while building Hustronix.",
        ],
        "Research": [
            "In three separate conversations this month, founders described the same texture.",
            "That showed up before anyone called it a process problem.",
            "The gap appears long before teams name it as a decision problem.",
        ],
        "Framework": [
            "Trigger. Decision. Outcome. Lesson.",
            "Not as a process doc — as a way to check whether a decision still connects to why it was made.",
        ],
    }
    lines = extras.get(post_type, extras.get("Contrarian", []))
    if pillar == "Founder Context":
        lines = [
            "Sales sees one part.",
            "Product sees another.",
            "Leadership tries to connect everything.",
        ]
    out = _dedupe_paragraphs(_split_paragraphs(text))
    text_blob = _join_paragraphs(out).lower()
    added = 0
    i = 0
    insert_at = max(len(out) - 1, 0) if out else 0
    while added < gap and i < len(lines) * 3:
        line = lines[i % len(lines)]
        norm = _normalize_para(line)
        if norm and norm not in _normalize_para(text_blob) and not any(
            _paragraph_in_text(line, p) for p in out
        ):
            out.insert(insert_at, line)
            insert_at += 1
            text_blob = _join_paragraphs(out).lower()
            added += word_count(line)
        i += 1
    return _join_paragraphs(_dedupe_paragraphs(out))


def pick_tiers_for_batch(conn, ideas: list) -> list[str]:
    tiers = ["default", "default", "default"]
    if not ideas:
        return tiers

    rows = conn.execute(
        """SELECT body FROM daily_post_options
           WHERE status = 'published' ORDER BY published_at DESC LIMIT 30"""
    ).fetchall()
    if not rows:
        return tiers

    history = [classify_tier(word_count(r["body"])) for r in rows]
    total = len(history)
    short_pct = history.count("short") / total
    deep_pct = history.count("deep") / total

    short_slot: int | None = None
    deep_slot: int | None = None

    if short_pct < 0.15:
        for i, idea in enumerate(ideas[:3]):
            if idea.get("post_type") in ("Contrarian", "Builder", "Research"):
                short_slot = i
                break

    if deep_pct < 0.08:
        for i, idea in enumerate(ideas[:3]):
            src = idea.get("source_type", "")
            ptype = idea.get("post_type", "")
            if src in ("founder", "building", "research") or ptype in (
                "Interview",
                "Framework",
                "Research",
            ):
                deep_slot = i
                break

    if deep_slot is not None and deep_slot != short_slot:
        tiers[deep_slot] = "deep"
    elif short_slot is not None:
        tiers[short_slot] = "short"

    return tiers


def _short_body(idea: dict) -> str:
    hook = idea["hook"]
    return f"""{hook}

Most founders I talk to aren't lacking information.

They have dashboards, reports, and customer feedback.

The hard part is deciding what actually matters when a decision has to be made.

I'm starting to think that's a different problem than execution.

{pick_closing(idea)}"""


def _contrarian_body(idea: dict) -> str:
    hook = idea["hook"]
    # Gold-standard structure from content-feedback.md
    line1, line2 = hook, ""
    if ". " in hook:
        parts = hook.split(". ", 1)
        line1 = parts[0].rstrip(".") + "."
        line2 = parts[1]
    elif hook.count(".") >= 1:
        line1 = hook
    else:
        line1 = hook
        line2 = "Your decision infrastructure might be."

    opening = pick_opening(idea)
    return f"""{line1}
{line2}

{opening}

Teams have more information than ever.

Customer feedback.
Product analytics.
Revenue dashboards.
Internal docs.

The challenge isn't collecting information.

It's knowing what matters when a decision has to be made.

As companies grow, context gets fragmented.

Sales sees one part.
Product sees another.
Leadership tries to connect everything.

When we talk to founders about where slowdown actually starts, the answer is rarely "we need more tools."

It's usually that teams are re-deciding the same thing because context didn't travel.

I'm starting to think many execution problems begin as decision problems.

That's a pattern I'm paying close attention to right now."""


def _builder_body(idea: dict) -> str:
    hook = idea["hook"]
    return f"""While working on Hustronix this week, something shifted in how I think about our marketing.

{hook}

We could optimize for output — more posts, more impressions.

But that's not what we're trying to learn.

We're trying to understand how founders make decisions under uncertainty.

So we run our marketing like a research loop:
notice something, form a hypothesis, decide what to publish, see what conversations it starts.

Last week we killed a post angle that might have performed well but didn't feel honest.

That felt like the right call.

We're sharing the process because the decisions matter more than the output."""


def _research_body(idea: dict) -> str:
    hook = idea["hook"]
    pillar = idea.get("pillar", "Decision Quality")
    return f"""{pick_opening(idea)}

{hook}

In three separate conversations this month, founders described the same texture.

Not a tooling gap — a judgment gap.

One founder put it plainly: "We're moving, but alignment got harder."

They had customer calls, pipeline data, and product metrics.

When a real strategic call came up, the context still lived in one person's head.

That's what I'm tracking in our {pillar.lower()} research at Hustronix.

The interesting part isn't whether teams have enough dashboards.

It's whether anyone can explain why the last major decision was made without the founder in the room.

I'm starting to think slowdown often shows up before anyone names it as a decision problem.

{pick_closing(idea)}"""


def _framework_body(idea: dict) -> str:
    hook = idea["hook"]
    return f"""{pick_opening(idea)}

{hook}

When the company is small, decisions are fast because context is shared by default.

When it grows, the same decisions take longer — not because people work less, but because nobody shares the same model of reality.

I've started using a simple frame:
trigger, decision, outcome, lesson.

Not as a process doc.

As a way to check whether a decision is still connected to why it was made.

We tried this on our own roadmap calls at Hustronix last month.

It surfaced two decisions we'd been reopening without realizing it.

{pick_closing(idea)}"""


def _founder_body(idea: dict) -> str:
    hook = idea["hook"]
    return f"""{pick_opening(idea)}

{hook}

After a few founder conversations this month, the same detail keeps appearing.

They have more signal than ever — customer calls, pipeline data, product metrics.

But when a real decision comes up, the context still lives in one person's head.

I'm starting to believe the next layer of startup software won't be about collecting more information.

It will be about helping teams decide with shared context.

While working on Hustronix, I keep coming back to a simple loop:
what triggered the decision, what was chosen, what happened, what we learned.

{pick_closing(idea)}"""


def _default_body(idea: dict) -> str:
    post_type = idea.get("post_type", "Research")
    source_type = idea.get("source_type", "research")

    if post_type == "Contrarian":
        return _contrarian_body(idea)
    if source_type == "building" or post_type == "Builder":
        return _builder_body(idea)
    if post_type == "Research":
        return _research_body(idea)
    if post_type == "Framework":
        return _framework_body(idea)
    if source_type == "founder" or post_type == "Interview":
        return _founder_body(idea)

    return _research_body(idea)


def _deep_body(idea: dict) -> str:
    hook = idea["hook"]
    pillar = idea.get("pillar", "Decision Quality")
    source_type = idea.get("source_type", "research")
    post_type = idea.get("post_type", "Research")

    if source_type == "building" or post_type == "Builder":
        return f"""While working on Hustronix, I've been thinking about what "building in public" should actually mean for us.

{hook}

For a while I assumed it meant sharing progress — what we shipped, what we learned technically.

I'm less convinced that's useful for anyone.

What feels more honest is sharing the decisions we're wrestling with.

Should we optimize for reach or for founder conversations?
Should we publish before we fully understand a pattern?
What do we do when a post idea scores well on engagement but poorly on truth?

We structured our marketing system around the same loop we're trying to sell:
inputs, intelligence, decision, execution.

Research surfaces a signal from founder conversations.
We propose a few post options — not one auto-generated take.
A human approves, because judgment still matters.
Then we publish and pay attention to what conversations start.

What surprised me is how often the right decision is to not publish.

We killed an angle last week that was catchy but generic.

It would have gotten reactions.

It wouldn't have helped us understand founders better.

The bar for us: does this post help us learn something true about decision-making at startups?

We're not trying to sound like a content creator.

We're trying to sound like founders studying a problem while building toward it.

{pick_closing(idea)}"""

    return f"""{pick_opening(idea)}

{hook}

I've spent the last few months on {pillar.lower()} — mostly through founder conversations, not surveys.

Stage one: the founder is in every decision.

Context is ambient. Tradeoffs get resolved quickly because one person holds product, GTM, and strategy together.

Stage two: the team grows.

Customer conversations multiply. Functions form. Dashboards appear.

Execution looks healthy — maybe even faster in pockets.

But strategic decisions start taking longer.

Founders often describe this as a hiring problem or a process problem.

What I hear underneath is fragmentation.

Sales learns one story from the market.
Product learns another from usage.
The founder still connects the dots — alone.

I'm starting to think the slowdown isn't about effort.

It's about disconnected judgment.

That's the pattern we're exploring at Hustronix.

Not another tool for generating more output.

Something that helps teams preserve why a decision was made — so they're not re-deciding the same thing every quarter.

Can your team explain your last three major decisions without you in the room?

If the honest answer is no, that might be where the friction is coming from.

{pick_closing(idea)}"""


def post_from_idea(idea: dict, tier: str = "default") -> dict:
    spec = LENGTH_TIERS.get(tier, LENGTH_TIERS["default"])
    builders = {
        "default": _default_body,
        "short": _short_body,
        "deep": _deep_body,
    }
    body = builders.get(tier, _default_body)(idea)
    body = trim_to_word_range(body, spec["min_words"], spec["max_words"], idea)
    wc = word_count(body)
    if wc > ABSOLUTE_MAX_WORDS:
        body = trim_to_word_range(body, spec["min_words"], ABSOLUTE_MAX_WORDS, idea)
        wc = word_count(body)
    voice_flags = validate_voice(body)
    return {
        "body": body,
        "word_count": wc,
        "length_tier": tier,
        "tier_label": spec["label"],
        "voice_flags": voice_flags,
        "uncertainty_count": count_uncertainty(body),
    }


def short_post_from_idea(idea: dict, ctx: dict | None = None) -> str:
    return post_from_idea(idea, "default")["body"]
