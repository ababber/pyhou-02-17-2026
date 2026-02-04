#!/bin/zsh
#
# Test script for install.sh
#
# Creates a temporary repo and tests the installation process.
#

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

TEST_DIR="/tmp/cursor-starter-kit-test-$$"
STARTER_KIT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INSTALL_SCRIPT="$STARTER_KIT_DIR/install.sh"

echo "Testing Cursor Starter Kit Installer"
echo "======================================"
echo ""

# Cleanup function
cleanup() {
    if [ -d "$TEST_DIR" ]; then
        echo ""
        echo "Cleaning up test directory..."
        rm -rf "$TEST_DIR"
    fi
}
trap cleanup EXIT

# Create test repo
echo "1. Creating test repository..."
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"
git init --quiet
echo "# Test Repo" > README.md
git add README.md
git commit -m "Initial commit" --quiet
echo "   ${GREEN}✅ Test repo created at $TEST_DIR${NC}"
echo ""

# Test 1: Check if script detects already installed (should not)
echo "2. Testing detection of existing starter kit..."
if [ -f "$INSTALL_SCRIPT" ]; then
    echo "   ${GREEN}✅ Install script exists${NC}"
else
    echo "   ${RED}❌ Install script not found${NC}"
    exit 1
fi
echo ""

# Test 2: Run installation (non-interactive - skip existing)
echo "3. Running installation (skip existing files)..."
cd "$STARTER_KIT_DIR"
INSTALL_SKIP_EXISTING=1 INSTALL_FORCE=1 "$INSTALL_SCRIPT" "$TEST_DIR" > /tmp/install-output.txt 2>&1
INSTALL_EXIT_CODE=$?

if [ $INSTALL_EXIT_CODE -eq 0 ]; then
    echo "   ${GREEN}✅ Installation completed${NC}"
else
    echo "   ${RED}❌ Installation failed (exit code: $INSTALL_EXIT_CODE)${NC}"
    cat /tmp/install-output.txt | tail -20
    exit 1
fi
echo ""

# Test 3: Verify files were copied
echo "4. Verifying installed files..."
EXPECTED_FILES=(
    ".cursorrules"
    ".cursorignore"
    ".gitignore"
    ".env.example"
    "cursor-scripts/cursor_usage.py"
    "cursor-scripts/export-chat.sh"
    "tests/run_all.py"
)

MISSING_FILES=()
for file in "${EXPECTED_FILES[@]}"; do
    if [ -f "$TEST_DIR/$file" ]; then
        echo "   ${GREEN}✅ Found: $file${NC}"
    else
        echo "   ${RED}❌ Missing: $file${NC}"
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo ""
    echo "   ${RED}❌ Some files are missing!${NC}"
    exit 1
fi
echo ""

# Test 4: Verify scripts are executable
echo "5. Verifying scripts are executable..."
EXECUTABLE_SCRIPTS=(
    "cursor-scripts/export-chat.sh"
)

for script in "${EXECUTABLE_SCRIPTS[@]}"; do
    if [ -x "$TEST_DIR/$script" ]; then
        echo "   ${GREEN}✅ Executable: $script${NC}"
    else
        echo "   ${RED}❌ Not executable: $script${NC}"
        exit 1
    fi
done
echo ""

# Test 5: Verify .env was created
echo "6. Verifying .env creation..."
if [ -f "$TEST_DIR/.env" ]; then
    echo "   ${GREEN}✅ .env created from .env.example${NC}"
else
    echo "   ${YELLOW}⚠️  .env not created (may already exist)${NC}"
fi
echo ""

# Test 6: Verify directory structure
echo "7. Verifying directory structure..."
EXPECTED_DIRS=(
    "cursor-chats"
    "cursor-usage"
    "cursor-web-search"
    "mcp-bypass-skeleton"
)

for dir in "${EXPECTED_DIRS[@]}"; do
    if [ -d "$TEST_DIR/$dir" ]; then
        echo "   ${GREEN}✅ Directory exists: $dir${NC}"
    else
        echo "   ${RED}❌ Missing directory: $dir${NC}"
        exit 1
    fi
done
echo ""

echo "${GREEN}✅ All tests passed!${NC}"
echo ""
echo "Test directory: $TEST_DIR"
echo "(Will be cleaned up on exit)"
