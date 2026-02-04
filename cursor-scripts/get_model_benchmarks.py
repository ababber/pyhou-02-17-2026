#!/usr/bin/env python3
"""
Fetch latest AI model benchmarks and assessments for model selection recommendations.

Usage:
    python cursor-scripts/get_model_benchmarks.py [task_type]
    
    task_type: Optional. One of: coding, reasoning, writing, fast, general
"""

import sys
import subprocess
from pathlib import Path

# Get script directory
SCRIPT_DIR = Path(__file__).parent
WEB_SEARCH_SCRIPT = SCRIPT_DIR / "web_search.py"

def get_benchmarks_for_task(task_type=None):
    """Fetch latest benchmarks relevant to the task type."""
    
    queries = []
    
    if task_type == "coding":
        queries = [
            "LMSYS Chatbot Arena leaderboard 2026 Claude GPT Gemini coding",
            "SWE-bench HumanEval MBPP coding benchmarks 2026 Claude Opus GPT-5 Gemini",
            "AI model coding performance comparison 2026 best for software engineering"
        ]
    elif task_type == "reasoning":
        queries = [
            "AI model reasoning benchmarks ARC-AGI GPQA 2026 Claude GPT Gemini",
            "LMSYS Chatbot Arena reasoning performance 2026",
            "best AI model complex reasoning problem solving 2026"
        ]
    elif task_type == "writing":
        queries = [
            "AI model writing quality benchmarks 2026 Claude Sonnet GPT Gemini",
            "best AI model documentation writing 2026",
            "LMSYS Chatbot Arena writing performance 2026"
        ]
    elif task_type == "fast":
        queries = [
            "fast AI models cost comparison 2026 Gemini Flash Claude Haiku GPT pricing",
            "AI model speed latency comparison 2026",
            "cost effective AI models tokens per dollar 2026"
        ]
    else:  # general or no task specified
        queries = [
            "LMSYS Chatbot Arena leaderboard 2026 latest rankings Claude GPT Gemini",
            "AI model benchmarks comparison 2026 Claude Opus GPT-5 Gemini Pro",
            "best AI model 2026 coding reasoning writing performance"
        ]
    
    print(f"Fetching latest benchmarks for: {task_type or 'general'}")
    print("=" * 70)
    
    results = []
    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] Searching: {query}")
        try:
            result = subprocess.run(
                [sys.executable, str(WEB_SEARCH_SCRIPT), query],
                capture_output=True,
                text=True,
                check=True
            )
            results.append(result.stdout)
            print("Retrieved")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            results.append(f"Error fetching: {query}\n")
    
    print("\n" + "=" * 70)
    print("Summary of latest benchmark data:")
    print("=" * 70)
    
    # Print all results
    for result in results:
        print(result)
        print("\n" + "-" * 70 + "\n")
    
    return results

if __name__ == "__main__":
    task_type = sys.argv[1] if len(sys.argv) > 1 else None
    get_benchmarks_for_task(task_type)
