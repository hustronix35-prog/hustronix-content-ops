# Duplicate Repository — hustronix-content-ops

This project was transformed from `marketing-os` into **Hustronix Content Ops**. Follow these steps to publish the duplicate on GitHub.

## Option A — GitHub CLI (recommended)

```powershell
# 1. Authenticate (one-time)
gh auth login

# 2. Create new repo from current directory
cd D:\content
gh repo create hustronix35-prog/hustronix-content-ops --public --source=. --remote=content-ops --push

# 3. Set as primary remote (optional)
git remote rename origin marketing-os
git remote rename content-ops origin
git push -u origin master
```

## Option B — Manual duplicate on GitHub

1. Go to https://github.com/hustronix35-prog/marketing-os
2. Click **Settings** → scroll to **Danger Zone** → **Duplicate this repository**  
   *(Or: create empty repo `hustronix-content-ops` at https://github.com/new)*
3. Name: `hustronix-content-ops`
4. Local push:

```powershell
cd D:\content
git remote add content-ops https://github.com/hustronix35-prog/hustronix-content-ops.git
git push -u content-ops master
```

## After Push

1. Update **Cursor Automations** repo field → `hustronix35-prog/hustronix-content-ops`
2. Verify GitHub Actions badges on README
3. Apply labels from [docs/github-labels.md](github-labels.md)
4. Replace screenshot placeholders in `docs/assets/`

## Keep marketing-os?

The original `marketing-os` repo can remain as a private archive or be archived on GitHub. Content Ops is the portfolio-facing public repo going forward.
