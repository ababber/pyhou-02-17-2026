# Cursor Starter Kit Test Suite

Tests for verifying the starter kit scripts work correctly after installation.

## Quick Start

```bash
# Run all tests
python tests/run_all.py

# Test fresh agent setup (validates protocols are in place)
python tests/test_fresh_agent.py

# Run specific test
python tests/test_cursor_usage.py
python tests/test_export_chat.py
python tests/test_web_search.py
python tests/test_review.py
python tests/test_startup_cards.py
```

## Test Coverage

| Script | Test File | Status |
|--------|-----------|--------|
| Fresh agent setup | `test_fresh_agent.py` | ✅ |
| `cursor_usage.py` | `test_cursor_usage.py` | ✅ |
| `export-chat.sh` | `test_export_chat.py` | ✅ |
| `web_search.py` | `test_web_search.py` | ⚠️ (requires API key) |
| `review.py` | `test_review.py` | ✅ (quiz, practice, flow) |
| `startup_cards.py` | `test_startup_cards.py` | ✅ (digest, quiz, reveal) |

## Requirements

- Python 3.8+
- Access to `~/.cursor/chats` (for export-chat tests)
- `GEMINI_API_KEY` in `.env` (for web search tests, optional)

## Running Tests

### All Tests
```bash
python tests/run_all.py
```

### Individual Tests
```bash
python tests/test_cursor_usage.py
python tests/test_export_chat.py
python tests/test_web_search.py --skip-api  # Skip API-required tests
```

### With Coverage
```bash
pip install pytest pytest-cov
pytest tests/ --cov=cursor-scripts --cov-report=html
```

## Test Structure

```
tests/
├── README.md              # This file
├── run_all.py             # Test runner
├── test_fresh_agent.py    # Fresh agent setup validation
├── test_cursor_usage.py   # Usage tracking tests
├── test_export_chat.py    # Chat export tests
├── test_web_search.py     # Web search tests
├── test_review.py        # Flashcard/quiz-through-AI tests
├── test_startup_cards.py # Daily digest and reveal-as-review tests
└── fixtures/             # Test data
    └── sample_usage.csv   # Sample CSV for import tests
```

## Notes

- **API Tests**: Web search tests require `GEMINI_API_KEY`. Use `--skip-api` to skip.
- **Export Tests**: Require access to `~/.cursor/chats`. Will skip if not available.
