# Cursor Starter Kit

A portable template for setting up Cursor CLI workflows in new repositories.

**Philosophy:** AI answers should be verified. This template includes `.cursorrules`, `web_search.py`, and logging (web searches, chats) to expand reference and improve verification — don't rely solely on model training data.

**NOTE:** use the [gemini conversation](https://gemini.google.com/share/1fe756873a38) as an entry point into this repo. I used Gemini in Pro mode to analyze the repo; if you are having trouble seeing what the purpose of this repo is... read the conversation. It'll help you decide whether this tool fits your usecase.

## Quick Start

### Option 1: GitHub Template Repository (Easiest)

Create a template repository with the starter kit, then use GitHub's "Use this template" button for new repos.

See `TEMPLATE-SETUP.md` for detailed instructions.

### Option 2: Automated CLI Script

Automatically create a new GitHub repo with the starter kit:

```bash
./create-repo-with-kit.sh my-project --private --clone
```

This script:
- Creates the GitHub repository
- Clones it locally
- Installs the starter kit
- Commits and pushes everything

See `TEMPLATE-SETUP.md` for full documentation.

### Option 3: Manual Installation (Use the Installer Script)

```bash
# From the starter kit directory
./install.sh /path/to/your/repo

# Or install to current directory
cd /path/to/your/repo
/path/to/cursor-starter-kit/install.sh
```

The installer will:
- Copy all starter kit files
- Handle existing files (skip, backup, or overwrite)
- Make scripts executable
- Create `.env` from `.env.example`
- Provide next steps

## Contents

### Directory Structure

```
cursor-starter-kit/
├── install.sh              # Installation script
├── .cursorrules            # AI behavior rules
├── CURSOR-TOOLS.md         # Quick reference for custom tools (usage, web search, etc.)
├── .cursorignore           # Files to exclude from Cursor indexing
├── .gitignore              # Git ignore patterns
├── .env.example            # Environment variable template
├── cursor-scripts/         # Cursor workflow tools
│   ├── cursor_usage.py     # Usage tracking & quota management
│   ├── export-chat.sh      # Chat export to markdown
│   ├── cursor-new-chat.sh  # Export + clear for fresh start
│   ├── web_search.py       # Gemini web search with logging
│   ├── review.py           # Flashcard system (spaced repetition)
│   ├── startup_cards.py    # Daily digest + quiz at startup
│   └── get_model_benchmarks.py  # AI model selection helper
├── tests/                  # Test suite
│   ├── README.md           # Test documentation
│   ├── run_all.py          # Test runner
│   └── test_*.py           # Individual test files
├── cursor-chats/           # Exported conversations
├── cursor-usage/           # Usage CSV imports
├── cursor-web-search/      # Web search logs
└── cursor-data/            # Flashcard and learning data
```

### Tools

| Tool | Purpose | Requirements |
|------|---------|--------------|
| `cursor_usage.py` | Track usage to help manage API costs (quota, budget, alerts; On-Demand vs Included) | None (uses local CSVs) |
| `export-chat.sh` | Export chat from Cursor SQLite | Access to `~/.cursor/chats` |
| `cursor-new-chat.sh` | Manage context window exhaustion (export + clear); chats saved for reference | Access to `~/.cursor/chats` |
| `web_search.py` | Web search with logging | `GEMINI_API_KEY` |
| `review.py` | Flashcard system with spaced repetition | None |
| `startup_cards.py` | Daily digest + quiz at conversation start | None |
| `get_model_benchmarks.py` | Fetch latest AI model benchmarks | `GEMINI_API_KEY` |

### Key Features

- **Session continuity**: Auto-summarizes recent work at conversation start
- **Usage tracking**: Import Cursor usage CSVs; track quota/budget/alerts (On-Demand counts toward quota; Included does not). Use `quota --on-demand-reported N` for web vs CSV (N from Cursor console; authoritative).
- **Chat export**: One command (`/e`) to export conversation to markdown
- **New chat**: Export current chat and clear history for a fresh start. Also helps manage Cursor's context-window usage (the footer %); when that gets high, starting a new chat keeps the model responsive (context exhaustion management). Run `./cursor-scripts/cursor-new-chat.sh`. In case anything earlier needs to be referenced, the chats are there (exported to `cursor-chats/`). Trigger: say "new chat" in conversation.
- **Web search**: Gemini-powered search with automatic logging
- **Daily reminders**: Prompts to export yesterday's usage data
- **Flashcards**: Spaced repetition system for learning
- **Startup quiz**: Random review card at each session start; `--reveal` records as review (SM-2)
- **Model selection**: Fetch latest benchmarks for AI model recommendations
- **Research protocol**: Multi-source grounding (codebase → docs → web → browser; browser fallback is IDE-only, not available in Cursor CLI)

## Context Window Management

Cursor's context window has limits. As it fills (watch the % in the footer), responses get slower and less accurate.

**Solution:** Run `./cursor-scripts/cursor-new-chat.sh` to:

1. Export the current chat to `cursor-chats/` (nothing lost)
2. Clear history
3. Restart with a fresh context

**Trigger:** Say "new chat" (or "start fresh", "clear chat") in conversation.

## Customization

After copying to your repo:

1. **Edit `.cursorrules`** to add project-specific protocols at the bottom
2. **Update `.cursorignore`** for your file patterns
3. **Add API keys to `.env`** (copy from `.env.example`)
4. **Customize categories** in `review.py` for your domain

### Adding Project-Specific Rules

The `.cursorrules` file has a "Project-Specific Rules" section at the bottom. Add your custom rules there:

```markdown
## 🔧 Project-Specific Rules

### My API Wrapper
- Always use `my_wrapper.py` instead of direct API calls
- Check `./results/` for cached responses before making new requests

### Testing Protocol
- Run `pytest tests/` before any commit
- Use `--dry-run` flag first for destructive operations
```

**Examples of project-specific additions:**
- MCP server wrappers (like QuantConnect)
- Custom environment detection (Docker, virtual envs)
- Domain-specific search protocols
- API authentication flows
- CI/CD integration rules

### Flashcard Categories

Default categories in `review.py`: `dev`, `concept`, `tool`, `workflow`, `debug`, `general`

To customize, edit the `CATEGORIES` list at the top of the file.

## Testing

After installation, verify everything works:

```bash
# Run all tests
python tests/run_all.py

# Run specific test
python tests/test_cursor_usage.py
```

See `tests/README.md` for full test documentation.

## Learning Tools Usage

### Flashcards

```bash
# Add a card
python cursor-scripts/review.py --add "What is X?" "X is..."

# Review due cards
python cursor-scripts/review.py --quiz              # Interactive (terminal)
python cursor-scripts/review.py --quiz --start     # Quiz-through-AI (one Q at a time)
python cursor-scripts/review.py --quiz --start --practice  # Practice: random cards

# Check stats
python cursor-scripts/review.py --stats

# Export to markdown
python cursor-scripts/review.py --export > flashcards.md
```

### Startup Cards

Automatically shown at conversation start (configured in `.cursorrules`):

```bash
# Manual trigger
python cursor-scripts/startup_cards.py

# Just digest
python cursor-scripts/startup_cards.py --digest

# Reveal quiz answer (records as review for real flashcards)
python cursor-scripts/startup_cards.py --reveal
```

### Model Benchmarks

```bash
# General benchmarks
python cursor-scripts/get_model_benchmarks.py

# Task-specific
python cursor-scripts/get_model_benchmarks.py coding
python cursor-scripts/get_model_benchmarks.py reasoning
python cursor-scripts/get_model_benchmarks.py writing
python cursor-scripts/get_model_benchmarks.py fast
```

## MCP Bypass Pattern

If you need to work around Cursor's MCP tool serialization issues, see `MCP-WRAPPER-PATTERN.md` for a complete guide with code examples.

## Template Repository Maintenance

If you're maintaining a GitHub template repository, see **[TEMPLATE-MAINTENANCE.md](TEMPLATE-MAINTENANCE.md)** for complete documentation.

**Automatic sync (recommended):**

```bash
# One-time setup: Install git hook
./install-hook.sh

# Then just commit normally - template auto-syncs!
git commit -m "update: Add feature"
```

**Manual sync:**

```bash
cd cursor-starter-kit
./sync-template.sh --dry-run  # Preview
./sync-template.sh --yes      # Sync, commit, and push
```

**Note:** Maintenance scripts (`sync-template.sh`, `install-hook.sh`, etc.) are not part of the starter kit - they're tools for managing the template repository.

**Gemini analysis:** if you would like to see what Gemini thinks of this repo, check out this conversation it's wild [Gemini Analysis of cursor-starter-kit-template](https://gemini.google.com/share/1fe756873a38)
