"""Voice quality validation tests for Founder Voice v2.0."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from lib.linkedin_posts import (  # noqa: E402
    count_uncertainty,
    enforce_voice_quality,
    validate_voice,
    word_count,
)


def test_count_uncertainty_zero_on_clean_text():
    text = "Founders confuse activity with progress. One team shipped 12 features in a month."
    assert count_uncertainty(text) == 0


def test_count_uncertainty_detects_stacked_hedging():
    text = "Still exploring this idea. Curious what others think."
    assert count_uncertainty(text) >= 2


def test_validate_voice_flags_forbidden_phrases():
    text = "Hot take: AI will replace everyone. Follow for more."
    hits = validate_voice(text)
    assert len(hits) >= 2


def test_validate_voice_allows_one_uncertainty():
    text = "Decision infrastructure matters. I could be wrong about the scale."
    hits = validate_voice(text)
    assert "too_many_uncertainty_statements" not in str(hits)


def test_enforce_voice_quality_strips_forbidden():
    idea = {"id": 1, "title": "Decision loops", "pillar": "contrarian"}
    dirty = "Hot take.\n\nFounders need decision infrastructure.\n\nFollow for more."
    clean = enforce_voice_quality(dirty, idea)
    assert validate_voice(clean) == [] or "hot take" not in clean.lower()


def test_word_count_basic():
    assert word_count("one two three") == 3
