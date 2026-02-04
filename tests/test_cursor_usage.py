#!/usr/bin/env python3
"""
Tests for cursor_usage.py

Tests:
- Import command
- Report command
- Quota command
- Budget command
- Alerts command
- Reminder command
"""

import sys
import os
import subprocess
import tempfile
import csv
import shutil
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

SCRIPT_PATH = Path(__file__).parent.parent / "cursor-scripts" / "cursor_usage.py"


def run_command(cmd: list) -> tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)] + cmd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def create_sample_csv() -> Path:
    """Create a sample CSV for testing (matches Cursor export format)."""
    temp_dir = Path(tempfile.mkdtemp())
    csv_file = temp_dir / "test_usage.csv"
    
    # Sample CSV data matching Cursor's export format
    sample_data = [
        {
            "Date": "2026-01-25T10:00:00.000Z",
            "Kind": "Included",
            "Model": "auto",
            "Max Mode": "No",
            "Input (w/ Cache Write)": "100",
            "Input (w/o Cache Write)": "50",
            "Cache Read": "500",
            "Output Tokens": "200",
            "Total Tokens": "850",
            "Cost": "0.10"
        },
        {
            "Date": "2026-01-25T11:00:00.000Z",
            "Kind": "Included",
            "Model": "claude-4.5-opus-high-thinking",
            "Max Mode": "No",
            "Input (w/ Cache Write)": "500",
            "Input (w/o Cache Write)": "100",
            "Cache Read": "2000",
            "Output Tokens": "1000",
            "Total Tokens": "3600",
            "Cost": "0.50"
        }
    ]
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=sample_data[0].keys())
        writer.writeheader()
        writer.writerows(sample_data)
    
    return csv_file


def test_import():
    """Test CSV import."""
    print("Testing import command...")
    csv_file = create_sample_csv()
    
    # Create a temp directory structure that matches expected layout
    temp_dir = Path(tempfile.mkdtemp())
    usage_dir = temp_dir / "cursor-usage"
    usage_dir.mkdir()
    
    # Copy CSV to temp usage dir
    test_csv = usage_dir / "test_usage.csv"
    import shutil
    shutil.copy(csv_file, test_csv)
    
    # Change to temp directory (so script finds cursor-usage/)
    old_cwd = Path.cwd()
    try:
        os.chdir(temp_dir)
        returncode, stdout, stderr = run_command(["import", str(test_csv)])
    finally:
        os.chdir(old_cwd)
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    if returncode != 0:
        print(f"❌ Import failed: {stderr}")
        return False
    
    if "imported" not in stdout.lower():
        print(f"❌ Import output unexpected: {stdout}")
        return False
    
    print("✅ Import test passed")
    return True


def test_report():
    """Test report command."""
    print("Testing report command...")
    returncode, stdout, stderr = run_command(["report"])
    
    if returncode != 0:
        # Check if it's just a "no data" case
        if "no data" in stderr.lower() or "no records" in stderr.lower():
            print("⚠️  Report has no data (OK for test)")
            return True
        print(f"❌ Report failed: {stderr}")
        return False
    
    # Report should work even with no data (just show zeros)
    print("✅ Report test passed")
    return True


def test_quota():
    """Test quota command."""
    print("Testing quota command...")
    returncode, stdout, stderr = run_command(["quota"])
    
    if returncode != 0:
        print(f"❌ Quota failed: {stderr}")
        return False
    
    if "quota" not in stdout.lower():
        print(f"❌ Quota output unexpected: {stdout[:200]}")
        return False
    
    print("✅ Quota test passed")
    return True


def test_budget():
    """Test budget command."""
    print("Testing budget command...")
    returncode, stdout, stderr = run_command(["budget"])
    
    if returncode != 0:
        print(f"❌ Budget failed: {stderr}")
        return False
    
    print("✅ Budget test passed")
    return True


def test_alerts():
    """Test alerts command."""
    print("Testing alerts command...")
    returncode, stdout, stderr = run_command(["alerts", "--warn", "50", "--fail", "90"])
    
    # Exit code 0, 1, or 2 are all valid (0=ok, 1=warn, 2=fail)
    if returncode > 2:
        print(f"❌ Alerts failed: {stderr}")
        return False
    
    print("✅ Alerts test passed")
    return True


def test_reminder():
    """Test reminder command."""
    print("Testing reminder command...")
    returncode, stdout, stderr = run_command(["reminder", "--no-stamp"])
    
    if returncode != 0:
        print(f"❌ Reminder failed: {stderr}")
        return False
    
    print("✅ Reminder test passed")
    return True


def main():
    tests = [
        test_import,
        test_report,
        test_quota,
        test_budget,
        test_alerts,
        test_reminder,
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} raised exception: {e}")
    
    print(f"\n{passed}/{len(tests)} tests passed")
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
