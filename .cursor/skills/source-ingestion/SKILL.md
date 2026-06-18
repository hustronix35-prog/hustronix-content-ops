---
name: source-ingestion
description: Ingest URLs, articles, transcripts, and manual content into raw_sources vault. Use when user says ingest, add source, or paste content for research.
---

# Source Ingestion

Collect high-signal information into the Knowledge Vault.

## Triggers

- Slack: `ingest {url}`
- Daily automation (7am)
- Manual: user pastes content or provides file path

## Priority Sources

1. Founder interviews (manual — highest value)
2. YC videos, articles, interviews
3. OpenAI / Anthropic research and announcements
4. Startup founder LinkedIn posts, blogs
5. Podcast show notes (Lenny, 20VC, Acquired, Latent Space)

## Procedure

### URL ingest

```bash
python scripts/ingest_url.py "{url}" --type article --tags "yc,decision-quality"
```

### File / transcript ingest

```bash
python scripts/ingest_url.py --file vault/founder_interviews/{file}.md --type founder_interview --title "Interview with {name}"
```

### Verify

```bash
python scripts/vault_query.py list raw_sources --limit 5
```

## Output

- Row in `raw_sources` table (processed=0)
- Markdown file at `vault/raw_sources/{id}.md`

## Rules

- Always set meaningful `source_type` and `tags`
- Founder interviews: use type `founder_interview`
- Do not process insights here — research-agent handles that
