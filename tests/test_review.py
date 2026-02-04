#!/usr/bin/env python3
"""
Tests for review.py (flashcards and quiz-through-AI).

Tests:
- Script exists
- Add card and load
- Digest / stats
- Quiz start (no cards, practice with cards)
- Quiz answer/skip with no state
- Full quiz flow (start -> answer -> complete)
- Review card updates schedule
"""

import sys
import tempfile
from pathlib import Path

# Add parent and cursor-scripts to path so "import review" finds cursor-scripts/review.py
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cursor-scripts"))

SCRIPT_PATH = ROOT / "cursor-scripts" / "review.py"
DATA_DIR = ROOT / "cursor-data"


def use_temp_data():
    """Patch review module to use a temp dir; return (tmp_path, review module)."""
    tmp = Path(tempfile.mkdtemp())
    import review as mod
    mod.DATA_DIR = tmp
    mod.FLASHCARDS_FILE = tmp / "flashcards.json"
    mod.QUIZ_STATE_FILE = tmp / ".quiz_state.json"
    return tmp, mod


def test_script_exists():
    """Test that review.py exists."""
    print("Testing script exists...")
    if not SCRIPT_PATH.exists():
        print(f"❌ Script not found: {SCRIPT_PATH}")
        return False
    print("✅ Script exists")
    return True


def test_add_and_load():
    """Test add_card and load_cards."""
    print("Testing add card and load...")
    tmp, review = use_temp_data()
    try:
        card = review.add_card("Q1?", "A1", "dev")
        if not card.get("id"):
            print("❌ add_card did not return id")
            return False
        data = review.load_cards()
        if len(data["cards"]) != 1:
            print(f"❌ Expected 1 card, got {len(data['cards'])}")
            return False
        if data["cards"][0]["question"] != "Q1?":
            print("❌ Card question mismatch")
            return False
        print("✅ Add and load passed")
        return True
    finally:
        tmp.exists() and tmp.joinpath("flashcards.json").unlink(missing_ok=True)


def test_digest():
    """Test digest / get_stats."""
    print("Testing digest/stats...")
    tmp, review = use_temp_data()
    try:
        review.add_card("Q?", "A", "general")
        stats = review.get_stats()
        for key in ("total_cards", "due_today", "streak_days", "total_reviews"):
            if key not in stats:
                print(f"❌ get_stats missing key: {key}")
                return False
        if stats["total_cards"] != 1:
            print(f"❌ Expected 1 total card, got {stats['total_cards']}")
            return False
        print("✅ Digest/stats passed")
        return True
    finally:
        tmp.joinpath("flashcards.json").unlink(missing_ok=True)


def test_quiz_start_no_cards():
    """Test quiz_start with no cards (due)."""
    print("Testing quiz start with no cards...")
    tmp, review = use_temp_data()
    try:
        out = review.quiz_start(practice=False)
        if "No cards due" not in out:
            print(f"❌ Expected 'No cards due', got: {out[:120]}")
            return False
        print("✅ Quiz start (no cards) passed")
        return True
    finally:
        review.clear_quiz_state()


def test_quiz_start_practice_empty():
    """Test quiz_start practice with empty deck."""
    print("Testing quiz start practice (empty deck)...")
    tmp, review = use_temp_data()
    try:
        out = review.quiz_start(practice=True, practice_limit=5)
        if "No cards" not in out and "Add cards" not in out:
            print(f"❌ Expected no-cards message, got: {out[:120]}")
            return False
        print("✅ Quiz start practice (empty) passed")
        return True
    finally:
        review.clear_quiz_state()


def test_quiz_start_practice_with_cards():
    """Test quiz_start practice with cards."""
    print("Testing quiz start practice with cards...")
    tmp, review = use_temp_data()
    try:
        review.add_card("Practice Q?", "Practice A", "concept")
        review.add_card("Practice Q2?", "Practice A2", "tool")
        out = review.quiz_start(practice=True, practice_limit=2)
        if "PRACTICE" not in out:
            print(f"❌ Expected PRACTICE in output, got: {out[:200]}")
            return False
        if "Q:" not in out or "Practice" not in out:
            print(f"❌ Expected question in output, got: {out[:200]}")
            return False
        print("✅ Quiz start practice (with cards) passed")
        return True
    finally:
        review.clear_quiz_state()
        tmp.joinpath("flashcards.json").unlink(missing_ok=True)


def test_quiz_answer_no_state():
    """Test quiz_answer when no quiz in progress."""
    print("Testing quiz answer (no state)...")
    tmp, review = use_temp_data()
    try:
        out = review.quiz_answer("some answer")
        if "No quiz in progress" not in out:
            print(f"❌ Expected 'No quiz in progress', got: {out[:120]}")
            return False
        print("✅ Quiz answer (no state) passed")
        return True
    finally:
        review.clear_quiz_state()


def test_quiz_skip_no_state():
    """Test quiz_skip when no quiz in progress."""
    print("Testing quiz skip (no state)...")
    tmp, review = use_temp_data()
    try:
        out = review.quiz_skip()
        if "No quiz in progress" not in out:
            print(f"❌ Expected 'No quiz in progress', got: {out[:120]}")
            return False
        print("✅ Quiz skip (no state) passed")
        return True
    finally:
        review.clear_quiz_state()


def test_full_quiz_flow():
    """Test full flow: add card -> start -> answer -> complete."""
    print("Testing full quiz flow...")
    tmp, review = use_temp_data()
    try:
        review.add_card("Full flow Q?", "Full flow A", "general")
        start_out = review.quiz_start(practice=False)
        if "Q:" not in start_out or "Full flow Q?" not in start_out:
            print(f"❌ Start missing question: {start_out[:200]}")
            return False
        answer_out = review.quiz_answer("my answer")
        if "CORRECT ANSWER" not in answer_out or "Full flow A" not in answer_out:
            print(f"❌ Answer missing correct answer: {answer_out[:200]}")
            return False
        if "QUIZ COMPLETE" not in answer_out:
            print(f"❌ Expected QUIZ COMPLETE: {answer_out[-200:]}")
            return False
        # After complete, answer again should say no quiz
        out2 = review.quiz_answer("x")
        if "No quiz in progress" not in out2 and "finished" not in out2.lower():
            print(f"❌ After complete, expected no quiz: {out2[:120]}")
            return False
        print("✅ Full quiz flow passed")
        return True
    finally:
        review.clear_quiz_state()
        tmp.joinpath("flashcards.json").unlink(missing_ok=True)


def test_review_card_updates_schedule():
    """Test that review_card updates next_review."""
    print("Testing review_card updates schedule...")
    tmp, review = use_temp_data()
    try:
        from datetime import datetime, timedelta
        card = review.add_card("Schedule Q?", "Schedule A", "general")
        before = datetime.fromisoformat(card["next_review"])
        updated = review.review_card(card["id"], 4)
        after = datetime.fromisoformat(updated["next_review"])
        if after <= before:
            print(f"❌ next_review should increase after review, got {before} -> {after}")
            return False
        print("✅ Review card schedule passed")
        return True
    finally:
        tmp.joinpath("flashcards.json").unlink(missing_ok=True)


def main():
    tests = [
        test_script_exists,
        test_add_and_load,
        test_digest,
        test_quiz_start_no_cards,
        test_quiz_start_practice_empty,
        test_quiz_start_practice_with_cards,
        test_quiz_answer_no_state,
        test_quiz_skip_no_state,
        test_full_quiz_flow,
        test_review_card_updates_schedule,
    ]
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} raised: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
