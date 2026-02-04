# Cursor Custom Tools

Quick reference for the custom tools/scripts in this template.

## cursor-scripts/

- `cursor-scripts/cursor_usage.py`
  - Track Cursor usage from CSV exports (import/report/quota/budget/alerts/reminder/export).
  - **Kind-based billing:** Only **On-Demand** usage counts toward quota; **Included** usage does not. Quota/budget/alerts use On-Demand only.
  - Examples: `python cursor-scripts/cursor_usage.py report`, `python cursor-scripts/cursor_usage.py quota`.
  - Web vs CSV: `python cursor-scripts/cursor_usage.py quota --on-demand-reported 17` (17 = from Cursor console; console is authoritative).
  - Default billing day: 14 (configurable with `--billing-day`).
  - External requirements: none (uses local CSVs in `cursor-usage/`).

- `cursor-scripts/export-chat.sh`
  - Export latest Cursor chat from `~/.cursor/chats` SQLite to `cursor-chats/`.
  - Splits output at 5MB and names by environment/date.
  - Example: `./cursor-scripts/export-chat.sh`.
  - External requirements: access to `~/.cursor/chats`.

- `cursor-scripts/cursor-new-chat.sh`
  - Export current chat and clear history for a fresh start.
  - Example: `./cursor-scripts/cursor-new-chat.sh`.

- `cursor-scripts/web_search.py`
  - Gemini grounded web search with logging to `cursor-web-search/` (5MB split).
  - Requires `GEMINI_API_KEY` in env or `.env`.
  - Example: `python cursor-scripts/web_search.py "query"`.
  - External requirements: Google Gemini API key (`GEMINI_API_KEY`), internet access.

- `cursor-scripts/review.py`
  - Flashcard system with spaced repetition (add, quiz, stats, export).
  - Data: `cursor-data/flashcards.json`.
  - Example: `python cursor-scripts/review.py --quiz`.

- `cursor-scripts/startup_cards.py`
  - Daily digest and quiz at conversation start.
  - Example: `python cursor-scripts/startup_cards.py`.

- `cursor-scripts/get_model_benchmarks.py`
  - Fetch latest AI model benchmarks for task-based recommendations.
  - Example: `python cursor-scripts/get_model_benchmarks.py coding`.
  - External requirements: `GEMINI_API_KEY` for optional grounding.

## Agent Tooling Inventory

### Custom tools in this template

- `cursor-scripts/cursor_usage.py`
- `cursor-scripts/export-chat.sh`
- `cursor-scripts/cursor-new-chat.sh`
- `cursor-scripts/web_search.py`
- `cursor-scripts/review.py`
- `cursor-scripts/startup_cards.py`
- `cursor-scripts/get_model_benchmarks.py`

### Built-in tools available to the agent

- `Shell`
- `ReadFile`
- `ApplyPatch`
- `Grep`
- `Glob`
- `LS`
- `Delete`
- `EditNotebook`
- `WebFetch`
- `TodoWrite`
- `ListMcpResources`
- `FetchMcpResource`
