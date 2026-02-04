#!/usr/bin/env python3
"""
Tests for web_search.py

Tests:
- Script exists
- API key detection
- Search functionality (if API key available)
"""

import sys
import os
import subprocess
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "cursor-scripts" / "web_search.py"

# Load .env if present (optional dependency)
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass  # dotenv not required


def test_script_exists():
    """Test that script exists."""
    print("Testing script exists...")
    
    if not SCRIPT_PATH.exists():
        print(f"❌ Script not found: {SCRIPT_PATH}")
        return False
    
    print("✅ Script exists")
    return True


def test_api_key():
    """Test API key detection."""
    print("Testing API key...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  GEMINI_API_KEY not found (skipping API tests)")
        return None  # Skip, not fail
    
    print("✅ API key found")
    return True


def test_search():
    """Test search functionality."""
    print("Testing search...")
    
    if "--skip-api" in sys.argv:
        print("⏭️  Skipping API test (--skip-api flag)")
        return None
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⏭️  Skipping API test (no API key)")
        return None
    
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "test query"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=Path(__file__).parent.parent
    )
    
    if result.returncode != 0:
        print(f"❌ Search failed: {result.stderr}")
        return False
    
    print("✅ Search test passed")
    return True


def main():
    tests = [
        test_script_exists,
        test_api_key,
        test_search,
    ]
    
    results = []
    for test in tests:
        result = test()
        if result is not None:  # None means skip
            results.append(result)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"\n{passed}/{total} tests passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
