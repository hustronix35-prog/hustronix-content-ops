# Architecture — Hustronix Content Ops

## System Components

```mermaid
graph LR
    subgraph Presentation
        SL[Slack UI]
        LI[LinkedIn]
        HTML[Carousel HTML/PNG]
    end

    subgraph Application
        WF[slack_post_workflow.py]
        RP[run_daily_pipeline.py]
        GPO[generate_post_options.py]
        GC[generate_carousel.py]
    end

    subgraph Domain
        LP[linkedin_posts.py]
        CI[carousel_intelligence.py]
        CR[carousel_renderer.py]
        PW[post_workflow.py]
    end

    subgraph Data
        DB[(SQLite)]
        VAULT[vault/]
    end

    SL --> WF
    WF --> GPO
    WF --> GC
    WF --> LI
    GPO --> LP
    GC --> CI
    GC --> CR
    WF --> PW
    PW --> DB
    RP --> DB
    RP --> VAULT
```

| Component | Responsibility |
|-----------|----------------|
| **Vault (SQLite)** | Sources, insights, ideas, drafts, post options, workflow state |
| **Vault (markdown)** | Long-form artifacts, learning, published distribution notes |
| **Pipeline scripts** | Orchestrate daily research → options → digest |
| **Post generator** | Founder Voice v2.0 body generation with quality enforcement |
| **Carousel intelligence** | Derive 7 slides from hook + body + metadata |
| **Carousel renderer** | Playwright PNG export from HTML/CSS/SVG |
| **Slack upload** | External file upload API for PNG review |
| **LinkedIn media** | UGC API text + multi-image posts |
| **Cursor skills** | Agent behavior specs (research, writer, design, analytics) |
| **Automations** | Cron + Slack triggers for cloud execution |

---

## Data Flow

### Daily generation

```mermaid
flowchart TD
    A[raw_sources processed=0] --> B[research_insights]
    B --> C[content_ideas pending]
    C --> D[generate_post_options.py]
    D --> E[daily_post_options x3]
    E --> F[Slack message]
```

### Publish flow

```mermaid
flowchart TD
    S[select N] --> ST[(status=selected)]
    C[carousel] --> R[generate_carousel.py]
    R --> P[PNG slides]
    P --> U[slack_upload.py]
    PUB[publish] --> L[linkedin_media.py]
    ST --> PUB
    L --> ST2[(status=published)]
```

---

## Dependencies

| Dependency | Role |
|------------|------|
| Python 3.12+ | Runtime |
| Playwright + Chromium | Headless PNG render |
| PyYAML | Design brief parsing |
| stdlib sqlite3, urllib | DB + HTTP APIs |

No web framework. CLI-first architecture.

---

## External Integrations

| Service | Integration | Auth |
|---------|-------------|------|
| **LinkedIn** | UGC Posts + Asset Upload | OAuth bearer token |
| **Slack** | Message triggers + file upload | Bot token |
| **Cursor Cloud** | Agent execution + automations | Platform auth |
| **GitHub** | Source + CI | Actions |

---

## Failure Points

| Failure | Impact | Mitigation |
|---------|--------|------------|
| LinkedIn token expiry | Publish fails | Regenerate token; document in SECURITY.md |
| Slack upload `invalid_arguments` | No PNG in channel | Form-encoded API (fixed in slack_upload.py) |
| Playwright missing | No PNG render | `setup_carousel_env.py` |
| Empty vault | Stale post options | Seed + ingestion pipeline |
| Cursor secrets not injected | Cloud publish fails | Dashboard secrets + local `.env` fallback |
| Voice rule regression | Mediocre posts | `validate_voice()` + content-feedback.md |

---

## Scaling Considerations

**Current:** Single-founder, single SQLite file, single Slack channel.

**Scale path:**

1. Postgres + row-level tenant isolation
2. Queue-based job runner (carousel render is CPU-heavy)
3. S3 for generated assets
4. Webhook router instead of Slack-only triggers
5. Cached post generation with idempotency keys

---

## Security Considerations

- Secrets in `.env` / Cursor Dashboard only — never committed
- Slack bot scoped to `files:write`, `chat:write`, `channels:read`
- LinkedIn `w_member_social` minimum scope
- Private Slack channel exposes data in automation run history (documented)
- No SQL injection risk (parameterized queries throughout)
- Sample founder data in vault is synthetic/demo

See [SECURITY.md](SECURITY.md).

---

## Future Architecture

```mermaid
flowchart TB
    subgraph v2["Content Ops v2"]
        API[FastAPI gateway]
        Q[Job queue]
        PG[(Postgres)]
        S3[S3 assets]
    end

    subgraph v3["Hustronix Native"]
        DI[Decision Intelligence core]
        SIG[Signal engine]
    end

    CO[Content Ops v1] --> API
    API --> Q
    Q --> PG
    DI --> CO
    SIG --> DI
```

See [docs/V3_HUSTRONIX_NATIVE.md](V3_HUSTRONIX_NATIVE.md).
