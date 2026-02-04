#!/usr/bin/env python3
"""
Web Search with Logging - Searches via Gemini and logs to cursor-web-search/

Usage:
    python scripts/web_search.py "your search query"
    
Logs to: cursor-web-search/CURSOR-WEB_YYYY-DD-MM_NN.md (splits at 5MB)
"""

import os
import sys
import re
import glob
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes


def get_log_path() -> Path:
    """Get today's log file path, splitting by size if needed."""
    script_dir = Path(__file__).parent.parent
    log_dir = script_dir / "cursor-web-search"
    log_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%d-%m")
    pattern = str(log_dir / f"CURSOR-WEB_{today}_*.md")
    existing_files = sorted(glob.glob(pattern))
    
    if not existing_files:
        # First file of the day
        return log_dir / f"CURSOR-WEB_{today}_01.md"
    
    # Check size of most recent file
    latest_file = Path(existing_files[-1])
    file_size = latest_file.stat().st_size if latest_file.exists() else 0
    
    if file_size >= MAX_FILE_SIZE:
        # Need new file - extract and increment number
        match = re.search(r'_(\d+)\.md$', str(latest_file))
        if match:
            file_num = int(match.group(1)) + 1
        else:
            file_num = len(existing_files) + 1
        return log_dir / f"CURSOR-WEB_{today}_{file_num:02d}.md"
    
    return latest_file


def append_to_log(query: str, summary: str) -> Path:
    """Append search result to daily log file."""
    log_path = get_log_path()
    
    # Create file with header if it doesn't exist
    if not log_path.exists():
        today = datetime.now().strftime("%Y-%d-%m")
        file_num = re.search(r'_(\d+)\.md$', str(log_path))
        file_num = file_num.group(1) if file_num else "01"
        log_path.write_text(f"# CURSOR-WEB_{today}_{file_num}\n\n")
    
    # Append search entry
    with open(log_path, "a") as f:
        f.write(f"\n## {query}\n")
        f.write(f"### {summary}\n")
    
    return log_path


def search(query: str) -> str:
    """
    Performs a Google Search using Gemini's grounding capabilities.
    Returns real-time web results.
    """
    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not set"
    
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_modalities=["TEXT"],
            ),
        )

        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return "No results found."

    except Exception as e:
        return f"Error performing search: {str(e)}"


def summarize_for_log(result: str, max_length: int = 500) -> str:
    """Create a concise summary for the log file."""
    # Take first paragraph or truncate
    lines = result.strip().split("\n")
    summary = " ".join(lines[:3]).replace("\n", " ").strip()
    
    if len(summary) > max_length:
        summary = summary[:max_length] + "..."
    
    return summary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python web_search.py 'your query'")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    
    # Perform search
    result = search(query)
    print(result)
    
    # Log to file
    summary = summarize_for_log(result)
    log_path = append_to_log(query, summary)
    
    print(f"\n---\nLogged to: {log_path}")
