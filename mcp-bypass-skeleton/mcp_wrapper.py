#!/usr/bin/env python3
"""
MCP Wrapper Skeleton

Bypasses Cursor's MCP tool serialization by calling the MCP server directly via Docker.

Customize:
- DOCKER_IMAGE: Your MCP server Docker image
- ENV_VARS: Environment variables for credentials
- Docker run arguments as needed
"""

import json
import os
import subprocess
from pathlib import Path

# === CUSTOMIZE THESE ===
DOCKER_IMAGE = "your-mcp-server-image:tag"
CONTAINER_NAME = "mcp-server"

# Environment variables to pass to container
# These should be set in your .env or shell environment
ENV_VARS = [
    "YOUR_API_KEY",
    "YOUR_USER_ID",
]

# Load from .env if present
def load_dotenv():
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

load_dotenv()


def call_mcp_tool(tool_name: str, arguments: dict) -> dict:
    """Call an MCP tool via Docker subprocess."""
    
    # Build environment args
    env_args = []
    for var in ENV_VARS:
        value = os.environ.get(var)
        if value:
            env_args.extend(["-e", f"{var}={value}"])
    
    # MCP request format
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    # Build Docker command
    cmd = [
        "docker", "run", "--rm", "-i",
        "--name", f"{CONTAINER_NAME}-{os.getpid()}",
        *env_args,
        DOCKER_IMAGE
    ]
    
    try:
        result = subprocess.run(
            cmd,
            input=json.dumps(request),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            return {
                "success": False,
                "error": f"Docker error: {result.stderr}",
                "returncode": result.returncode
            }
        
        # Parse response
        response = json.loads(result.stdout)
        return {
            "success": True,
            "response": response
        }
        
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Timeout after 120s"}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON decode error: {e}", "raw": result.stdout}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python mcp_wrapper.py <tool_name> '<json_args>'")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    result = call_mcp_tool(tool_name, args)
    print(json.dumps(result, indent=2))
