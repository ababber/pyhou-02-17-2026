#!/usr/bin/env python3
"""
Tests for startup_cards.py (daily digest and quiz/reveal).

Tests:
- Script exists
- Digest format (get_digest, format_digest)
- Get quiz card (empty deck, with cards)
- Reveal with no cached quiz
- Reveal records as review for real cards
"""

import sys
import tempfile
from pathlib import Path

# Add parent and cursor-scripts so we can import review then startup_cards
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cursor-scripts"))

SCRIPT_PATH = ROOT / "cursor-scripts" / "startup_cards.py"


def use_temp_data():
    """Patch review and startup_cards to use temp dir; return (tmp_path, startup_cards module)."""
    tmp = Path(tempfile.mkdtemp())
    import review
    review.DATA_DIR = tmp
    review.FLASHCARDS_FILE = tmp / "flashcards.json"
    review.QUIZ_STATE_FILE = tmp / ".quiz_state.json"
    import startup_cards as sc
    sc.QUIZ_CACHE_FILE = tmp / ".current_quiz.json"
    return tmp, sc


def test_script_exists():
    """Test that startup_cards.py exists."""
    print("Testing script exists...")
    if not SCRIPT_PATH.exists():
        print(f"❌ Script not found: {SCRIPT_PATH}")
        return False
    print("✅ Script exists")
    return True


def test_digest_format():
    """Test get_digest and format_digest."""
    print("Testing digest format...")
    tmp, sc = use_temp_data()
    try:
        digest = sc.get_digest()
        for key in ("due_cards", "streak", "total_cards", "mastered", "learning"):
            if key not in digest:
                print(f"❌ get_digest missing key: {key}")
                return False
        formatted = sc.format_digest(digest)
        if "DAILY DIGEST" not in formatted:
            print(f"❌ format_digest missing DAILY DIGEST: {formatted[:150]}")
            return False
        print("✅ Digest format passed")
        return True
    finally:
        pass


def test_get_quiz_card_empty():
    """Test get_quiz_card with empty deck."""
    print("Testing get quiz card (empty deck)...")
    tmp, sc = use_temp_data()
    try:
        quiz = sc.get_quiz_card(use_cache=False)
        if quiz.get("card") is not None:
            print(f"❌ Expected no card with empty deck, got: {quiz}")
            return False
        print("✅ Get quiz card (empty) passed")
        return True
    finally:
        pass


def test_get_quiz_card_with_cards():
    """Test get_quiz_card when deck has cards."""
    print("Testing get quiz card (with cards)...")
    tmp, sc = use_temp_data()
    try:
        import review
        review.add_card("Startup Q?", "Startup A", "general")
        quiz = sc.get_quiz_card(use_cache=False)
        if not quiz.get("card"):
            print(f"❌ Expected a card, got: {quiz}")
            return False
        if quiz["card"].get("question") != "Startup Q?":
            print(f"❌ Card question mismatch: {quiz['card']}")
            return False
        print("✅ Get quiz card (with cards) passed")
        return True
    finally:
        tmp.joinpath("flashcards.json").unlink(missing_ok=True)


def test_reveal_no_quiz():
    """Test reveal when no cached quiz (use_cache=True, empty cache)."""
    print("Testing reveal (no cached quiz)...")
    tmp, sc = use_temp_data()
    try:
        quiz = sc.get_quiz_card(use_cache=True)  # no cache -> returns empty
        out = sc.reveal_answer(quiz)
        if "No quiz card available" not in out:
            print(f"❌ Expected 'No quiz card available', got: {out[:120]}")
            return False
        print("✅ Reveal (no quiz) passed")
        return True
    finally:
        tmp.joinpath(".current_quiz.json").unlink(missing_ok=True)


def test_reveal_records_review():
    """Test that --reveal path records as review for real cards."""
    print("Testing reveal records as review...")
    tmp, sc = use_temp_data()
    try:
        import review
        card = review.add_card("Reveal Q?", "Reveal A", "general")
        card_id = card["id"]
        # Simulate: get quiz (saves to cache), then "reveal" logic
        quiz = sc.get_quiz_card(use_cache=False)
        if not quiz.get("card") or quiz["card"].get("id") != card_id:
            print("❌ Quiz card mismatch")
            return False
        # Call review_card as startup_cards does on reveal (for real, non-generated cards)
        updated = review.review_card(card_id, 4)
        if not updated.get("next_review"):
            print("❌ review_card did not set next_review")
            return False
        from datetime import datetime
        next_dt = datetime.fromisoformat(updated["next_review"])
        if next_dt <= datetime.now():
            print("❌ next_review should be in future after review")
            return False
        print("✅ Reveal records review passed")
        return True
    finally:
        tmp.joinpath("flashcards.json").unlink(missing_ok=True)
        tmp.joinpath(".current_quiz.json").unlink(missing_ok=True)


def main():
    tests = [
        test_script_exists,
        test_digest_format,
        test_get_quiz_card_empty,
        test_get_quiz_card_with_cards,
        test_reveal_no_quiz,
        test_reveal_records_review,
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
