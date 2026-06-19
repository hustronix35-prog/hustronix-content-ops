"""Generate LinkedIn posts in Founder Voice v1.0."""

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

OPENINGS = [
    "One thing I've noticed while talking to founders.",
    "Something interesting came up this week.",
    "I've been thinking about this while building Hustronix.",
    "After talking to a few founders recently.",
    "A pattern I'm starting to see.",
    "This surprised me a little.",
    "We've been experimenting with something on our side.",
    "I used to think about this differently.",
]

ENDINGS = [
    "Still exploring this idea.",
    "Curious what others think.",
    "Not sure if this is broadly true yet, but it keeps showing up.",
    "Would love to hear how others approach this.",
    "Still trying to understand the pattern.",
    "This feels important, but I'm still figuring out the edges.",
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


def pick_ending(idea: dict) -> str:
    idx = ((idea.get("id") or 0) + 3) % len(ENDINGS)
    return ENDINGS[idx]


def validate_voice(text: str) -> list[str]:
    lower = text.lower()
    hits = []
    for pattern in FORBIDDEN_PHRASES:
        if re.search(pattern, lower, re.MULTILINE):
            hits.append(pattern)
    return hits


def trim_to_word_range(text: str, min_words: int, max_words: int) -> str:
    text = text.strip()
    max_words = min(max_words, ABSOLUTE_MAX_WORDS)
    wc = word_count(text)
    if wc > max_words:
        words = text.split()
        trimmed = " ".join(words[:max_words])
        return trimmed
    if wc < min_words:
        gap = min_words - wc
        return f"{text}\n\n{_humility_padding(gap)}"
    return text


def _humility_padding(gap: int) -> str:
    lines = [
        "I'm still trying to understand whether this pattern holds at scale.",
        "It might be specific to the founders I've spoken with so far.",
        "Still exploring this idea.",
        "Curious what others think.",
    ]
    out: list[str] = []
    count = 0
    i = 0
    while count < gap and i < len(lines) * 3:
        line = lines[i % len(lines)]
        out.append(line)
        count += word_count(line)
        i += 1
    return "\n\n".join(out)


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
    opening = pick_opening(idea)
    ending = pick_ending(idea)
    hook = idea["hook"]

    return f"""{opening}

{hook}

Most founders I talk to aren't lacking information.

They have dashboards, reports, and customer feedback.

The hard part is deciding what actually matters.

I'm starting to think that's a different problem than execution.

{ending}"""


def _default_body(idea: dict) -> str:
    opening = pick_opening(idea)
    ending = pick_ending(idea)
    hook = idea["hook"]
    pillar = idea["pillar"]
    post_type = idea["post_type"]
    source_type = idea.get("source_type", "research")

    if source_type == "founder" or post_type == "Interview":
        return f"""{opening}

{hook}

After a few founder conversations this month, a pattern keeps showing up.

They have more signal than ever — customer calls, pipeline data, product metrics.

But when a real decision comes up, the context still lives in one person's head.

I'm starting to believe the next layer of startup software won't be about collecting more information.

It will be about helping teams decide with shared context.

While working on Hustronix, I keep coming back to a simple loop:
what triggered the decision, what was chosen, what happened, what we learned.

Not sure we've built enough products around that yet.

{ending}"""

    if source_type == "building" or post_type == "Builder":
        return f"""While working on Hustronix this week, something shifted in how I think about our marketing.

{hook}

We could optimize for output — more posts, more impressions.

But that's not what we're trying to learn.

We're trying to understand how founders make decisions under uncertainty.

So we run our marketing like a research loop:
notice something, form a hypothesis, decide what to publish, see what conversations it starts.

Last week we killed a post angle that might have performed well but didn't feel honest.

That felt like the right call.

I'm still figuring out how to share that process without sounding like we're performing "building in public."

{ending}"""

    if post_type == "Contrarian":
        return f"""{opening}

{hook}

We spend a lot of time measuring execution — velocity, output, activity.

I wonder if we spend enough time measuring decision quality.

As startups grow, I've noticed decisions get harder.

Not because people become less capable.

Because context gets scattered.

Sales sees one slice.
Product sees another.
The founder still holds the full picture.

I'm starting to think slowdown often shows up before anyone identifies it as a decision problem.

{ending}"""

    if post_type == "Framework":
        return f"""{opening}

{hook}

I've been trying to name something I see in early-stage teams.

When the company is small, decisions are fast because context is shared by default.

When it grows, the same decisions take longer — not because people work less, but because nobody shares the same model of reality.

I've started using a simple frame:
trigger, decision, outcome, lesson.

Not as a process doc.

As a way to check whether a decision is still connected to why it was made.

I'm still early in understanding how useful this is outside our own work at Hustronix.

{ending}"""

    return f"""{opening}

{hook}

I've been reading and talking to founders about {pillar.lower()}.

The interesting part isn't the tools.

It's what happens when teams scale and decisions stop feeling shared.

Founders describe the same texture:
"We're moving, but alignment got harder."

I'm starting to think that's less about execution discipline and more about decision clarity.

Something I'm noticing in our research at Hustronix — the gap shows up long before teams name it as a problem.

{ending}"""


def _deep_body(idea: dict) -> str:
    opening = pick_opening(idea)
    ending = pick_ending(idea)
    hook = idea["hook"]
    pillar = idea["pillar"]
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

Those aren't marketing questions.

They're product questions about what kind of company we're building.

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

I'm starting to believe that's the bar for us:
does this post help us learn something true about decision-making at startups?

If not, it's noise — even if it's "good content."

I'm still figuring out how to do this consistently without turning every week into meta-commentary about marketing.

But the direction feels right.

We're not trying to sound like a content creator.

We're trying to sound like founders studying a problem while building toward it.

{ending}"""

    return f"""{opening}

{hook}

I've spent the last few months on {pillar.lower()} — mostly through founder conversations, not surveys.

Here's what I think I'm seeing.

Stage one: the founder is in every decision.

Context is ambient. Tradeoffs get resolved quickly because one person holds product, GTM, and strategy together.

Stage two: the team grows.

Customer conversations multiply. Functions form. Dashboards appear.

Execution looks healthy — maybe even faster in pockets.

But strategic decisions start taking longer.

Founders often describe this as a hiring problem or a process problem.

I'm not sure it is.

What I hear underneath is fragmentation.

Sales learns one story from the market.
Product learns another from usage.
The founder still connects the dots — alone.

I'm starting to think the slowdown isn't about effort.

It's about disconnected judgment.

That's the pattern we're exploring at Hustronix.

Not another tool for generating more output.

Something that helps teams preserve why a decision was made — so they're not re-deciding the same thing every quarter.

I don't think we have the full answer yet.

But the question feels worth sitting with:
can your team explain your last three major decisions without you in the room?

If the honest answer is no, I wonder if that's where the friction is coming from.

{ending}"""


def post_from_idea(idea: dict, tier: str = "default") -> dict:
    spec = LENGTH_TIERS.get(tier, LENGTH_TIERS["default"])
    builders = {
        "default": _default_body,
        "short": _short_body,
        "deep": _deep_body,
    }
    body = builders.get(tier, _default_body)(idea)
    body = trim_to_word_range(body, spec["min_words"], spec["max_words"])
    wc = word_count(body)
    if wc > ABSOLUTE_MAX_WORDS:
        body = trim_to_word_range(body, spec["min_words"], ABSOLUTE_MAX_WORDS)
        wc = word_count(body)
    voice_flags = validate_voice(body)
    return {
        "body": body,
        "word_count": wc,
        "length_tier": tier,
        "tier_label": spec["label"],
        "voice_flags": voice_flags,
    }


def short_post_from_idea(idea: dict, ctx: dict | None = None) -> str:
    return post_from_idea(idea, "default")["body"]
