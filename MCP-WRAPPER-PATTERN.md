# MCP Wrapper Pattern

**When to use:** If an MCP server's tools fail through Cursor's client (serialization bugs, permission issues, etc.), create a wrapper to bypass the problematic layer.

## The Problem

MCP servers expose tools that Cursor's AI should be able to call directly. Sometimes this fails due to:
- **Serialization bugs** - Cursor's MCP client mangles complex JSON
- **Permission issues** - Docker/filesystem access from Cursor's subprocess
- **Transport issues** - SSE/stdio connection problems
- **Credential handling** - Environment variables not passed correctly

## The Solution Pattern

Create a Python wrapper that:
1. Connects directly to the MCP server (bypassing Cursor's client)
2. Accepts tool calls via CLI arguments
3. Returns results to JSON files
4. Provides shell aliases for easy invocation

## Implementation Steps

### Step 1: Identify the Bug

Test the MCP tool through Cursor's client:

```python
# In Cursor, this fails:
mcp_ServerName_tool_name({"arg": "value"})
```

If it fails, note:
- Error message
- Expected input/output format
- Which tools are affected

### Step 2: Create Wrapper Script

**File: `mcp-wrapper/wrapper.py`**

```python
#!/usr/bin/env python3
import json
import sys
import subprocess
import os
from datetime import datetime

# MCP server connection details
MCP_SERVER_CMD = ["docker", "exec", "mcp-container", "command"]  # Or stdio command
RESULTS_DIR = "mcp-wrapper/results"

def call_mcp_tool(tool_name, args_json):
    """Call MCP server directly via stdio/docker."""
    # Build MCP protocol request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": json.loads(args_json) if isinstance(args_json, str) else args_json
        }
    }
    
    # Send to MCP server
    proc = subprocess.run(
        MCP_SERVER_CMD,
        input=json.dumps(request),
        capture_output=True,
        text=True
    )
    
    # Parse response
    if proc.returncode != 0:
        return {"success": False, "error": proc.stderr}
    
    try:
        response = json.loads(proc.stdout)
        return {"success": True, "response": response.get("result", {})}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON: {e}"}

def save_result(request_id, result):
    """Save result to file for AI to read."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    output = {
        "request_id": request_id,
        "timestamp": datetime.now().isoformat(),
        "result": result
    }
    
    filepath = os.path.join(RESULTS_DIR, f"{request_id}.json")
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"RESULT_FILE:{os.path.abspath(filepath)}")
    print("SUCCESS" if result.get("success") else "ERROR")
    return filepath

def main():
    if len(sys.argv) < 3:
        print("Usage: python wrapper.py <request_id> <tool_name> '<json_args>'")
        sys.exit(1)
    
    request_id = sys.argv[1]
    tool_name = sys.argv[2]
    args_json = sys.argv[3] if len(sys.argv) > 3 else "{}"
    
    # Call MCP tool
    result = call_mcp_tool(tool_name, args_json)
    
    # Save result
    save_result(request_id, result)
    
    # Print result for immediate use
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
```

### Step 3: Create Shell Aliases

**Add to `~/.zshrc` or create Oh My Zsh plugin:**

```bash
# MCP Wrapper Functions
export MCP_WRAPPER_ROOT="/path/to/your/project"

# Quick command runner
mcp-run() {
    local request_id="req_$(date +%s)"
    local tool_name="$1"
    shift
    local args="$*"
    
    cd "$MCP_WRAPPER_ROOT" && \
    python3 mcp-wrapper/wrapper.py "$request_id" "$tool_name" "$args"
}

# Auto-generated request ID
mcp-ai-run() {
    local request_id="$1"
    local tool_name="$2"
    shift 2
    local args="$*"
    
    cd "$MCP_WRAPPER_ROOT" && \
    python3 mcp-wrapper/wrapper.py "$request_id" "$tool_name" "$args"
}
```

### Step 4: Update .cursorrules

Instruct the AI to use the wrapper:

```markdown
### 🔧 MCP Server Wrapper

**Problem:** MCP tools fail through Cursor's client (serialization bug).

**Solution:** Use wrapper via Shell tool.

**Command pattern:**
```bash
mcp-ai-run <request_id> <tool_name> '<json_args>'
```

**Workflow:**
1. Generate unique request_id (e.g., `req_001`)
2. Run wrapper command via Shell
3. Read result from `mcp-wrapper/results/<request_id>.json`

**Example:**
```bash
# Get data
mcp-ai-run req_001 get_user_info '{}'

# Parse result
import json
result = json.loads(read_file('mcp-wrapper/results/req_001.json'))
data = result["result"]["response"]
```

**Status:**
✅ Wrapper bypasses Cursor's bug
✅ All tools accessible
⚠️ Must use wrapper (don't call `mcp_ServerName_*` directly)
```

### Step 5: Test the Wrapper

```bash
# Test basic call
python3 mcp-wrapper/wrapper.py test_001 tool_name '{}'

# Check result file
cat mcp-wrapper/results/test_001.json

# Test via alias
mcp-run tool_name '{}'
```

## AI Usage Pattern

When AI needs MCP data:

1. **Generate request ID:**
   ```python
   request_id = f"req_{uuid.uuid4().hex[:8]}"
   ```

2. **Call wrapper:**
   ```bash
   mcp-ai-run req_abc123 tool_name '{"arg": "value"}'
   ```

3. **Read result:**
   ```python
   result = json.loads(read_file(f'mcp-wrapper/results/req_abc123.json'))
   if result["result"]["success"]:
       data = result["result"]["response"]
   ```

## Environment Detection

Add to session continuity checks:

```bash
# Check if wrapper is available
if command -v mcp-run &> /dev/null; then
    echo "✅ MCP Wrapper: Available"
else
    echo "⚠️ MCP Wrapper: Not installed (reload shell)"
fi
```

## File Structure

```
project/
├── mcp-wrapper/
│   ├── wrapper.py           # Core wrapper script
│   ├── results/             # Result files (JSON)
│   │   ├── req_001.json
│   │   └── req_002.json
│   └── README.md            # Usage docs
├── .cursorrules             # Instructions for AI
└── ~/.zshrc                 # Shell aliases
```

## Advantages

✅ **Bypasses client bugs** - Direct MCP server access  
✅ **Traceable** - Every call has unique ID  
✅ **Debuggable** - Results saved to files  
✅ **Parallel calls** - AI can batch requests  
✅ **Environment isolation** - Uses your shell's env vars  

## Real Example: QuantConnect MCP

The QuantConnect MCP server had a serialization bug where 59/64 tools failed through Cursor's client. This section shows the complete implementation that achieved 100% tool success.

### Problem

```python
# This failed with serialization errors:
mcp_QuantConnect_read_file({"model": {"projectId": 123, "name": "main.py"}})
# Error: Invalid params, unexpected property "model"
```

Cursor's MCP client was mangling nested JSON parameters before sending to the server.

### Solution Architecture

```
┌─────────────┐    Shell cmd    ┌──────────────┐    stdio    ┌─────────────┐
│   Cursor    │ ──────────────► │   Wrapper    │ ──────────► │   Docker    │
│   AI Agent  │                 │   Scripts    │             │  MCP Server │
└─────────────┘                 └──────────────┘             └─────────────┘
       │                               │
       │ Read file                     │ Save result
       ▼                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     cursor-qc-env/results/*.json                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### Core Wrapper: `qc_mcp_wrapper.py`

The main wrapper handles MCP protocol communication directly via Docker stdio:

```python
#!/usr/bin/env python3
"""Bypasses Cursor's broken serialization by connecting directly to MCP server."""

import json
import subprocess
import os
import sys
from typing import Any, Dict

class QCMCPWrapper:
    """Wrapper for QuantConnect MCP server that bypasses Cursor serialization"""

    def __init__(self):
        self.process = None
        self.initialized = False
        self.request_id = 0

    def _ensure_initialized(self):
        """Initialize MCP connection if not already done"""
        if self.initialized:
            return

        # Start Docker container with MCP server
        cmd = [
            "docker", "run", "-i", "--rm",
            "--platform", "linux/arm64",
            "-e", f"QUANTCONNECT_USER_ID={os.environ.get('QUANTCONNECT_USER_ID', '')}",
            "-e", f"QUANTCONNECT_API_TOKEN={os.environ.get('QUANTCONNECT_API_TOKEN', '')}",
            "quantconnect/mcp-server:latest",
        ]

        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        # Send MCP initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "qc-wrapper", "version": "1.0.0"},
            },
        }

        self.process.stdin.write(json.dumps(init_request) + "\n")
        self.process.stdin.flush()

        # Wait for response
        response_line = self.process.stdout.readline()
        response = json.loads(response_line)

        if "result" in response:
            # Send initialized notification (required by MCP protocol)
            self.process.stdin.write(json.dumps({
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {},
            }) + "\n")
            self.process.stdin.flush()
            self.initialized = True
        else:
            raise Exception(f"Initialization failed: {response.get('error')}")

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool with proper parameter handling"""
        self._ensure_initialized()
        self.request_id += 1

        # Build MCP tools/call request
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        }

        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()

        response_line = self.process.stdout.readline()
        response = json.loads(response_line)

        if "error" in response:
            raise Exception(f"MCP error: {response['error']}")

        return response.get("result", {})

    def close(self):
        """Close MCP connection"""
        if self.process:
            self.process.stdin.close()
            self.process.wait()
            self.initialized = False
```

**Key design decisions:**
- **Persistent connection** - Reuses Docker container across multiple calls
- **Proper MCP handshake** - Sends `initialize` then `notifications/initialized`
- **Clean JSON handling** - No serialization layer between Python and MCP

### Runner Script: `qc_wrapper_runner.py`

Executes wrapper commands and saves results to files for AI to read:

```python
#!/usr/bin/env python3
"""Runs wrapper commands and saves results to files for AI to read."""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

WRAPPER_PATH = Path(__file__).parent / "qc_mcp_wrapper.py"
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def run_wrapper_command(tool_name: str, arguments: dict = None) -> dict:
    """Run wrapper command and return result"""
    args_json = json.dumps(arguments or {})
    cmd = [sys.executable, str(WRAPPER_PATH), tool_name, args_json]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout)
        return {"success": True, "response": response}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr}

def is_result_useful(result: dict) -> bool:
    """Check if result has data (filters empty search results)"""
    if not result.get("success", False):
        return False
    
    # Filter empty search results
    response = result.get("response", {})
    structured = response.get("structuredContent", {})
    if "retrivals" in structured:
        if len(structured.get("retrivals", [])) == 0:
            return False
    return True

def save_result(request_id: str, result: dict):
    """Save result to file (only if useful)"""
    if not is_result_useful(result):
        return None  # Don't save empty/error results
    
    result_file = RESULTS_DIR / f"{request_id}.json"
    result_data = {
        "request_id": request_id,
        "timestamp": datetime.now().isoformat(),
        "result": result,
    }
    with open(result_file, "w") as f:
        json.dump(result_data, f, indent=2)
    return result_file

def main():
    request_id = sys.argv[1]
    tool_name = sys.argv[2]
    arguments = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}

    result = run_wrapper_command(tool_name, arguments)
    result_file = save_result(request_id, result)

    if result_file:
        print(f"RESULT_FILE:{result_file}")
        print("SUCCESS")
    else:
        print("RESULT_DELETED:Empty or error result, file not saved")

if __name__ == "__main__":
    main()
```

**Key features:**
- **Auto-cleanup** - Doesn't save empty search results or errors
- **Unique IDs** - Each request has traceable ID
- **JSON output** - AI can parse results easily

### Shell Function: Oh My Zsh Plugin

**File: `~/.oh-my-zsh/custom/plugins/qc-wrapper/qc-wrapper.plugin.zsh`**

```bash
# Environment variable pointing to project root
export QC_WRAPPER_ROOT="/Users/yourname/path/to/project"

# Main function for AI to call
qc-ai-run() {
    local request_id="$1"
    local tool="$2"
    shift 2
    local args="$*"
    
    cd "$QC_WRAPPER_ROOT" && \
    python3 cursor-qc-env/qc_wrapper_runner.py "$request_id" "$tool" "$args"
}

# Quick test function
qc-test() {
    qc-ai-run test_$(date +%s) read_account '{}'
}
```

**Enable in `~/.zshrc`:**
```bash
plugins=(... qc-wrapper)
```

### `.cursorrules` Integration

```markdown
### 🔧 QuantConnect MCP Wrapper

**🔴 NEVER use `mcp_QuantConnect_*` tools directly.** Serialization bug affects 59/64 tools.

**ALWAYS use:** `qc-ai-run <request_id> <tool_name> '<json_args>'`

**Workflow:**
1. Check `cursor-qc-env/results/` for existing results
2. Run `qc-ai-run` via Shell tool
3. Read `cursor-qc-env/results/<request_id>.json`

**Example commands:**
```bash
# Read account
qc-ai-run req_001 read_account '{}'

# Read file from project
qc-ai-run req_002 read_file '{"model":{"projectId":27636702,"name":"main.py"}}'

# Search examples
qc-ai-run req_003 search_quantconnect '{"model":{"language":"Py","criteria":[{"input":"RSI","type":"Examples","count":5}]}}'

# Check syntax
qc-ai-run req_004 check_syntax '{"model":{"language":"Py","files":[{"name":"test.py","content":"def hello():\n    print(1)\n"}]}}'
```

**Response parsing:**
```python
import json
result = json.loads(read_file('cursor-qc-env/results/req_001.json'))
if result.get("result", {}).get("success"):
    data = result["result"]["response"].get("structuredContent", {})
    # If empty, check content[0].text
    if not data and "content" in result["result"]["response"]:
        text = result["result"]["response"]["content"][0].get("text", "")
        data = json.loads(text) if text else {}
```

**Tool name format:**
- ✅ `read_account`, `search_quantconnect` (no prefix)
- ❌ `mcp_QuantConnect_read_account` (broken)
```

### Result File Format

**File: `cursor-qc-env/results/req_001.json`**

```json
{
  "request_id": "req_001",
  "timestamp": "2026-01-27T06:30:00.000000",
  "result": {
    "success": true,
    "response": {
      "structuredContent": {
        "organizationId": "abc123",
        "balance": 100000,
        "seats": 1
      }
    }
  }
}
```

### Results

| Metric | Before | After |
|--------|--------|-------|
| Tools working | 5/64 | 64/64 |
| Success rate | 8% | 100% |
| Serialization errors | 59 | 0 |

**Files created:**
- `cursor-qc-env/qc_mcp_wrapper.py` - Core MCP client (1000 lines)
- `cursor-qc-env/qc_wrapper_runner.py` - Result file manager (250 lines)
- `~/.oh-my-zsh/custom/plugins/qc-wrapper/` - Shell integration
- `cursor-qc-env/results/` - Cached results directory

## Customization

Adapt this pattern to your MCP server:

1. **Connection method:**
   - Docker exec: `docker exec container command`
   - Stdio: `npx mcp-server-name`
   - HTTP: `requests.post(mcp_url, json=request)`

2. **Authentication:**
   - Environment vars: `os.environ.get("API_KEY")`
   - Config file: `json.load(open(".env.json"))`
   - Credential store: `keyring.get_password("service", "user")`

3. **Result format:**
   - Simple JSON: `{"success": true, "data": {...}}`
   - Full MCP response: Include entire `result` object
   - Streaming: Write chunks to file as they arrive

## When NOT to Use

Don't create a wrapper if:
- MCP tools work fine through Cursor's client
- Issue is with MCP server itself (not client)
- Problem can be fixed with better error handling

Try fixing the underlying issue first. Wrappers add complexity.

## Troubleshooting

**"Command not found"**
- Reload shell: `source ~/.zshrc`
- Check alias: `type mcp-run`

**"Docker permission denied"**
- Run in CLI mode (Docker running)
- Or provide commands for user to run manually

**"Result file empty"**
- Check MCP server logs
- Verify JSON arguments are valid
- Test MCP tool outside wrapper

## Further Reading

- MCP Protocol Spec: https://modelcontextprotocol.io/docs/
- Cursor MCP Integration: https://docs.cursor.com/context/model-context-protocol
- Example Implementation: See `cursor-qc-env/` in this repo
