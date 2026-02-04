# Git Commit Conventions

## Commit Message Format

```
<tag>: <description>

<optional body with details>
```

## Commit Tags

### Primary Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `add:` | New features, files, or functionality | `add: user authentication system` |
| `update:` | Changes to existing files or features | `update: improve error handling` |
| `refactor:` | Code restructuring without changing functionality | `refactor: extract helper functions` |
| `fix:` | Bug fixes | `fix: resolve null pointer exception` |
| `style:` | Formatting, linting, whitespace changes | `style: format Python files with black` |

### Special Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `revert:` | Reverting previous commits | `revert: undo breaking change` |
| `init:` | Initial setup or project initialization | `init: setup project structure` |
| `docs:` | Documentation only changes | `docs: update README` |
| `test:` | Adding or updating tests | `test: add unit tests for auth` |
| `lint` | Linting changes (no colon) | `lint` |

## Guidelines

### When to Use Each Tag

- **`add:`** - New files, features, protocols, documentation
- **`update:`** - Modifying existing content, refining functionality
- **`refactor:`** - Renaming files, restructuring code, improving organization
- **`fix:`** - Correcting bugs, errors, or broken functionality
- **`style:`** - Code formatting, linting with tools (black, prettier, etc.)
- **`docs:`** - README updates, comments, documentation files
- **`test:`** - Test files, test coverage improvements
- **`lint`** - Quick linting fixes (standalone, no description needed)
- **`revert:`** - Undoing changes
- **`init:`** - Project setup, initial configuration

### Message Body

For complex changes, include a body with bullet points:

```
add: comprehensive test suite with 100% pass rate

- Created test_all.py testing all modules
- 23/23 tested functions pass
- Updated documentation with test results
```

### Date Format in Filenames

**Always use `YYYY-DD-MM` format** (e.g., `2026-25-01` for January 25, 2026)

## Examples

### Good Commit Messages

```bash
add: user authentication system
update: improve error handling in API calls
refactor: extract validation logic to helpers
fix: resolve race condition in async handler
style: format Python files with black
docs: update installation instructions
test: add integration tests for auth flow
revert: undo breaking API change
lint
```

### Bad Commit Messages

```bash
# Too vague
update: stuff
fix: it
changes

# Missing tag
Added new feature
Fixed bug

# Wrong date format in filename references
update: append to log_2026-01-25.md  # Should be 2026-25-01
```

## References

- Chat history: `cursor-chats/CURSOR-CLI_YYYY-DD-MM_NN.md`
- Web search logs: `cursor-web-search/CURSOR-WEB_YYYY-DD-MM.md`
