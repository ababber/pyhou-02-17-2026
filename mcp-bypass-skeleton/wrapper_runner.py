#!/usr/bin/env python3
"""
MCP Wrapper Runner

CLI interface for the MCP wrapper with result file management.

Usage:
    python wrapper_runner.py <request_id> <tool_name> '<json_args>'
    python wrapper_runner.py cleanup  # Remove old result files
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# === CUSTOMIZE THIS ===
RESULTS_DIR = Path(__file__).parent / "results"

# Import the wrapper
from mcp_wrapper import call_mcp_tool


def ensure_results_dir():
    RESULTS_DIR.mkdir(exist_ok=True)


def save_result(request_id: str, result: dict):
    ensure_results_dir()
    result_file = RESULTS_DIR / f"{request_id}.json"
    result["timestamp"] = datetime.now().isoformat()
    result_file.write_text(json.dumps(result, indent=2))
    return result_file


def cleanup_old_results(days: int = 7):
    """Remove result files older than N days."""
    if not RESULTS_DIR.exists():
        return 0
    
    cutoff = datetime.now() - timedelta(days=days)
    removed = 0
    
    for f in RESULTS_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            ts = datetime.fromisoformat(data.get("timestamp", ""))
            if ts < cutoff:
                f.unlink()
                removed += 1
        except (json.JSONDecodeError, ValueError):
            pass
    
    return removed


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python wrapper_runner.py <request_id> <tool_name> '<json_args>'")
        print("  python wrapper_runner.py cleanup")
        sys.exit(1)
    
    if sys.argv[1] == "cleanup":
        removed = cleanup_old_results()
        print(f"Removed {removed} old result files")
        return
    
    if len(sys.argv) < 3:
        print("Error: Need request_id and tool_name")
        sys.exit(1)
    
    request_id = sys.argv[1]
    tool_name = sys.argv[2]
    arguments = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    
    # Call the tool
    result = call_mcp_tool(tool_name, arguments)
    
    # Save result
    result_file = save_result(request_id, {
        "request_id": request_id,
        "tool": tool_name,
        "arguments": arguments,
        "result": result
    })
    
    # Output
    if result.get("success"):
        print(f"✓ Result saved to {result_file}")
    else:
        print(f"✗ Error: {result.get('error')}")
        print(f"  Result saved to {result_file}")
        sys.exit(1)


if __name__ == "__main__":
    main()
