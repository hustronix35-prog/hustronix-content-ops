# GitHub repo polish checklist

## Fix broken CI badge / "workflow does not exist"

1. **Enable Actions** — Repo → **Settings** → **Actions** → **General** → allow actions
2. **Run CI once** — **Actions** tab → **CI** → **Run workflow** → Run
3. Badge in README points to `ci.yml` (runs on every push)

## Add repo logo (GitHub profile image)

1. Repo → **Settings** → scroll to **Social preview**
2. Upload `assets/brand/logo-icon.svg` or `logo-lockup.png` (1280×640 works best for social card)
3. Or: first image in README (`logo-lockup.png`) is used as Open Graph preview

## Add description & topics

**Settings** → **General** → Description:

> Decision Intelligence marketing OS — Slack approval, voice quality gates, intelligent LinkedIn carousels.

**Topics:** `marketing-automation`, `linkedin`, `slack`, `decision-intelligence`, `python`, `cursor`, `playwright`, `startup`

## Replace screenshot placeholders

Capture real `#marketing-os` Slack thread + `assets/generated/*/preview.html` and save to `docs/assets/`.
