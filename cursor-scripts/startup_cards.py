#!/usr/bin/env python3
"""
Startup Cards - Daily digest and quiz for conversation startup

Shows two cards after normal AI startup:
1. Daily digest (cards due, streak, next task)
2. Random quiz from yesterday's work

Usage:
    python startup_cards.py              # Full output
    python startup_cards.py --digest     # Just digest
    python startup_cards.py --quiz       # Just quiz
    python startup_cards.py --json       # JSON output for parsing
    python startup_cards.py --compact    # Compact single-line output
    python startup_cards.py --reveal     # Show quiz answer (auto-records as review for real cards)
"""

import argparse
import json
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Import from sibling modules
sys.path.insert(0, str(Path(__file__).parent))
from review import load_cards, get_due_cards, get_stats, get_random_card, review_card

# File to persist the current quiz card between calls
QUIZ_CACHE_FILE = Path(__file__).parent.parent / "cursor-data" / ".current_quiz.json"


def get_yesterday_files() -> list:
    """Get files modified yesterday from git log."""
    try:
        # Get yesterday's date
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Get files changed yesterday
        result = subprocess.run(
            ["git", "log", "--since", yesterday, "--until", "today", "--name-only", "--pretty=format:"],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0:
            files = [f.strip() for f in result.stdout.split("\n") if f.strip()]
            return list(set(files))  # Deduplicate
    except Exception:
        pass
    
    return []


def get_digest() -> dict:
    """Get daily digest information."""
    stats = get_stats()
    
    # Get next task hint from progress (future: integrate with progress tracker)
    next_task = None
    
    return {
        "due_cards": stats["due_today"],
        "streak": stats["streak_days"],
        "total_cards": stats["total_cards"],
        "mastered": stats["mastered"],
        "learning": stats["learning"],
        "next_task": next_task
    }


def save_quiz_card(quiz: dict) -> None:
    """Save quiz card to cache for later reveal."""
    try:
        QUIZ_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(QUIZ_CACHE_FILE, 'w') as f:
            json.dump({
                "quiz": quiz,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2, default=str)
    except Exception:
        pass  # Silently fail - not critical


def load_quiz_card() -> dict:
    """Load quiz card from cache."""
    try:
        if QUIZ_CACHE_FILE.exists():
            with open(QUIZ_CACHE_FILE) as f:
                data = json.load(f)
            return data.get("quiz", {})
    except Exception:
        pass
    return {}


def get_quiz_card(use_cache: bool = False) -> dict:
    """Get a quiz card based on yesterday's work.
    
    Args:
        use_cache: If True, load from cache instead of generating new card.
    """
    # If using cache (for reveal), load saved card only — never generate
    if use_cache:
        cached = load_quiz_card()
        if cached and cached.get("card"):
            return cached
        # No cache: return empty quiz so reveal says "No quiz card available"
        return {"card": None, "source_type": ""}

    # First, try to get files from yesterday's git activity
    yesterday_files = get_yesterday_files()
    
    card = None
    source_type = "random"
    
    if yesterday_files:
        # Try to find a flashcard related to yesterday's files
        card = get_random_card(from_files=yesterday_files)
        if card:
            source_type = "yesterday_flashcard"
    
    if not card:
        # Fall back to any random flashcard
        card = get_random_card()
        if card:
            source_type = "random_flashcard"
    
    quiz = {
        "card": card,
        "source_type": source_type
    }
    
    # Save to cache for later reveal
    save_quiz_card(quiz)
    
    return quiz


def format_digest(digest: dict) -> str:
    """Format digest for display."""
    lines = [
        "─────────────────────────────────────────",
        "📋 DAILY DIGEST"
    ]
    
    if digest["due_cards"] > 0:
        lines.append(f"   {digest['due_cards']} card(s) due for review")
    else:
        lines.append("   No cards due today ✓")
    
    if digest["streak"] > 0:
        lines.append(f"   Streak: {digest['streak']} day(s) 🔥")
    
    if digest["total_cards"] > 0:
        lines.append(f"   Library: {digest['total_cards']} cards ({digest['mastered']} mastered)")
    
    if digest["next_task"]:
        lines.append(f"   Next: {digest['next_task']}")
    
    lines.append("─────────────────────────────────────────")
    
    return "\n".join(lines)


def format_quiz(quiz: dict) -> str:
    """Format quiz card for display."""
    card = quiz.get("card")
    
    if not card:
        return ""
    
    source_label = {
        "yesterday_flashcard": "from yesterday's work",
        "random_flashcard": "random review",
    }.get(quiz.get("source_type", ""), "")
    
    lines = [
        "─────────────────────────────────────────",
        f"🎴 QUICK QUIZ ({source_label})",
        "",
        f"   Q: {card['question']}",
        "",
        "   [Answer with 'reveal' or type your answer]",
        "─────────────────────────────────────────"
    ]
    
    return "\n".join(lines)


def format_compact(digest: dict, quiz: dict) -> str:
    """Format as compact single line."""
    parts = []
    
    if digest["due_cards"] > 0:
        parts.append(f"📚 {digest['due_cards']} due")
    
    if digest["streak"] > 0:
        parts.append(f"🔥 {digest['streak']}d streak")
    
    if quiz.get("card"):
        parts.append("🎴 Quiz ready")
    
    return " | ".join(parts) if parts else "No cards or quizzes"


def reveal_answer(quiz: dict) -> str:
    """Reveal the answer to the quiz."""
    card = quiz.get("card")
    if not card:
        return "No quiz card available."
    
    lines = [
        "─────────────────────────────────────────",
        "🎴 ANSWER",
        "",
        f"   A: {card['answer']}",
        ""
    ]
    
    if card.get("source"):
        lines.append(f"   Source: {card['source']}")
    
    lines.append("─────────────────────────────────────────")
    
    return "\n".join(lines)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Startup cards for daily digest and quiz",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python startup_cards.py              # Full startup cards
  python startup_cards.py --digest     # Just the digest
  python startup_cards.py --quiz       # Just the quiz
  python startup_cards.py --compact    # Single line summary
  python startup_cards.py --reveal     # Show quiz answer
        """
    )
    
    parser.add_argument("--digest", action="store_true", help="Show only digest")
    parser.add_argument("--quiz", action="store_true", help="Show only quiz")
    parser.add_argument("--reveal", action="store_true", help="Reveal quiz answer")
    parser.add_argument("--compact", action="store_true", help="Compact single-line output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    digest = get_digest()
    
    # Use cache for reveal operations to get the same card that was shown
    use_cache = args.reveal
    quiz = get_quiz_card(use_cache=use_cache)
    
    # JSON output
    if args.json:
        output = {
            "digest": digest,
            "quiz": quiz,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(output, indent=2, default=str))
        return
    
    # Compact output
    if args.compact:
        print(format_compact(digest, quiz))
        return
    
    # Reveal answer (track as review for real flashcards — updates SM-2)
    if args.reveal:
        print(reveal_answer(quiz))
        card = quiz.get("card")
        if card and card.get("id") and not card.get("generated"):
            updated = review_card(card["id"], 4)  # 4 = engaged, count as review
            next_review = datetime.fromisoformat(updated["next_review"]).strftime("%Y-%m-%d")
            print(f"\n   Recorded as reviewed (next: {next_review})\n")
        return
    
    # Digest only
    if args.digest:
        print(format_digest(digest))
        return
    
    # Quiz only
    if args.quiz:
        print(format_quiz(quiz))
        return
    
    # Full output (default)
    print(format_digest(digest))
    if quiz.get("card"):
        print(format_quiz(quiz))


if __name__ == "__main__":
    main()
