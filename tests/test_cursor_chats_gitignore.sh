#!/usr/bin/env zsh
#
# Test that cursor-chats/ is set up for the template:
# - cursor-chats/.gitkeep is tracked (shows directory structure)
# - cursor-chats/*.md are ignored (exported chats stay local)
#
# Run from repo root: ./tests/test_cursor_chats_gitignore.sh
#

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

PASS=0
FAIL=0

check() {
    if eval "$@"; then
        echo "   ${GREEN}✅ $1${NC}"
        ((PASS++)) || true
        return 0
    else
        echo "   ${RED}❌ $1${NC}"
        ((FAIL++)) || true
        return 1
    fi
}

echo "Testing cursor-chats/ gitignore behavior"
echo "========================================"
echo ""

echo "1. cursor-chats/.gitkeep is tracked..."
check "git ls-files --error-unmatch cursor-chats/.gitkeep >/dev/null 2>&1"
echo ""

echo "2. .gitignore ignores cursor-chats/*.md..."
check "grep -q 'cursor-chats/\*\.md' .gitignore"
echo ""

echo "3. .gitignore keeps cursor-chats/.gitkeep (exception)..."
check "grep -q '!cursor-chats/\.gitkeep' .gitignore"
echo ""

echo "4. A new .md in cursor-chats/ is ignored by git..."
TEST_MD="cursor-chats/test-export-$$.md"
touch "$TEST_MD"
if git check-ignore -q "$TEST_MD" 2>/dev/null; then
    echo "   ${GREEN}✅ $TEST_MD is ignored${NC}"
    ((PASS++)) || true
else
    echo "   ${RED}❌ $TEST_MD is not ignored (git check-ignore)${NC}"
    ((FAIL++)) || true
fi
STATUS=$(git status --porcelain "$TEST_MD" 2>/dev/null || true)
if [ -z "$STATUS" ]; then
    echo "   ${GREEN}✅ $TEST_MD does not appear in git status${NC}"
    ((PASS++)) || true
else
    echo "   ${RED}❌ $TEST_MD appears in git status: $STATUS${NC}"
    ((FAIL++)) || true
fi
rm -f "$TEST_MD"
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo "${RED}Failed: $FAIL | Passed: $PASS${NC}"
    exit 1
fi
echo "${GREEN}All cursor-chats gitignore tests passed ($PASS)${NC}"
exit 0
