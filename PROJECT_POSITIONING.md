# Project Positioning — Hustronix Content Ops

## Elevator Pitch

**Hustronix Content Ops** is an open-source Decision Intelligence system that turns founder research into publish-ready LinkedIn content — with human approval, strict voice quality gates, and zero-terminal daily operations via Slack.

---

## Problem Statement

Founders and early-stage marketing teams face a hidden failure mode: they optimize for **content output** while **decision quality** and **founder context** degrade.

Existing tools automate posting but not judgment. They produce AI-slop: repeated hedging, engagement bait, and clever one-liners without evidence. Teams lack:

- A research-to-publish pipeline tied to real founder conversations
- Quality gates that enforce authentic founder voice
- Workflow state (select → review → publish) without living in terminals
- Reusable infrastructure that compounds into product IP

---

## Solution Overview

Content Ops is a **marketing operating system** built as dogfood for Hustronix's Decision Intelligence thesis:

1. **Vault** — SQLite + markdown store for sources, insights, founders, content ideas
2. **Agents** — Cursor skills for research, strategy, writing, design, analytics
3. **Pipeline** — Daily generation of 3 post options with tiered length and voice rules
4. **Slack workflow** — `select` → `carousel` → `publish` with optional @mention chat for feedback
5. **Carousel engine** — Post-intelligent HTML/CSS/SVG → PNG slides
6. **Learning loop** — Content feedback, analytics, weekly recommendations

---

## Target Users

| Persona | Use case |
|---------|----------|
| **Solo founder** | Daily LinkedIn presence without hiring a content team |
| **Early-stage PMM** | Research-backed posts with approval gates |
| **Startup CTO** | Dogfood decision-infrastructure patterns |
| **Consulting / SPO recruiters** | Portfolio demo of full-stack product engineering |
| **OSS contributors** | Extend voice rules, carousel layouts, integrations |

---

## Key Features

- Founder Voice v2.0 with forbidden-pattern enforcement
- 3 daily post options (180–300w default, strict anti-mediocrity gate)
- Intelligent carousel derived from selected post content
- LinkedIn multi-image publish via API
- Slack PNG upload for carousel review
- 13 agent skills + Cursor Automation prefills
- Founder intelligence DB (target: 100 founders)
- Decision pattern + visual pattern libraries

---

## Value Proposition

| For | Value |
|-----|-------|
| Founders | Sound like a founder, not a content creator |
| Startups | Compound research into distribution without losing judgment |
| Hustronix | Every subsystem becomes reusable product IP |
| Recruiters | End-to-end system design: data, agents, API integrations, CI |

---

## Competitive Advantages

1. **Decision Intelligence framing** — not "AI content generator"
2. **Strict voice QA** — max 1 uncertainty statement; banned engagement bait
3. **Human-in-the-loop by design** — Slack approval, never auto-publish
4. **Post-intelligent carousels** — slides derived from post body, not fixed templates
5. **Agent-native** — skills + rules + automations as first-class artifacts
6. **Open architecture** — SQLite vault, plain Python, minimal dependencies

---

## Category

**Decision Intelligence · Marketing Operations · AI Agent Workflow · Founder-Led Growth Infrastructure**

Comparable mental models: lightweight CMS + workflow engine + brand system + agent orchestration layer.
