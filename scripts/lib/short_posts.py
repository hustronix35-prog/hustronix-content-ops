"""Back-compat re-exports — use linkedin_posts.py for tier-aware generation."""

from lib.linkedin_posts import (  # noqa: F401
    LENGTH_TIERS,
    classify_tier,
    pick_tiers_for_batch,
    post_from_idea,
    short_post_from_idea,
    word_count,
)
