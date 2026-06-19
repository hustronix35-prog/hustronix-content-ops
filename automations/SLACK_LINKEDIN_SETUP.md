# Slack → LinkedIn workflow (select → carousel → publish)

## Daily flow (3 steps in Slack)

**7:00 AM** — Daily Research Pipeline posts 3 text options.

| Step | You reply | What happens |
|------|-----------|----------------|
| 1 | `select 2` | Locks in option 2 as your post |
| 2 | `carousel` | Generates 6 brand slides → **uploads PNGs to Slack** |
| 3 | `publish` | Posts **text + carousel images** to LinkedIn |

Step 2 is optional — skip it and `publish` posts text only.

---

## One automation (replace old approve/carousel automations)

Import: **`automations/prefill/slack-post-workflow.json`**

**Slack trigger keywords:** `select 1`, `select 2`, `select 3`, `carousel`, `publish`

| Setting | Value |
|---------|--------|
| Send to Slack | ON → `#marketing-os` |
| Ignore thread replies | ON |
| Authenticated users only | ON |
| Repo | `hustronix35-prog/marketing-os` |

Also keep **Daily Research Pipeline** on schedule (no Slack trigger).

---

## Secrets (Cursor Automation → Environment)

### LinkedIn (required for `publish`)

| Secret | How to get |
|--------|------------|
| `LINKEDIN_ACCESS_TOKEN` | [LinkedIn Developer](https://www.linkedin.com/developers/apps) → OAuth, scope `w_member_social` |
| `LINKEDIN_AUTHOR_URN` | `urn:li:person:{id}` from `/v2/userinfo` |

### Slack (required for carousel upload to channel)

| Secret | How to get |
|--------|------------|
| `SLACK_BOT_TOKEN` | [Slack API](https://api.slack.com/apps) → Create app → Bot Token `xoxb-...` |
| `SLACK_CHANNEL_ID` | Right-click `#marketing-os` → View channel details → copy ID (`C...`) |

**Bot scopes needed:** `files:write`, `chat:write`, `channels:read`

Invite the bot to `#marketing-os`: `/invite @YourBotName`

Without Slack secrets, carousel still generates locally — automation tells you to add secrets or use `preview.html`.

---

## Example thread

```
Bot:  [3 post options...]
You:  select 2
Bot:  Selected OPTION 2. Reply carousel or publish.
You:  carousel
Bot:  [6 PNG slides uploaded]. Reply publish to post on LinkedIn.
You:  publish
Bot:  Published OPTION 2 to LinkedIn (text + 6 images).
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No post selected" | Run `select 1` first |
| Carousel not in Slack | Add `SLACK_BOT_TOKEN` + `SLACK_CHANNEL_ID`, invite bot |
| LinkedIn 401 | Refresh OAuth token |
| Images not on LinkedIn | Token needs `w_member_social`; multi-image uses asset upload API |
| Wrong repo | `hustronix35-prog/marketing-os` |

---

## What you don't need

- Terminal for daily use
- Separate approve / carousel automations (one workflow automation handles all commands)
- Manual PNG upload to LinkedIn (if `publish` succeeds with images)
