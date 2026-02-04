# MCP Bypass Skeleton

This is a template for working around Cursor's MCP tool serialization issues.

## The Problem

Cursor's internal MCP tool handling can have serialization bugs that affect certain tools. When this happens, direct `mcp_*` tool calls fail silently or return malformed data.

## The Solution

Bypass Cursor's MCP integration by calling the MCP server directly via Docker subprocess.

## Files

- `mcp_wrapper.py` - Core wrapper that calls MCP server via Docker
- `wrapper_runner.py` - CLI interface + result file management
- `wrapper_module.py` - Python module for programmatic access

## Usage

1. Copy this skeleton to your project (e.g., `my-mcp-env/`)
2. Edit `mcp_wrapper.py`:
   - Update `DOCKER_IMAGE` to your MCP server image
   - Update `ENV_VARS` for your credentials
   - Adjust Docker run arguments as needed
3. Edit `wrapper_runner.py`:
   - Update `RESULTS_DIR` path
4. Add shell alias to `~/.zshrc`:
   ```bash
   alias my-mcp-run='python /path/to/wrapper_runner.py'
   ```
5. Reload shell: `source ~/.zshrc`

## Workflow

```bash
# Run a tool
my-mcp-run req_001 tool_name '{"arg": "value"}'

# Read result
cat my-mcp-env/results/req_001.json
```

## Integration with .cursorrules

Add to your `.cursorrules`:

```markdown
### MCP Wrapper

**NEVER use `mcp_*` tools directly.** Use the wrapper instead.

**Command:** `my-mcp-run <request_id> <tool_name> '<json_args>'`

**Workflow:**
1. Check `my-mcp-env/results/` for existing results
2. Run wrapper command
3. Read result from `my-mcp-env/results/<request_id>.json`
```
