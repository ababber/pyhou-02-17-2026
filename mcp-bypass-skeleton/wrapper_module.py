#!/usr/bin/env python3
"""
MCP Wrapper Module

Python module for programmatic access to MCP tools.

Usage:
    from wrapper_module import call_tool, list_tools
    
    result = call_tool("tool_name", {"arg": "value"})
"""

from mcp_wrapper import call_mcp_tool


def call_tool(tool_name: str, arguments: dict = None) -> dict:
    """
    Call an MCP tool and return the result.
    
    Args:
        tool_name: Name of the MCP tool
        arguments: Dictionary of arguments (optional)
    
    Returns:
        dict with 'success' boolean and 'response' or 'error'
    """
    return call_mcp_tool(tool_name, arguments or {})


def list_tools() -> dict:
    """List available MCP tools."""
    # This calls the MCP 'tools/list' method
    # You may need to customize this for your MCP server
    return call_mcp_tool("list_tools", {})


# Add convenience functions for your specific tools
# Example:
# def read_account():
#     return call_tool("read_account", {})
