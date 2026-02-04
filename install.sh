#!/bin/zsh
#
# Cursor Starter Kit Installer
#
# Adds the Cursor Starter Kit to a repository that doesn't have it.
#
# Usage:
#   ./install.sh [target-repo-path]
#
# If no path provided, installs to current directory.
#
# Environment variables for non-interactive mode:
#   INSTALL_SKIP_EXISTING=1  - Skip existing files (default: 0)
#   INSTALL_BACKUP=1         - Backup and overwrite (default: 0)
#   INSTALL_FORCE=1         - Force reinstall even if already installed (default: 0)
#

set -euo pipefail

# Check for non-interactive mode
NON_INTERACTIVE=false
if [ -n "${INSTALL_SKIP_EXISTING:-}" ] || [ -n "${INSTALL_BACKUP:-}" ] || [ -n "${INSTALL_FORCE:-}" ]; then
    NON_INTERACTIVE=true
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory (starter kit location)
STARTER_KIT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Target repository (default: current directory)
TARGET_REPO="${1:-$(pwd)}"
TARGET_REPO="$(cd "$TARGET_REPO" && pwd)"

echo "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo "${BLUE}  Cursor Starter Kit Installer${NC}"
echo "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "Starter Kit: $STARTER_KIT_DIR"
echo "Target Repo: $TARGET_REPO"
echo ""

# Check if starter kit is already installed
STARTER_KIT_MARKERS=(
    ".cursorrules"
    "cursor-scripts/cursor_usage.py"
    "cursor-scripts/export-chat.sh"
)

ALREADY_INSTALLED=false
for marker in "${STARTER_KIT_MARKERS[@]}"; do
    if [ -e "$TARGET_REPO/$marker" ]; then
        # Check if it looks like our starter kit (not just any .cursorrules)
        if [ "$marker" = ".cursorrules" ]; then
            if grep -q "Session Continuity" "$TARGET_REPO/$marker" 2>/dev/null; then
                ALREADY_INSTALLED=true
                break
            fi
        else
            ALREADY_INSTALLED=true
            break
        fi
    fi
done

if [ "$ALREADY_INSTALLED" = true ]; then
    if [ "$NON_INTERACTIVE" = true ] && [ "${INSTALL_FORCE:-0}" = "1" ]; then
        echo "Proceeding with reinstallation (non-interactive mode)..."
    elif [ "$NON_INTERACTIVE" = true ]; then
        echo "${YELLOW}⚠️  Cursor Starter Kit already installed. Set INSTALL_FORCE=1 to reinstall.${NC}"
        exit 0
    else
        echo "${YELLOW}⚠️  Cursor Starter Kit appears to already be installed${NC}"
        echo ""
        echo "Found starter kit files in: $TARGET_REPO"
        echo ""
        echo "Options:"
        echo "  1) Reinstall anyway (will handle existing files)"
        echo "  2) Cancel"
        echo ""
        read -p "Choose option (1-2): " -n 1 -r
        echo
        
        case $REPLY in
            1)
                echo "Proceeding with reinstallation..."
                ;;
            2|*)
                echo "Installation cancelled."
                exit 0
                ;;
        esac
    fi
fi

# Check if target is a git repo
if [ ! -d "$TARGET_REPO/.git" ]; then
    if [ "$NON_INTERACTIVE" = true ]; then
        echo "${YELLOW}⚠️  Warning: Target directory doesn't appear to be a git repository${NC}"
        echo "Continuing anyway (non-interactive mode)..."
    else
        echo "${YELLOW}⚠️  Warning: Target directory doesn't appear to be a git repository${NC}"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Installation cancelled."
            exit 1
        fi
    fi
fi

# Files to copy (excluding install.sh and git files)
FILES_TO_COPY=(
    ".cursorrules"
    ".cursorignore"
    ".gitignore"
    ".env.example"
    "README.md"
    "COMMIT-CONVENTIONS.md"
    "cursor-scripts/"
    "cursor-chats/"
    "cursor-usage/"
    "cursor-web-search/"
    "cursor-data/"
    "mcp-bypass-skeleton/"
    "tests/"
)

# Check for existing files
EXISTING_FILES=()
for item in "${FILES_TO_COPY[@]}"; do
    if [ -e "$TARGET_REPO/$item" ]; then
        EXISTING_FILES+=("$item")
    fi
done

if [ ${#EXISTING_FILES[@]} -gt 0 ]; then
    if [ "$NON_INTERACTIVE" = true ]; then
        # Non-interactive mode: use environment variables
        if [ "${INSTALL_BACKUP:-0}" = "1" ]; then
            SKIP_EXISTING=false
            BACKUP_DIR="$TARGET_REPO/.cursor-starter-kit-backup-$(date +%Y%m%d-%H%M%S)"
            echo "Creating backup in: $BACKUP_DIR"
            mkdir -p "$BACKUP_DIR"
            for file in "${EXISTING_FILES[@]}"; do
                if [ -e "$TARGET_REPO/$file" ]; then
                    cp -r "$TARGET_REPO/$file" "$BACKUP_DIR/" 2>/dev/null || true
                fi
            done
            echo "${GREEN}✅ Backup created${NC}"
        elif [ "${INSTALL_SKIP_EXISTING:-0}" = "1" ]; then
            SKIP_EXISTING=true
            echo "Skipping existing files (non-interactive mode)"
        else
            SKIP_EXISTING=false
            echo "Overwriting existing files (non-interactive mode)"
        fi
    else
        echo "${YELLOW}⚠️  The following files/directories already exist:${NC}"
        for file in "${EXISTING_FILES[@]}"; do
            echo "   - $file"
        done
        echo ""
        echo "Options:"
        echo "  1) Skip existing files (recommended)"
        echo "  2) Backup and overwrite"
        echo "  3) Cancel"
        echo ""
        read -p "Choose option (1-3): " -n 1 -r
        echo
        
        case $REPLY in
            1)
                SKIP_EXISTING=true
                ;;
            2)
                SKIP_EXISTING=false
                BACKUP_DIR="$TARGET_REPO/.cursor-starter-kit-backup-$(date +%Y%m%d-%H%M%S)"
                echo "Creating backup in: $BACKUP_DIR"
                mkdir -p "$BACKUP_DIR"
                for file in "${EXISTING_FILES[@]}"; do
                    if [ -e "$TARGET_REPO/$file" ]; then
                        cp -r "$TARGET_REPO/$file" "$BACKUP_DIR/" 2>/dev/null || true
                    fi
                done
                echo "${GREEN}✅ Backup created${NC}"
                ;;
            3)
                echo "Installation cancelled."
                exit 1
                ;;
            *)
                echo "Invalid option. Installation cancelled."
                exit 1
                ;;
        esac
    fi
else
    SKIP_EXISTING=false
fi

echo ""
echo "${BLUE}Installing files...${NC}"

# Copy files
COPIED=0
SKIPPED=0

for item in "${FILES_TO_COPY[@]}"; do
    source="$STARTER_KIT_DIR/$item"
    target="$TARGET_REPO/$item"
    
    if [ "$SKIP_EXISTING" = true ] && [ -e "$target" ]; then
        echo "   ⏭️  Skipping existing: $item"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi
    
    if [ -d "$source" ]; then
        # Copy directory
        mkdir -p "$(dirname "$target")"
        if cp -r "$source" "$target" 2>/dev/null; then
            echo "   ${GREEN}✅ Copied directory: $item${NC}"
            COPIED=$((COPIED + 1))
        else
            echo "   ${RED}❌ Failed to copy: $item${NC}"
            # Don't exit, continue with other files
        fi
    elif [ -f "$source" ]; then
        # Copy file
        mkdir -p "$(dirname "$target")"
        if cp "$source" "$target" 2>/dev/null; then
            echo "   ${GREEN}✅ Copied file: $item${NC}"
            COPIED=$((COPIED + 1))
        else
            echo "   ${RED}❌ Failed to copy: $item${NC}"
            # Don't exit, continue with other files
        fi
    else
        echo "   ${YELLOW}⚠️  Source not found: $item${NC}"
        # Don't exit, continue with other files
    fi
done

# Make scripts executable
echo ""
echo "${BLUE}Making scripts executable...${NC}"
if [ -d "$TARGET_REPO/cursor-scripts" ]; then
    find "$TARGET_REPO/cursor-scripts" -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
    echo "   ${GREEN}✅ Made shell scripts executable${NC}"
fi

if [ -d "$TARGET_REPO/tests" ]; then
    find "$TARGET_REPO/tests" -type f -name "*.py" -exec chmod +x {} \; 2>/dev/null || true
    echo "   ${GREEN}✅ Made test scripts executable${NC}"
fi

# Create .env from .env.example if .env doesn't exist
if [ -f "$TARGET_REPO/.env.example" ] && [ ! -f "$TARGET_REPO/.env" ]; then
    echo ""
    echo "${BLUE}Creating .env from .env.example...${NC}"
    cp "$TARGET_REPO/.env.example" "$TARGET_REPO/.env"
    echo "   ${GREEN}✅ Created .env${NC}"
    echo "   ${YELLOW}⚠️  Remember to add your API keys to .env${NC}"
fi

# Summary
echo ""
echo "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo "${GREEN}✅ Installation Complete!${NC}"
echo "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "Files copied: $COPIED"
if [ $SKIPPED -gt 0 ]; then
    echo "Files skipped: $SKIPPED"
fi
echo ""

# Next steps
echo "${BLUE}Next Steps:${NC}"
echo ""
echo "1. ${YELLOW}Add API keys${NC}:"
echo "   Edit $TARGET_REPO/.env and add your API keys"
echo ""
echo "2. ${YELLOW}Run tests${NC}:"
echo "   cd $TARGET_REPO"
echo "   python tests/run_all.py"
echo ""
echo "3. ${YELLOW}Customize${NC}:"
echo "   - Edit .cursorrules for project-specific protocols"
echo "   - Update .cursorignore for your file patterns"
echo ""
echo "4. ${YELLOW}Review${NC}:"
echo "   - Check README.md for usage instructions"
echo "   - Review cursor-scripts/ for available tools"
echo ""

if [ -n "${BACKUP_DIR:-}" ]; then
    echo "${YELLOW}Backup location: $BACKUP_DIR${NC}"
    echo ""
fi

echo "${GREEN}Happy coding! 🚀${NC}"
