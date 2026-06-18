#!/usr/bin/env python3
"""Initialize the Hustronix Marketing OS SQLite vault."""

from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "marketing.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS raw_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT NOT NULL,
    source_url TEXT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    date TEXT,
    tags TEXT,
    processed INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS research_insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER REFERENCES raw_sources(id),
    insight TEXT NOT NULL,
    category TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 0.8,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS founders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    company TEXT,
    linkedin_url TEXT,
    founder_stage TEXT,
    company_size TEXT,
    industry TEXT,
    pain_points TEXT,
    interview_count INTEGER NOT NULL DEFAULT 0,
    relationship_score INTEGER NOT NULL DEFAULT 0,
    pilot_interest TEXT NOT NULL DEFAULT 'none',
    first_contact_at TEXT,
    last_contact_at TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS founder_intelligence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    founder_id INTEGER NOT NULL REFERENCES founders(id),
    conversation_date TEXT NOT NULL,
    pain TEXT,
    current_stack TEXT,
    decision_process TEXT,
    biggest_friction TEXT,
    interesting_quotes TEXT,
    product_implications TEXT,
    content_angles TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS decision_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    trigger TEXT NOT NULL,
    decision_made TEXT NOT NULL,
    outcome TEXT,
    why_it_worked TEXT,
    why_it_failed TEXT,
    source TEXT NOT NULL,
    source_id INTEGER,
    confidence REAL NOT NULL DEFAULT 0.8,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS strategic_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    category TEXT NOT NULL,
    founder_id INTEGER REFERENCES founders(id),
    founder_intelligence_id INTEGER REFERENCES founder_intelligence(id),
    context TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    times_seen INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS product_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    founder_intelligence_id INTEGER REFERENCES founder_intelligence(id),
    founder_id INTEGER REFERENCES founders(id),
    requirement TEXT NOT NULL,
    pain_evidence TEXT,
    priority TEXT NOT NULL DEFAULT 'medium',
    status TEXT NOT NULL DEFAULT 'hypothesis',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS feature_hypotheses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_requirement_id INTEGER NOT NULL REFERENCES product_requirements(id),
    hypothesis TEXT NOT NULL,
    validation_method TEXT,
    status TEXT NOT NULL DEFAULT 'untested',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS category_narratives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_of TEXT NOT NULL,
    category_term TEXT NOT NULL,
    current_narrative TEXT,
    emerging_narrative TEXT,
    contrarian_opportunity TEXT,
    content_gap TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS competitor_intel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor TEXT NOT NULL,
    narrative_shift TEXT,
    positioning_change TEXT,
    content_angle TEXT,
    recorded_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS content_ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pillar TEXT NOT NULL,
    post_type TEXT NOT NULL,
    hook TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_id INTEGER,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS content_drafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea_id INTEGER NOT NULL REFERENCES content_ideas(id),
    format TEXT NOT NULL,
    body TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS content_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea_id INTEGER REFERENCES content_ideas(id),
    draft_id INTEGER REFERENCES content_drafts(id),
    founder_relevance INTEGER NOT NULL,
    category_building INTEGER NOT NULL,
    conversation_potential INTEGER NOT NULL,
    di_alignment INTEGER NOT NULL,
    generic_ai_risk INTEGER NOT NULL,
    total_score INTEGER NOT NULL,
    passed INTEGER NOT NULL,
    rejection_reason TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS design_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    draft_id INTEGER NOT NULL REFERENCES content_drafts(id),
    visual_category TEXT,
    clarity INTEGER NOT NULL,
    brand_consistency INTEGER NOT NULL,
    founder_appeal INTEGER NOT NULL,
    di_alignment INTEGER NOT NULL,
    generic_ai_feel INTEGER NOT NULL,
    total_score INTEGER NOT NULL,
    passed INTEGER NOT NULL,
    rejection_reason TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS visual_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    layout_spec TEXT,
    performance_score REAL NOT NULL DEFAULT 0.0,
    example_paths TEXT,
    times_used INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS published_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    draft_id INTEGER NOT NULL REFERENCES content_drafts(id),
    platform TEXT NOT NULL,
    scheduled_at TEXT,
    published_at TEXT,
    url TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS analytics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER REFERENCES published_posts(id),
    impressions INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    reposts INTEGER DEFAULT 0,
    followers_delta INTEGER DEFAULT 0,
    profile_visits INTEGER DEFAULT 0,
    website_clicks INTEGER DEFAULT 0,
    recorded_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS founder_outreach (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    founder_id INTEGER REFERENCES founders(id),
    name TEXT,
    company TEXT,
    linkedin_url TEXT,
    message_draft TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending_review',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_raw_sources_processed ON raw_sources(processed);
CREATE INDEX IF NOT EXISTS idx_research_insights_source ON research_insights(source_id);
CREATE INDEX IF NOT EXISTS idx_founder_intelligence_founder ON founder_intelligence(founder_id);
CREATE INDEX IF NOT EXISTS idx_content_ideas_status ON content_ideas(status);
CREATE INDEX IF NOT EXISTS idx_strategic_questions_times_seen ON strategic_questions(times_seen DESC);
"""

SEED_STRATEGIC_QUESTIONS = [
    ("Should we hire?", "hiring"),
    ("Should we expand market?", "gtm"),
    ("Should we raise?", "fundraising"),
    ("Should we prioritize feature X?", "product"),
    ("Should we kill project Y?", "firing"),
]

SEED_VISUAL_PATTERNS = [
    (
        "decision_pattern_vertical_v1",
        "decision_pattern",
        "Trigger → Decision → Outcome → Lesson vertical flow on #0A0A0A background",
    ),
    (
        "strategic_question_minimal_v1",
        "strategic_question",
        "Large Inter Bold question centered, signal gold accent line",
    ),
    (
        "founder_insight_quote_v1",
        "founder_insight",
        "Large quote #EDEDED, small framework below in soft_grey",
    ),
]


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def seed_canonical_questions(conn: sqlite3.Connection) -> None:
    for question, category in SEED_STRATEGIC_QUESTIONS:
        exists = conn.execute(
            "SELECT 1 FROM strategic_questions WHERE question = ? AND founder_id IS NULL",
            (question,),
        ).fetchone()
        if not exists:
            conn.execute(
                """INSERT INTO strategic_questions (question, category, status, times_seen)
                   VALUES (?, ?, 'recurring', 0)""",
                (question, category),
            )


def seed_visual_patterns(conn: sqlite3.Connection) -> None:
    for name, category, layout_spec in SEED_VISUAL_PATTERNS:
        conn.execute(
            """INSERT OR IGNORE INTO visual_patterns (name, category, layout_spec)
               VALUES (?, ?, ?)""",
            (name, category, layout_spec),
        )


def main() -> None:
    conn = get_connection()
    seed_canonical_questions(conn)
    seed_visual_patterns(conn)
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")


if __name__ == "__main__":
    main()
