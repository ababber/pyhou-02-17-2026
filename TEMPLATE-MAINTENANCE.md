# Template System Maintenance Guide

## Overview

The Cursor Starter Kit uses a **source-of-truth** model:
- **Source of Truth**: `cursor-starter-kit/` in the `quant` repository
- **Template Repository**: Separate GitHub repo for "Use this template"
- **Auto-Sync**: Git hook automatically syncs template on commits

## Quick Reference

```bash
# One-time setup: Install auto-sync hook
./cursor-starter-kit/install-hook.sh

# Then just commit changes - template auto-syncs!
git add cursor-starter-kit/
git commit -m "update: Add feature"
git push

# Manual sync (if needed)
./cursor-starter-kit/sync-template.sh --dry-run  # Preview
./cursor-starter-kit/sync-template.sh --yes      # Sync
```

## Repository Structure

### Source of Truth
**Location**: `/Users/ankit/Playground/_quantRepos/quant/cursor-starter-kit/`

Contains:
- All starter kit files (`.cursorrules`, scripts, tests, etc.)
- `install.sh` - Installation script
- `cursorkit.zsh` - Shell helper function
- `sync-template.sh` - Sync to template repo
- `install-hook.sh` - Install auto-sync hook
- `hooks/post-commit` - Auto-sync hook (tracked)
- `.syncignore` - Files to exclude from sync (gitignore syntax)

### Template Repository
**Location**: `https://github.com/ababber/cursor-starter-kit-template`

Contains all starter kit files, automatically synced from source of truth.

## Scripts

| Script | Purpose |
|--------|---------|
| `sync-template.sh` | Sync template repo (git clone/push) |
| `install-hook.sh` | Install/uninstall auto-sync hook |
| `install.sh` | Install starter kit into a repo |
| `cursorkit.zsh` | Shell helper for install.sh |
| `create-repo-with-kit.sh` | Create GitHub repo + install kit |

## Configuration

### `.syncignore`
Controls which files are excluded from syncing to the template. Uses gitignore-style patterns:

```gitignore
# Exclude user data
cursor-usage/usage.db
cursor-chats/*.md

# Keep .gitkeep files
!cursor-chats/.gitkeep
```

### `sync.log`
Sync operations are logged to `cursor-starter-kit/sync.log` for debugging.

## Auto-Sync Workflow

### Setup (one-time)
```bash
cd /path/to/quant
./cursor-starter-kit/install-hook.sh
```

### Daily Use
Just commit changes to `cursor-starter-kit/` — the hook automatically:
1. Detects changes to `cursor-starter-kit/`
2. Runs `sync-template.sh --yes`
3. Syncs, commits, and pushes to template repo
4. Reminds you if `cursorkit.zsh` was updated

### Disable/Re-enable
```bash
./cursor-starter-kit/install-hook.sh --uninstall  # Disable
./cursor-starter-kit/install-hook.sh              # Re-enable
```

## Manual Sync

```bash
cd /Users/ankit/Playground/_quantRepos/quant/cursor-starter-kit

# Preview changes
./sync-template.sh --dry-run

# Sync, commit, and push
./sync-template.sh --yes

# Sync without committing (to review first)
./sync-template.sh --yes --no-commit
```

## Initial Template Setup

If creating the template repo for the first time:

```bash
# 1. Create template repo
gh repo create cursor-starter-kit-template --public --clone
cd cursor-starter-kit-template

# 2. Run initial sync from source
cd /path/to/quant/cursor-starter-kit
./sync-template.sh --yes

# 3. Enable template mode on GitHub
# Go to repo Settings → Template repository → Enable
```

## Configuration

### Template Repo URL
Edit `sync-template.sh` line ~21:
```zsh
TEMPLATE_REPO_URL="https://github.com/ababber/cursor-starter-kit-template.git"
```

### cursorkit.zsh Location
The hook reminds you to update OMZ when `cursorkit.zsh` changes:
```bash
cp cursor-starter-kit/cursorkit.zsh ~/.oh-my-zsh/custom/cursorkit.zsh
```

## Checklist

When updating the starter kit:
- [ ] Make changes in `cursor-starter-kit/`
- [ ] Commit (auto-syncs to template)
- [ ] Push to `quant` repo
- [ ] Update `cursorkit.zsh` in OMZ if reminded

## Troubleshooting

### Hook not running
```bash
# Reinstall hook
./cursor-starter-kit/install-hook.sh --yes
```

### Sync fails
```bash
# Check template repo URL
grep TEMPLATE_REPO_URL cursor-starter-kit/sync-template.sh

# Test manually
./cursor-starter-kit/sync-template.sh --dry-run
```

### cursorkit not found
```bash
# Re-source it
source cursor-starter-kit/cursorkit.zsh
# Or copy to OMZ
cp cursor-starter-kit/cursorkit.zsh ~/.oh-my-zsh/custom/
```
