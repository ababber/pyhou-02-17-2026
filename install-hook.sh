#!/bin/zsh
#
# Install post-commit hook for automatic template sync
#
# Usage:
#   ./install-hook.sh [--uninstall]
#
# This script installs the post-commit hook that automatically syncs
# the template repository whenever cursor-starter-kit/ changes.

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOOK_SOURCE="$SCRIPT_DIR/hooks/post-commit"
HOOK_TARGET=".git/hooks/post-commit"

# Parse arguments
UNINSTALL=false
SKIP_CONFIRM=false
for arg in "$@"; do
    case "$arg" in
        --uninstall)
            UNINSTALL=true
            ;;
        --yes|-y)
            SKIP_CONFIRM=true
            ;;
        *)
            echo "${RED}Unknown option: $arg${NC}"
            echo "Usage: $0 [--uninstall] [--yes]"
            exit 1
            ;;
    esac
done

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo "${RED}❌ Not in a git repository${NC}"
    echo "Run this script from the root of your git repository."
    exit 1
fi

# Check if hook source exists
if [ ! -f "$HOOK_SOURCE" ]; then
    echo "${RED}❌ Hook source not found: $HOOK_SOURCE${NC}"
    exit 1
fi

if [ "$UNINSTALL" = true ]; then
    # Uninstall hook
    if [ -f "$HOOK_TARGET" ]; then
        # Check if it's our hook (simple check for our comment)
        if grep -q "Auto-sync template repo" "$HOOK_TARGET" 2>/dev/null; then
            rm "$HOOK_TARGET"
            echo "${GREEN}✅ Post-commit hook uninstalled${NC}"
        else
            echo "${YELLOW}⚠️  Hook exists but doesn't appear to be the template sync hook${NC}"
            echo "Not removing (might be a custom hook)"
            exit 1
        fi
    else
        echo "${YELLOW}⚠️  Hook not installed${NC}"
    fi
else
    # Install hook
    echo "${BLUE}Installing post-commit hook...${NC}"
    
    # Check if hook already exists
    if [ -f "$HOOK_TARGET" ]; then
        if grep -q "Auto-sync template repo" "$HOOK_TARGET" 2>/dev/null; then
            if [ "$SKIP_CONFIRM" = false ]; then
                echo "${YELLOW}⚠️  Hook already installed${NC}"
                if read -q "REPLY?Overwrite? (y/N): " 2>/dev/null; then
                    echo ""
                    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
                        echo "${BLUE}Cancelled.${NC}"
                        exit 0
                    fi
                else
                    # Non-interactive - skip confirmation
                    echo "${YELLOW}(Non-interactive mode - overwriting)${NC}"
                fi
            else
                echo "${YELLOW}⚠️  Hook already installed (overwriting)${NC}"
            fi
        else
            if [ "$SKIP_CONFIRM" = false ]; then
                echo "${YELLOW}⚠️  Hook exists but is different${NC}"
                if read -q "REPLY?Overwrite? (y/N): " 2>/dev/null; then
                    echo ""
                    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
                        echo "${BLUE}Cancelled.${NC}"
                        exit 0
                    fi
                else
                    # Non-interactive - skip confirmation
                    echo "${YELLOW}(Non-interactive mode - overwriting)${NC}"
                fi
            else
                echo "${YELLOW}⚠️  Hook exists but is different (overwriting)${NC}"
            fi
        fi
    fi
    
    # Copy hook
    cp "$HOOK_SOURCE" "$HOOK_TARGET"
    chmod +x "$HOOK_TARGET"
    
    echo "${GREEN}✅ Post-commit hook installed${NC}"
    echo ""
    echo "${BLUE}The hook will automatically sync the template repository${NC}"
    echo "${BLUE}whenever you commit changes to cursor-starter-kit/${NC}"
    echo ""
    echo "${YELLOW}To uninstall:${NC} ./install-hook.sh --uninstall"
fi
