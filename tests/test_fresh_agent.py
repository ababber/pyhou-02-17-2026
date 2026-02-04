#!/usr/bin/env python3
"""
Test script to validate a fresh Cursor CLI agent setup.

This simulates what a fresh agent instance should do when starting
a new conversation in a repo with the starter kit installed.

Run from a repo with the starter kit installed:
    python tests/test_fresh_agent.py
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def print_result(name: str, passed: bool, details: str = ""):
    """Print test result with color."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {name}")
    if details and not passed:
        print(f"       {details}")


def test_required_files():
    """Test that all required files exist."""
    print("\n📁 Required Files")
    print("-" * 40)
    
    required = [
        ".cursorrules",
        "COMMIT-CONVENTIONS.md",
        "cursor-scripts/cursor_usage.py",
        "cursor-scripts/export-chat.sh",
        "cursor-scripts/web_search.py",
        "cursor-chats/.gitkeep",
        "cursor-web-search/.gitkeep",
    ]
    
    all_passed = True
    for filepath in required:
        exists = Path(filepath).exists()
        print_result(filepath, exists)
        if not exists:
            all_passed = False
    
    return all_passed


def test_cursorrules_protocols():
    """Test that .cursorrules contains required protocol sections."""
    print("\n📜 Protocol Sections in .cursorrules")
    print("-" * 40)
    
    if not Path(".cursorrules").exists():
        print_result(".cursorrules exists", False)
        return False
    
    content = Path(".cursorrules").read_text()
    
    required_sections = [
        ("Session Continuity", "🔄 Session Continuity"),
        ("MANDATORY label", "⚠️ MANDATORY"),
        ("Self-check", "Self-check:"),
        ("Conversation Export", "📝 Conversation Export"),
        ("Workspace Boundaries", "🚫 Workspace Boundaries"),
        ("Git Commits", "Git Commits"),
        ("COMMIT-CONVENTIONS.md reference", "COMMIT-CONVENTIONS.md"),
    ]
    
    all_passed = True
    for name, marker in required_sections:
        found = marker in content
        print_result(name, found)
        if not found:
            all_passed = False
    
    return all_passed


def test_session_continuity_commands():
    """Test that session continuity commands work."""
    print("\n🔄 Session Continuity Commands")
    print("-" * 40)
    
    all_passed = True
    
    # Test git log
    try:
        result = subprocess.run(
            ["git", "--no-pager", "log", "--stat", "-5"],
            capture_output=True,
            text=True,
            timeout=10
        )
        passed = result.returncode == 0
        print_result("git log --stat -5", passed, result.stderr if not passed else "")
        if not passed:
            all_passed = False
    except Exception as e:
        print_result("git log --stat -5", False, str(e))
        all_passed = False
    
    # Test cursor_usage.py
    if Path("cursor-scripts/cursor_usage.py").exists():
        try:
            result = subprocess.run(
                ["python", "cursor-scripts/cursor_usage.py", "reminder", "--once"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # This may fail if no CSV imported, but should at least run
            passed = result.returncode in [0, 1]  # 1 = no data, but script works
            print_result("cursor_usage.py reminder --once", passed)
            if not passed:
                all_passed = False
        except Exception as e:
            print_result("cursor_usage.py reminder --once", False, str(e))
            all_passed = False
    else:
        print_result("cursor_usage.py exists", False)
        all_passed = False
    
    return all_passed


def test_export_chat():
    """Test that export-chat.sh is executable."""
    print("\n📝 Conversation Export")
    print("-" * 40)
    
    script_path = Path("cursor-scripts/export-chat.sh")
    
    if not script_path.exists():
        print_result("export-chat.sh exists", False)
        return False
    
    # Check if executable
    is_executable = os.access(script_path, os.X_OK)
    print_result("export-chat.sh is executable", is_executable)
    
    return is_executable


def test_commit_conventions():
    """Test that COMMIT-CONVENTIONS.md contains required sections."""
    print("\n📋 Commit Conventions")
    print("-" * 40)
    
    filepath = Path("COMMIT-CONVENTIONS.md")
    
    if not filepath.exists():
        print_result("COMMIT-CONVENTIONS.md exists", False)
        return False
    
    content = filepath.read_text()
    
    required_tags = ["add:", "update:", "fix:", "refactor:", "style:", "revert:"]
    
    all_passed = True
    for tag in required_tags:
        found = tag in content
        print_result(f"Tag '{tag}' documented", found)
        if not found:
            all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("=" * 50)
    print("🧪 Fresh Agent Setup Validation")
    print("=" * 50)
    
    results = []
    
    results.append(("Required Files", test_required_files()))
    results.append(("Protocol Sections", test_cursorrules_protocols()))
    results.append(("Session Continuity", test_session_continuity_commands()))
    results.append(("Conversation Export", test_export_chat()))
    results.append(("Commit Conventions", test_commit_conventions()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary")
    print("=" * 50)
    
    passed = sum(1 for _, p in results if p)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Agent setup is valid.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
