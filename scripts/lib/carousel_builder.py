"""Build premium carousel slide content from ideas."""

from __future__ import annotations

from lib.carousel_intelligence import brief_metadata, slides_from_post


def visual_category(idea: dict) -> str:
    if idea.get("source_type") == "founder":
        return "founder_insight" if idea.get("post_type") == "Interview" else "decision_pattern"
    if idea.get("post_type") in ("Framework", "Contrarian"):
        return "execution_model"
    if idea.get("post_type") == "Research":
        return "decision_pattern"
    if idea.get("post_type") == "Builder":
        return "founder_insight"
    return "future_of_organizations"


def build_slides(idea: dict, visual_type: str = "carousel", story: str | None = None) -> tuple[str, list[dict]]:
    hook = idea.get("hook", "Decision Intelligence for founders")
    if visual_type == "single_image":
        meta = brief_metadata(idea)
        return visual_category(idea), [
            {
                "name": "Insight",
                "layout": "fcp_hook",
                "line1": hook,
                "line2": "",
                "footer_note": "Hustronix — Decision Intelligence",
            }
        ]

    cat = visual_category(idea)
    slides = slides_from_post(idea)
    return cat, slides


def build_brief(idea: dict, visual_type: str = "carousel", story: str | None = None) -> dict:
    cat, slides = build_slides(idea, visual_type, story=story)
    meta = brief_metadata(idea)
    return {
        "topic": idea.get("pillar", "Decision Quality"),
        "audience": "Seed-Series B Founders",
        "visual_type": "Intelligent Post Carousel" if visual_type == "carousel" else "Single Image",
        "visual_category": cat,
        "story": meta["story"],
        "series_title": meta["series_title"],
        "brand_rules": {
            "background": "#0A0A0A",
            "typography": "#EDEDED",
            "accent": "#D4AF37",
            "font": "Inter",
        },
        "layout": "Post-intelligent v1.0 — graphics derived from selected post",
        "hook": idea.get("hook", ""),
        "post_body": idea.get("body", ""),
        "slides": slides,
    }
