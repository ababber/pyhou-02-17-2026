#!/usr/bin/env python3
"""
Run all starter kit tests.

Usage:
    python tests/run_all.py
    python tests/run_all.py --skip-api  # Skip API-required tests
"""

import sys
import subprocess
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

SKIP_API = "--skip-api" in sys.argv


def run_test(test_file: str) -> bool:
    """Run a test file and return True if successful."""
    test_path = Path(__file__).parent / test_file
    if not test_path.exists():
        print(f"⚠️  {test_file} not found, skipping")
        return False
    
    print(f"\n{'='*60}")
    print(f"Running {test_file}")
    print(f"{'='*60}")
    
    if test_path.suffix == ".sh":
        cmd = ["zsh", str(test_path)]
    else:
        cmd = [sys.executable, str(test_path)] + (["--skip-api"] if SKIP_API else [])
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode == 0


def main():
    tests = [
        "test_cursor_chats_gitignore.sh",
        "test_fresh_agent.py",
        "test_cursor_usage.py",
        "test_export_chat.py",
        "test_web_search.py",
        "test_review.py",
        "test_startup_cards.py",
    ]
    
    print("Cursor Starter Kit Test Suite")
    print("=" * 60)
    if SKIP_API:
        print("⚠️  API tests will be skipped")
    
    results = {}
    for test in tests:
        results[test] = run_test(test)
    
    # Summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    
    passed = sum(1 for v in results.values() if v)
    total = len([v for v in results.values() if v is not None])
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL" if result is False else "⏭️  SKIP"
        print(f"{status}  {test}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
